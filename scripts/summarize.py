#!/usr/bin/env python3
"""Summarize an official X Archive + Under the Hood export.

Only allowlisted files are read. DMs, emails, IPs, and Grok chats are skipped.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ALLOWED_FILES = {
    "account.js",
    "account-label.js",
    "article-metadata.js",
    "article.js",
    "deleted-tweets.js",
    "follower.js",
    "following.js",
    "like.js",
    "note-tweet.js",
    "professional-data.js",
    "profile.js",
    "screen-name-change.js",
    "tweets.js",
}

BLOCKED_NAME_PARTS = (
    "direct-message",
    "email-address",
    "phone-number",
    "ip-audit",
    "account-creation-ip",
    "grok-chat",
    "sso.js",
    "contact.js",
)

THEME_RULES = [
    ("growth_follow", r"互关|回关|互粉|互赞|涨粉|涨了\s*\d+\s*粉|过万粉|follow\s*back|follow4follow|#蓝V"),
    ("adult", r"黄片|黄推|成人内容|av\b|nsfw|onlyfans|福利照片|女优"),
    ("product_promo", r"限时|折扣|优惠码|promo\b|discount|猛蹬"),
    ("tutorial_tools", r"教程|怎么用|如何|github|工具合集|guide\b|how\s+to|walkthrough"),
    ("business", r"变现|商业化|收款|定价|mrr|现金流|付费意愿"),
    ("ops_growth", r"曝光|阅读量|创作者收益|算法|for\s*you|限流"),
]

TWEET_DATE = "%a %b %d %H:%M:%S %z %Y"


def die(msg: str, code: int = 2) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def load_ytd(path: Path) -> list[Any]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^window\.YTD\.[^=]+=\s*", "", text, count=1)
    data = json.loads(text)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    die(f"{path.name} is not a YTD array")


def find_data_dir(archive: Path) -> Path:
    if archive.is_file() and archive.suffix.lower() == ".zip":
        die("Pass an unzipped twitter-* folder, or unzip first. Zip support is extract-to-temp.")
    if archive.is_file():
        die(f"--archive must be a folder, got file: {archive}")
    if (archive / "tweets.js").exists():
        return archive
    if (archive / "data" / "tweets.js").exists():
        return archive / "data"
    matches = list(archive.glob("twitter-*/data/tweets.js"))
    if len(matches) == 1:
        return matches[0].parent
    die(f"Cannot find data/tweets.js under {archive}")


def maybe_unzip(archive: Path, tmp: Path) -> Path:
    if not (archive.is_file() and archive.suffix.lower() == ".zip"):
        return archive
    extracted = False
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            name = Path(info.filename).name
            if name not in ALLOWED_FILES:
                continue
            target = tmp / "data" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, target.open("wb") as dst:
                dst.write(src.read())
            extracted = True
    if not extracted:
        die("Zip has no allowlisted files (tweets.js, …). Is this an official Archive?")
    return tmp


def parse_tweet_date(value: str) -> datetime:
    return datetime.strptime(value, TWEET_DATE)


def classify(text: str) -> str:
    lowered = text.lower()
    for name, pat in THEME_RULES:
        if re.search(pat, lowered, re.I):
            return name
    stripped = text.strip()
    if len(stripped) <= 8 or (stripped.startswith("@") and len(stripped) < 40):
        return "short_reply"
    return "other"


def clip(text: str, limit: int) -> str:
    one_line = re.sub(r"\s+", " ", text).strip()
    return one_line if len(one_line) <= limit else one_line[: limit - 1] + "…"


def first_article_title(article: dict[str, Any]) -> str:
    title = (article.get("title") or "").strip()
    if title:
        return title[:80]
    for block in article.get("content", {}).get("blocks", []):
        text = (block.get("text") or "").strip()
        if text:
            return text[:80]
    return str(article.get("id") or "")


def unwrap(rows: list[Any], key: str) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if isinstance(row, dict) and key in row and isinstance(row[key], dict):
            out.append(row[key])
        elif isinstance(row, dict):
            out.append(row)
    return out


def safe_account(data_dir: Path) -> dict[str, Any]:
    account: dict[str, Any] = {}
    if (data_dir / "account.js").exists():
        raw = unwrap(load_ytd(data_dir / "account.js"), "account")
        if raw:
            src = raw[0]
            account = {
                "username": src.get("username"),
                "display_name": src.get("accountDisplayName"),
                "account_id": src.get("accountId"),
                "created_at": src.get("createdAt"),
            }
    if (data_dir / "profile.js").exists():
        raw = unwrap(load_ytd(data_dir / "profile.js"), "profile")
        if raw:
            desc = raw[0].get("description") or {}
            account["bio"] = desc.get("bio") or ""
            account["website"] = desc.get("website") or ""
    if (data_dir / "professional-data.js").exists():
        raw = unwrap(load_ytd(data_dir / "professional-data.js"), "professionalData")
        if raw:
            src = raw[0]
            account["professional_type"] = src.get("professionalType")
            cats = src.get("categories") or []
            if isinstance(cats, dict):
                cats = [cats]
            account["categories"] = [
                c.get("categoryName") for c in cats if isinstance(c, dict) and c.get("categoryName")
            ]
    if (data_dir / "screen-name-change.js").exists():
        changes = []
        for row in unwrap(load_ytd(data_dir / "screen-name-change.js"), "screenNameChange"):
            inner = row.get("screenNameChange") or row
            changes.append(
                {
                    "changed_at": inner.get("changedAt"),
                    "from": inner.get("changedFrom"),
                    "to": inner.get("changedTo"),
                }
            )
        account["screen_name_changes"] = changes
    return account


def load_notes(data_dir: Path) -> dict[str, str]:
    path = data_dir / "note-tweet.js"
    if not path.exists():
        return {}
    notes = {}
    for row in unwrap(load_ytd(path), "noteTweet"):
        nid = str(row.get("noteTweetId") or "")
        text = ((row.get("core") or {}).get("text")) or ""
        if nid and text:
            notes[nid] = text
    return notes


def attach_note(tweet: dict[str, Any], notes: dict[str, str]) -> str:
    text = tweet.get("full_text") or tweet.get("text") or ""
    tid = str(tweet.get("id_str") or tweet.get("id") or "")
    if tid in notes:
        return notes[tid]
    for nid, ntext in notes.items():
        if tid and (nid.startswith(tid[:10]) or tid.startswith(nid[:10])):
            return ntext
    return text


def summarize_posts(data_dir: Path, text_limit: int) -> dict[str, Any]:
    tweets = unwrap(load_ytd(data_dir / "tweets.js"), "tweet")
    notes = load_notes(data_dir)
    originals, replies, retweets, quotes = [], [], [], []
    monthly: Counter[str] = Counter()
    monthly_orig: Counter[str] = Counter()
    daily: Counter[str] = Counter()
    langs: Counter[str] = Counter()
    themes_orig: Counter[str] = Counter()
    orig_rows = []
    flagged = []

    for tw in tweets:
        created = parse_tweet_date(tw["created_at"])
        month = created.strftime("%Y-%m")
        day = created.strftime("%Y-%m-%d")
        monthly[month] += 1
        daily[day] += 1
        text = attach_note(tw, notes)
        is_rt = text.startswith("RT @") or bool(tw.get("retweeted_status"))
        is_reply = bool(tw.get("in_reply_to_status_id_str"))
        is_quote = bool(tw.get("is_quote_status")) and not is_reply
        if is_rt:
            retweets.append(tw)
            kind = "retweet"
        elif is_reply:
            replies.append(tw)
            kind = "reply"
        elif is_quote:
            quotes.append(tw)
            kind = "quote"
        else:
            originals.append(tw)
            monthly_orig[month] += 1
            kind = "original"
        langs[tw.get("lang") or "?"] += 1
        theme = classify(text)
        if kind == "original":
            themes_orig[theme] += 1
            row = {
                "id": tw.get("id_str"),
                "date": created.isoformat(),
                "fav": int(tw.get("favorite_count") or 0),
                "rt": int(tw.get("retweet_count") or 0),
                "theme": theme,
                "text": clip(text, text_limit),
            }
            orig_rows.append(row)
            if theme in {"growth_follow", "adult"}:
                flagged.append(row)

    orig_rows.sort(key=lambda x: (-x["fav"], -x["rt"]))
    by_month_theme: dict[str, Counter[str]] = defaultdict(Counter)
    for row in orig_rows:
        by_month_theme[row["date"][:7]][row["theme"]] += 1

    articles = []
    if (data_dir / "article.js").exists():
        for article in unwrap(load_ytd(data_dir / "article.js"), "article"):
            articles.append({"id": article.get("id"), "title": first_article_title(article)})

    article_meta = []
    if (data_dir / "article-metadata.js").exists():
        for meta in unwrap(load_ytd(data_dir / "article-metadata.js"), "articleMetadata"):
            ms = meta.get("firstPublishedAtMs") or meta.get("createdAtMs")
            published = (
                datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).isoformat() if ms else None
            )
            lifecycle = ((meta.get("lifecycleState") or {}).get("lifecycle") or {}).get("name")
            article_meta.append(
                {"tweet_id": meta.get("tweetId"), "date": published, "state": lifecycle}
            )

    deleted = 0
    if (data_dir / "deleted-tweets.js").exists():
        deleted = len(load_ytd(data_dir / "deleted-tweets.js"))

    followers = len(load_ytd(data_dir / "follower.js")) if (data_dir / "follower.js").exists() else 0
    following = len(load_ytd(data_dir / "following.js")) if (data_dir / "following.js").exists() else 0
    likes = len(load_ytd(data_dir / "like.js")) if (data_dir / "like.js").exists() else 0

    total = len(tweets)
    high_volume_days = [{"date": d, "count": n} for d, n in daily.most_common() if n >= 20][:10]
    days_with_posts = max(len(daily), 1)

    return {
        "followers_in_export": followers,
        "following_in_export": following,
        "likes_given_in_export": likes,
        "counts": {
            "tweets": total,
            "originals": len(originals),
            "replies": len(replies),
            "quotes": len(quotes),
            "retweets": len(retweets),
            "note_tweets": len(notes),
            "articles": len(articles),
            "deleted_tweets": deleted,
        },
        "reply_ratio": round(len(replies) / total, 4) if total else 0,
        "original_ratio": round(len(originals) / total, 4) if total else 0,
        "avg_posts_per_active_day": round(total / days_with_posts, 2),
        "avg_originals_per_active_day": round(len(originals) / days_with_posts, 2),
        "monthly": dict(sorted(monthly.items())),
        "monthly_originals": dict(sorted(monthly_orig.items())),
        "monthly_original_themes": {k: v.most_common() for k, v in sorted(by_month_theme.items())},
        "themes_originals": themes_orig.most_common(),
        "langs": langs.most_common(),
        "zero_like_originals": sum(1 for r in orig_rows if r["fav"] == 0),
        "originals_with_likes": sum(1 for r in orig_rows if r["fav"] > 0),
        "high_volume_days": high_volume_days,
        "top_originals_by_likes": orig_rows[:15],
        "recent_originals": sorted(orig_rows, key=lambda x: x["date"], reverse=True)[:12],
        "flagged_originals": flagged[:20],
        "articles": articles,
        "article_meta": article_meta,
    }


def parse_uth(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    if not path.exists():
        die(f"UTH file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        die("UTH file must be a JSON object")
    labels = data.get("postLabels") or []
    account_labels = data.get("accountLabels") or []
    return {
        "period": data.get("period"),
        "generated_at": data.get("generatedAt"),
        "post_count": data.get("postCount"),
        "account_labels": account_labels,
        "total_account_labels": data.get("totalAccountLabels", len(account_labels)),
        "post_labels": [
            {
                "label": item.get("label"),
                "posts": item.get("posts"),
                "percentage": item.get("percentageOfPosts"),
                "effect": item.get("effect"),
            }
            for item in labels
            if isinstance(item, dict)
        ],
    }


def build_signals(account: dict[str, Any], posts: dict[str, Any], uth: dict[str, Any] | None) -> dict[str, Any]:
    followers = posts.get("followers_in_export") or 0
    following = posts.get("following_in_export") or 0
    ratio = round(followers / following, 3) if following else None
    uth_account = (uth or {}).get("account_labels") or []
    post_labels = (uth or {}).get("post_labels") or []

    def label_count(name: str) -> int:
        for item in post_labels:
            if item.get("label") == name:
                try:
                    return int(item.get("posts") or 0)
                except (TypeError, ValueError):
                    return 0
        return 0

    themes = dict(posts.get("themes_originals") or [])
    return {
        "account_labels_present": bool(uth_account),
        "account_label_names": [
            (x.get("label") if isinstance(x, dict) else str(x)) for x in uth_account
        ],
        "nsfw_high_precision_posts": label_count("NSFW_HIGH_PRECISION"),
        "nsfw_high_recall_posts": label_count("NSFW_HIGH_RECALL"),
        "spam_high_recall_posts": label_count("SPAM_HIGH_RECALL"),
        "reply_heavy": posts.get("reply_ratio", 0) >= 0.6,
        "follow_graph_near_reciprocal": bool(ratio is not None and 0.7 <= ratio <= 1.3 and following >= 200),
        "follow_ratio": ratio,
        "growth_follow_originals": themes.get("growth_follow", 0),
        "adult_keyword_originals": themes.get("adult", 0),
        "high_volume_day_count": len(posts.get("high_volume_days") or []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize local X Archive + Under the Hood files")
    parser.add_argument("--archive", required=True, help="Unzipped twitter-* folder, or its data/ folder")
    parser.add_argument("--uth", help="Under the Hood JSON export")
    parser.add_argument("--out", help="Write sanitized JSON here. Default: stdout")
    parser.add_argument("--text-limit", type=int, default=180)
    args = parser.parse_args()

    archive = Path(args.archive).expanduser().resolve()
    uth_path = Path(args.uth).expanduser().resolve() if args.uth else None

    with TemporaryDirectory() as tmp:
        root = maybe_unzip(archive, Path(tmp))
        data_dir = find_data_dir(root)
        account = safe_account(data_dir)
        posts = summarize_posts(data_dir, args.text_limit)
        uth = parse_uth(uth_path)
        followers = posts.pop("followers_in_export")
        following = posts.pop("following_in_export")
        likes_given = posts.pop("likes_given_in_export")
        account = {
            **account,
            "followers": followers,
            "following": following,
            "likes_given": likes_given,
        }
        summary = {
            "privacy": {
                "read_only": sorted(ALLOWED_FILES),
                "never_read": [
                    "direct-messages.js",
                    "email-address-change.js",
                    "phone-number.js",
                    "ip-audit.js",
                    "account-creation-ip.js",
                    "grok-chat-item.js",
                    "sso.js",
                    "contact.js",
                ],
                "note": "Do not upload this JSON. It still contains public post snippets.",
            },
            "account": account,
            "uth": uth,
            "posts": posts,
            "signals": build_signals(
                account,
                {
                    **posts,
                    "followers_in_export": followers,
                    "following_in_export": following,
                },
                uth,
            ),
        }

    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.out:
        out = Path(args.out).expanduser().resolve()
        out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    counts = summary["posts"]["counts"]
    print(
        json.dumps(
            {
                "username": summary["account"].get("username"),
                "tweets": counts["tweets"],
                "originals": counts["originals"],
                "replies": counts["replies"],
                "reply_ratio": summary["posts"]["reply_ratio"],
                "uth_account_labels": summary["signals"]["account_label_names"],
            },
            ensure_ascii=False,
        ),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
