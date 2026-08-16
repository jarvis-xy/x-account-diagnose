---
name: x-account-diagnose
description: Diagnoses an X/Twitter account from the official Archive and Under the Hood export. An agent reads the two local files, never uploads them, and writes a formatted report covering recommendation limits, whether the profile bio matches the posts, and creation advice aligned with X's open-source ranking rules. Use when the user mentions X account diagnosis, Under the Hood, twitter archive, 账号诊断, 限流, 账号画像, x-account-diagnose, or wants a repeatable local report from X exports.
---

# X Account Diagnose

Read two official local exports, summarize them with the bundled script, then write one formatted report. This is for ongoing diagnosis, not a one-off guess about follower growth. Do not invent a second workflow.

Required inputs:

1. X account archive: `twitter-*.zip` or the unzipped `twitter-*/` folder
2. Under the Hood JSON: exported from `x.com/i/under_the_hood`

If either file is missing, stop and tell the user how to export it. See [references/export-guide.md](references/export-guide.md).

## Privacy

The official archive contains DMs, emails, IPs, phone numbers, and Grok chats.

- Run `scripts/summarize.py`. Do not open the archive by hand.
- Never read or quote: `direct-messages*.js`, `email-address-change.js`, `phone-number.js`, `ip-audit.js`, `account-creation-ip.js`, `grok-chat-item.js`, `sso.js`, `contact.js`
- Never write email, phone, IP, DM text, or login history into the report
- Never upload the archive, the UTH file, or the summary JSON
- Anyone who asks the user to upload the zip to a stranger's website should not be trusted

## Workflow

```
Task Progress:
- [ ] Locate Archive + UTH
- [ ] Run scripts/summarize.py
- [ ] Read the summary JSON only
- [ ] Write the formatted report from the template
- [ ] Give the user one next action
```

### 1. Locate files

Ask for both paths if the user did not give them. Accept:

- Archive: zip, `twitter-*` folder, or the inner `data/` folder
- UTH: `.json` from Under the Hood

If the user also pastes a bio, treat it as the **profile bio**, not as proven positioning. Check it against original posts.

### 2. Summarize locally

From this skill directory:

```bash
python3 scripts/summarize.py \
  --archive /path/to/twitter-YYYY-MM-DD-... \
  --uth /path/to/x-under-the-hood.json \
  --out /tmp/x-account-summary.json
```

The script only loads an allowlist. It prints counts and writes a sanitized JSON. If it errors, fix the path; do not start reading `data/*.js` yourself.

### 3. Read the summary

Open the JSON produced by the script. Use:

- `account` for handle, bio, follow counts
- `uth` for account labels and post labels
- `posts` for reply ratio, monthly mix, themes, top originals
- `signals` for first-pass flags

For label meanings and ranking weights, read [references/labels.md](references/labels.md) and [references/algorithm.md](references/algorithm.md).

UTH usually covers one calendar month. Do not use that month's account labels to judge later posts that only appear in the Archive.

### 4. Write the report

Write in the user's language.

- Chinese: copy [references/report-template.md](references/report-template.md)
- English: copy [references/report-template.en.md](references/report-template.en.md)

Keep the heading names, horizontal rules, and table layout. Fill every section with numbers from this export. Do not use another account's numbers.

The report must contain:

1. **账号有没有被限制推荐** — account labels first, then post labels, then posting habits that go against X's open-source ranking rules
2. **个人简介和实际内容对不对得上** — profile bio vs what originals actually say, by month; name the split if there is one
3. **下一步创作建议** — optimization direction and correction rules, grounded in X's open-source ranking. One primary change; two secondary tests max

Also include a short "how to run this again" so the user can repeat the diagnosis next month.

### 5. Plain language

Write as if explaining to a creator who has never opened the algorithm repo. Prefer a short everyday sentence over a compact jargon phrase.

| Do not write | Write this instead |
|---|---|
| 声称的定位 / claimed positioning | 账号个人简介 / profile bio |
| 回复当主业 | 把回复别人评论当成主要运营动作 |
| 和公式拧着 / 停掉和公式拧着的那一件事 | 避免和 X 开源推荐规则相违背的动作 |
| 整号限流 | 整个账号被限制推荐 |
| 主粮 | 这个月主要在发什么 |
| 定罪 | 不能用这份月报判断其他月份 |
| 站外 | 没关注你的人那边 |
| 聚合 | 单帖标签攒多了，可能变成整个账号的限制 |
| 不另起玄学 / 不另搞一套说不清的方法 | 不另搞一套摸不清的方法 |
| 下一步建议 / 优化建议 | 下一步创作建议 |

First time you mention For You, write: 推荐页（没关注你的人也能刷到）. After that, 推荐页 is enough.

Call the archive **X账号数据包**. Call the ranking source **X 在 GitHub 上开源的 x-algorithm**.

Full glossary: [references/writing.md](references/writing.md).

Do not dump raw label IDs without a one-line meaning. Example: `NSFW_HIGH_PRECISION` → 系统较有把握判定为成人内容，没关注你的人刷不到，还会加警告。

### 6. Quality bar

Good report:

- Opens with a verdict in 3 sentences
- Every claim has a count, date range, or label name
- Distinguishes "the whole account is blocked from recommendations" from "some posts are hidden"
- Helps the reader see the account's portrait on the platform
- Does not recommend mutual-follow content, reply spam, or evasion
- Does not promise followers, impressions, or creator payouts
- Uses 更可能 / 值得测试, not 一定 / 保证
- Looks like a finished document: title, meta table, horizontal rules, no leftover `[brackets]`

Bad report:

- Calls a quiet account "shadowbanned" when `accountLabels` is empty
- Treats likes as recommendation score (like weight is 0.5; copy-link is 20)
- Dumps 50 tweet texts
- Turns the advice into a growth course
- Leaves template placeholders or unformatted JSON in the markdown

## Defaults

- Save a markdown file if the user wants it kept. Default name: `x-diagnose-YYYY-MM-DD.md` next to the UTH file, or wherever they ask
- Status is a draft they can edit. Do not post it to X
- Weights in `references/algorithm.md` are a snapshot. If they may be stale, say so and point to [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)
- Suggested agents, in this order: Claude Code, Codex, Cursor
