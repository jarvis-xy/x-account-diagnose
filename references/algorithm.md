# Open-source ranking notes

Source: [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm), mainly `home-mixer/params/param.rs` and visibility-filtering. Snapshot used when this skill was written: 2026-08. Re-check the repo before treating a weight as current.

Default weights multiply the predicted probability of an action. They are not "1 report = 468 likes".

| Predicted action | Default weight | Say this in the report |
|---|---|---|
| Copy link and share | 20.0 | 别人愿意复制链接转发出去的教程、清单、长文 |
| Reply / quote | 5.0 | 能讨论的实操，不是报数字 |
| Follow author | 4.0 | 个人简介和内容一致，人才会粉 |
| Share | 2.0 | — |
| Repost | 1.0 | — |
| Like | 0.5 | 涨粉日记容易收赞，但不等于推荐分高 |
| Open a link | 0.2 | 主帖只丢一个链接，分偏弱 |
| Report | -234.0 | 乘的是「会不会被举报」的预测，不是举报次数 |

Other rules that show up in real accounts:

- Replies shown to people who do not follow you are rescored by `OonWeightFactor = 0.75`
- Same-author posts the same day: next post × 0.5, floor 0.25
- Replies between mutual follows get an extra boost. That looks like reach; it is still your existing circle
- Posts older than 48 hours drop out of pre-scoring. No long tail
- Empty account labels: ordinary posts can still enter the recommendation feed for people who do not follow you

## How to use this

If likes are high and copy/reply is low, say the ranking rules are not on this posting habit's side.

If reply ratio ≥ 60%, treat "把回复别人评论当成主要运营动作" as the default mismatch.

If following ≈ followers and both are large, mention the follow graph looks reciprocal. Do not tell them to mass-unfollow this week unless they ask. Account health is labels + original posts, not a cosmetic ratio.
