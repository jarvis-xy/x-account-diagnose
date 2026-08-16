# Under the Hood labels

Read the export first. These notes explain the common labels. Official text lives on the JSON `about` / `effect` fields and [x-reach-limited](https://help.x.com/rules-and-policies/x-reach-limited).

In the report, always add a plain-language meaning next to the raw label.

## Account labels

Empty `accountLabels` means the whole account can still appear in the recommendation feed for people who do not follow you, as long as the individual post is clean.

If any of these appear at account level, say so in the first paragraph:

| Label | Say this in the report |
|---|---|
| `DoNotAmplify` | 整个账号不会出现在没关注你的人的推荐页 |
| Account-level NSFW | 账号被当成成人向作者，所有帖都更难被没关注你的人刷到 |
| Account-level Spam | 整个账号对没关注你的人限制推荐 |

Post labels can later pile up onto the account (`safety-label-user-agg` in x-algorithm). Many adult post labels in one month is a warning, not yet an account-wide ban.

## Post labels

UTH does not give post IDs. Count them, then look in the Archive for matching originals in that same month.

| Label | Plain meaning |
|---|---|
| `NSFW_HIGH_PRECISION` | 系统较有把握判定为成人内容：加警告；没关注你的人刷不到 |
| `NSFW_HIGH_RECALL` | 系统怀疑是成人内容：没关注你的人刷不到 |
| `SPAM_HIGH_RECALL` | 系统怀疑是垃圾信息：没关注你的人刷不到，粉丝仍看得到 |

Do not call this "shadowban". Say: some posts are hidden from people who do not follow you.

## Date mismatch

If Archive has August posts and UTH is July, write:

> 这份月报只覆盖 7 月。8 月的帖不在里面，不能用 7 月的账号标签判断 8 月。
