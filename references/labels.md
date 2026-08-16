# Under the Hood labels

Read the export first. These notes explain the common labels. Official text lives on the JSON `about` / `effect` fields and [x-reach-limited](https://help.x.com/rules-and-policies/x-reach-limited).

## Account labels

Empty `accountLabels` means the account can still be recommended to non-followers, as long as the individual post is clean.

If any of these appear at account level, say so in the first paragraph:

| Label | Meaning for the report |
|---|---|
| `DoNotAmplify` | Account is kept out of non-follower For You |
| Account-level NSFW | Discovery via adult-author filters can drop for all posts |
| Account-level Spam | Non-follower recommendation is restricted |

Post labels can later aggregate onto the account (`safety-label-user-agg` in x-algorithm). A quiet month with many NSFW post labels is a warning, not yet an account ban.

## Post labels

UTH does not give post IDs. Count them, then look in the Archive for matching originals in that same month.

| Label | Typical effect |
|---|---|
| `NSFW_HIGH_PRECISION` | Warning; hidden from non-follower recommendations; hidden from underage / no-age / logged-out |
| `NSFW_HIGH_RECALL` | Hidden from non-follower recommendations and protected audiences |
| `SPAM_HIGH_RECALL` | Hidden from non-follower recommendations; followers can still see it |

Do not call this "shadowban". Say: some posts are out of non-follower For You.

## Date mismatch

If Archive has August posts and UTH is July, write:

> 账号级结论只对 7 月负责。8 月的帖不在这份月报里。
