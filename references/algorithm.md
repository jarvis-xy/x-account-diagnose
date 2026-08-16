# Open-source For You notes

Source: [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm), mainly `home-mixer/params/param.rs` and visibility-filtering. Snapshot used when this skill was written: 2026-08. Re-check the repo before treating a weight as current.

Default weights multiply the predicted probability of an action. They are not "1 report = 468 likes".

| Predicted action | Default weight | Use in the report |
|---|---|---|
| Copy link and share | 20.0 | Tutorials, checklists, saveable long posts |
| Reply / quote | 5.0 | Posts that start a discussion |
| Follow author | 4.0 | Clear positioning |
| Share | 2.0 | — |
| Repost | 1.0 | — |
| Like | 0.5 | Follower-count diaries can farm likes and still score poorly |
| Open a link | 0.2 | A main post that is only a t.co is weak |
| Report | -234.0 | Predicted probability, not a raw count |

Other rules that show up in real accounts:

- Replies and reposts to people who do not follow the author are rescored by `OonWeightFactor = 0.75`
- Same-author posts the same day: next post × 0.5, floor 0.25
- Mutual-follow replies get an extra boost. That looks like reach; it is in-network
- Posts older than 48 hours drop out of pre-scoring. No long tail
- Empty account labels: ordinary posts can still enter non-follower For You

## How to use this

If likes are high and copy/reply is low, say the scorer is not on the author's side.

If reply ratio ≥ 60%, treat "replies as the main product" as the default mismatch.

If following ≈ followers and both are large, mention the follow graph looks reciprocal. Do not tell them to mass-unfollow this week unless they ask. Account health is labels + originals, not a cosmetic ratio.
