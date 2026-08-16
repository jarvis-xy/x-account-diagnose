# 报告模板

Replace every bracket. Delete unused bullets. Keep the heading names.

```markdown
# X 账号诊断：[@handle]

数据：官方 Archive（[start] 至 [end]，[N] 条）+ Under the Hood（[month]，[N] 帖）
权重对照：[xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)（[date] 快照）
状态：draft。数字以这次导出为准。

## 先说结论

[3 句。先回答：整号还能不能进非粉丝 For You。再回答：被藏的是帖还是号。最后点出和打分公式拧着的那一件事。]

## 1. 风险识别

### 账号级

- 账号标签：[空 / 列出名字]
- 含义：[仍可推荐给非粉丝 / 非粉丝 For You 已受限]

### 帖子级（仅 [UTH month]）

| 标签 | 条数 | 占比 | 对非粉丝 For You |
|---|---|---|---|
| … | … | … | … |

Archive 里同月对得上的方向：[成人 / 互关话术 / 外链刷屏 / 看不出来，不要硬钉]

### 行为风险

- 回复占比：[xx%]（[replies]/[total]）
- 单日 ≥20 条的天数：[n]，最高一天 [n] 条
- 关注结构：关注者 [n] / 正在关注 [n]
- 增长日记原创：[n]；成人关键词原创：[n]

UTH 覆盖 [month]。[later month] 的帖不能用这份账号标签定罪。

## 2. 定位梳理

声称的定位（简介或用户自述）：

> [bio]

原创实际在写什么（一条只算一次）：

| 类型 | 条数 | 说明 |
|---|---|---|
| … | … | … |

按月：

| 月 | 全部 | 原创 | 这个月的主粮 |
|---|---|---|---|
| … | … | … | … |

带赞的原创在奖励什么：[教程 / 段子 / 涨粉数字 / 产品]

和简介是否同一条线：[是 / 6 月是、后来偏了 / 从未对齐]

## 3. 优化建议

不另起玄学，不写互关，不保证涨粉。

**本月只改一件事：** [一句话，必须能对照上面的数字]

值得测试的两件次要事：

1. [ ]
2. [ ]

不要做：[互关、回复当主业、继续发已打标的那类内容]

下一次验证：下月初再导一份 UTH，只看 [账号级 NSFW/Spam 有没有加上 / 回复占比有没有降]。

## 怎么复跑

1. 更新 Archive 和最近一个整月的 UTH
2. `python3 scripts/summarize.py --archive … --uth … --out summary.json`
3. 把两份路径交给装了 x-account-diagnose 的 Agent
```
