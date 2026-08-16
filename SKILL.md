---
name: x-account-diagnose
description: Diagnoses an X/Twitter account from the official Archive and Under the Hood export. Reads the two local files, never uploads them, and writes a report covering account risk, positioning, and one-change optimization. Use when the user mentions X account diagnosis, Under the Hood, twitter archive, 账号诊断, 限流, x-account-diagnose, or wants a local report from X exports.
---

# X Account Diagnose

Read two official local exports, summarize them with the bundled script, then write one report. Do not invent a second workflow.

Required inputs:

1. X Archive: `twitter-*.zip` or the unzipped `twitter-*/` folder
2. Under the Hood JSON: exported from `x.com/i/under_the_hood`

If either file is missing, stop and tell the user how to export it. See [references/export-guide.md](references/export-guide.md).

## Privacy

Archive packages contain DMs, emails, IPs, phone numbers, and Grok chats.

- Run `scripts/summarize.py`. Do not open the archive by hand.
- Never read or quote: `direct-messages*.js`, `email-address-change.js`, `phone-number.js`, `ip-audit.js`, `account-creation-ip.js`, `grok-chat-item.js`, `sso.js`, `contact.js`
- Never write email, phone, IP, DM text, or login history into the report
- Never upload the archive, the UTH file, or the summary JSON

## Workflow

```
Task Progress:
- [ ] Locate Archive + UTH
- [ ] Run scripts/summarize.py
- [ ] Read the summary JSON only
- [ ] Write the report from the template
- [ ] Give the user one next action
```

### 1. Locate files

Ask for both paths if the user did not give them. Accept:

- Archive: zip, `twitter-*` folder, or the inner `data/` folder
- UTH: `.json` from Under the Hood

If the user also pastes a bio or says what the account is for, keep that as claimed positioning. Do not treat it as proven until the originals match.

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

- `account` for handle, bio, follow graph
- `uth` for account labels and post labels
- `posts` for reply ratio, monthly mix, themes, top originals
- `signals` for the first-pass risk flags

For label meanings and For You weights, read [references/labels.md](references/labels.md) and [references/algorithm.md](references/algorithm.md).

UTH usually covers one calendar month. Do not apply that month's account labels to later posts that are only in the Archive.

### 4. Write the report

Copy [references/report-template.md](references/report-template.md). Write in the user's language. Fill every section with numbers from this export. Do not use another account's numbers.

The report must contain:

1. **风险识别** — account labels first, then post labels, then behavior that the open-source scorer punishes
2. **定位梳理** — claimed bio vs what originals actually say, by month; name the split if there is one
3. **优化建议** — exactly one primary change that matches the worst mismatch; two secondary changes max

Also include a 10-line "how this was done" so the user can rerun it next month.

### 5. Quality bar

Good report:

- Opens with a verdict in 3 sentences
- Every claim has a count, date range, or label name
- Distinguishes "account blocked from For You" from "some posts hidden"
- Does not recommend mutual follows, reply spam, or evasion
- Does not promise followers, impressions, or creator payouts
- Uses 更可能 / 值得测试, not 一定 / 保证

Bad report:

- Calls a quiet account "shadowbanned" when `accountLabels` is empty
- Treats likes as For You score (like weight is 0.5; copy-link is 20)
- Dumps 50 tweet texts
- Turns the advice into a growth course

## Defaults

- Output a markdown file if the user wants it saved. Default name: `x-diagnose-YYYY-MM-DD.md` next to the UTH file, or wherever they ask
- Status is a draft they can edit. Do not post it to X
- Weights in `references/algorithm.md` are a snapshot. If they may be stale, say so and point to [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)
