# Report template (English)

Keep this layout. Remove every `[bracket]`. Do not leave template voice. Keep the title, rules, and tables.

The first time you mention For You, write: "For You (the recommendation feed shown to people who do not follow you)".

```markdown
# Account diagnosis: @handle

> Draft · Generated on this machine · Your archive is not uploaded

| Item | Detail |
|---|---|
| Account | @[handle] |
| Archive | [start] to [end], [N] posts |
| Monthly report | Under the Hood, [YYYY-MM], [N] posts |
| Ranking reference | [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) ([date] snapshot) |

---

## Verdict

[Three sentences.]

1. Can the whole account still appear in the recommendation feed for people who do not follow you?
2. Are a few posts hidden, or is the whole account restricted?
3. Which daily habit goes against X's open-source ranking rules?

---

## 1. Are recommendations restricted?

### The whole account

- Account labels: [none / list names in plain language]
- What this means: [ordinary posts can still be recommended to non-followers / the whole account is kept out of that feed]

### Individual posts ([UTH month] only)

| Label | Plain meaning | Count | Share | Visible to non-followers? |
|---|---|---|---|---|
| … | … | … | … | … |

Matching originals in the same month: [adult content / follow-for-follow copy / link spam / not clear — do not force a match]

The monthly report does not include post IDs. Do not name individual posts unless the archive makes the match obvious.

### Posting habits

| Item | Number | How to read it |
|---|---|---|
| Replies to other people | [n] / [total] ([xx%]) | Above 60% usually means replies are the main daily work |
| Days with ≥20 posts | [n] days, peak [n] on [date] | Same-day posts after the first one are scored lower |
| Followers / following | [n] / [n] | A near 1:1 graph looks reciprocal, not one-way attention |
| Follower-count diary originals | [n] | Posts about how many followers you gained today |
| Adult-keyword originals | [n] | Posts that sit near the adult-content policy |
| Originals with likes | [n] with likes / [n] with zero | Likes are not the same as recommendation score |

This monthly report only covers [UTH month]. Do not use these account labels to judge posts from [later month].

---

## 2. Does the profile bio match the posts?

### Profile bio

> [bio]

### What original posts are actually about

Count each original once.

| Type | Count | Notes |
|---|---|---|
| … | … | … |

### By month

| Month | All posts | Originals | What this month mostly posted |
|---|---|---|---|
| … | … | … | … |

### What readers are likely to remember

The most-liked originals reward: [tutorials / jokes / follower-count updates / product]

Match with the profile bio: [yes / it matched earlier, then drifted / it never matched]

---

## 3. What to change next

No vague extra playbook. No follow-for-follow. No promised growth.

### Change only one thing this month

[One sentence. It must point back to a number above. Name the habit that goes against X's open-source ranking rules.]

### Two smaller tests

1. [ ]
2. [ ]

### Do not do this

- Follow-for-follow or like-for-like
- Keep treating replies as the main daily work
- Keep posting the kind of content that already received restriction labels
- Upload the archive to a website "diagnosis tool"

### How to check next time

Export next month's Under the Hood and look only at: [whether an account-level adult or spam label was added]. Also check whether the share of replies went down in a new archive.

---

## How to run this again

1. Download a fresh archive and the latest full-month Under the Hood export
2. `python3 scripts/summarize.py --archive … --uth … --out summary.json`
3. Give both file paths to an agent that has x-account-diagnose installed
```
