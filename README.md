# x-account-diagnose

[中文](#中文) · [English](#english)

让 AI 在本机拆你的 X 账号。你下载两份官方文件，交给 Claude Code、Codex 或 Cursor。文件只在你的电脑上读取，不会上传。

Let an agent diagnose your X account on your machine. Download two official files, hand them to Claude Code, Codex, or Cursor. Nothing is uploaded.

---

## 中文

X 把推荐算法开源之后，不必先猜「怎么涨粉」。把两份官方文件交给 Agent，它在本地读完，直接输出一篇排好版的诊断报告，方便你持续做账号诊断。

材料就是：

1. **X 账号数据包**
2. **Under the Hood 月报**
3. 对照 X 在 GitHub 上开源的 [x-algorithm](https://github.com/xai-org/x-algorithm)

报告包含：

1. 账号有没有被限制推荐
2. 个人简介和实际内容对不对得上
3. 下一步创作建议——结合 X 开源推荐规则，梳理优化方向和整改规则

这个 Skill 只做一件事：在你自己的电脑上读你导出的两份文件，写出报告。不是云端产品。官方数据包里有私信、邮箱、登录 IP。谁让你把 zip 上传到陌生网站，谁就不该被信任。

不写互关内容。不保证涨粉。

### 你要准备的两份文件

1. **X 账号数据包（Archive）**  
   X → 设置 → 你的账号 → 下载你的数据归档。解压后应有 `data/tweets.js`。不要截图，不要让别人代下。
2. **Under the Hood 月报**  
   打开 [x.com/i/under_the_hood](https://x.com/i/under_the_hood)，导出最近一个完整自然月的 JSON。月报只对那一个月负责。

### 安装

```bash
git clone https://github.com/jarvis-xy/x-account-diagnose.git

# Claude Code
cp -R x-account-diagnose ~/.claude/skills/x-account-diagnose

# Codex
cp -R x-account-diagnose "${CODEX_HOME:-$HOME/.codex}/skills/x-account-diagnose"

# Cursor
cp -R x-account-diagnose ~/.cursor/skills/x-account-diagnose
```

也可以不拷贝，直接告诉 Agent 仓库路径。

### 使用教程

对 Agent 说：

```text
用 x-account-diagnose 诊断这个号。
Archive：/path/to/twitter-2026-08-15-...
UTH：/path/to/x-under-the-hood.json
```

它会先在本地跑汇总脚本，只读推文和月报，不读私信。然后按模板排版，写出报告。

`--archive` 也可以是官方 zip。脚本只会从压缩包里抽出允许的文件，不会解压私信。

中文报告模板：`references/report-template.md`。英文：`references/report-template.en.md`。

### 报告里有什么

- **账号有没有被限制推荐**：整个账号有没有被打标签；哪些帖被标成成人内容或垃圾信息；你是不是把回复别人评论当成了主要运营动作；单日有没有连发到被自己挤掉
- **个人简介和实际内容对不对得上**：简介写了什么，对照原创实际在写什么，按月切开
- **下一步创作建议**：结合 X 开源推荐规则，梳理账号优化方向和整改规则

权重以 GitHub 当前代码为准。别人复制你帖子链接的默认权重是 20，点赞只有 0.5。

### 不会做的事

- 不代发帖
- 不写互关内容、不教刷回复、不帮你规避平台规则
- 不承诺粉丝、阅读或创作者分成
- 不把数据包上传到任何服务器

欢迎使用，多提建议。Issues 开在本仓库即可。

---

## English

After X open-sourced its ranking, you do not have to guess how to grow. Give an agent two official files. It reads them on your machine and writes a formatted report you can rerun every month.

The inputs are:

1. **X account archive**
2. **Under the Hood monthly report**
3. Checked against [x-algorithm](https://github.com/xai-org/x-algorithm) on GitHub

The report covers:

1. Whether recommendations are restricted
2. Whether the profile bio matches what you actually post
3. Creation advice — optimization direction and correction rules, using X's open-source ranking

This skill does one thing: read your two exports locally and write the report. It is not a cloud product. The official archive contains DMs, email, and login IPs. Anyone who asks you to upload the zip to a stranger's site should not be trusted.

No follow-for-follow copy. No promised growth.

### The two files you need

1. **X account archive**  
   X → Settings → Your account → Download an archive of your data. After unzipping you should see `data/tweets.js`. Do not use screenshots. Do not let someone else download it for you.
2. **Under the Hood**  
   Open [x.com/i/under_the_hood](https://x.com/i/under_the_hood) and export JSON for the latest full calendar month. That report only speaks for that month.

### Install

```bash
git clone https://github.com/jarvis-xy/x-account-diagnose.git

# Claude Code
cp -R x-account-diagnose ~/.claude/skills/x-account-diagnose

# Codex
cp -R x-account-diagnose "${CODEX_HOME:-$HOME/.codex}/skills/x-account-diagnose"

# Cursor
cp -R x-account-diagnose ~/.cursor/skills/x-account-diagnose
```

Or skip the copy and tell the agent the repo path.

### How to run it

```text
Use x-account-diagnose on this account.
Archive: /path/to/twitter-2026-08-15-...
UTH: /path/to/x-under-the-hood.json
```

The agent runs a local summary script. It reads posts and the monthly report, not DMs, then writes the formatted report.

`--archive` can also be the official zip. Allowlisted files only.

English template: `references/report-template.en.md`.

### What the report contains

- **Are recommendations restricted?** Account labels, adult/spam post labels, share of replies, same-day posting volume
- **Does the bio match the posts?** Profile bio vs originals, cut by month
- **Creation advice** Optimization direction and correction rules from X's open-source ranking

Copy-link defaults to 20; like is 0.5. Recheck the repo before treating a weight as current.

### What this will not do

- Post on your behalf
- Suggest follow-for-follow content, reply spam, or evasion
- Promise followers, views, or creator payouts
- Upload your archive anywhere

Issues and suggestions welcome in this repo.

---

## Develop

```bash
python3 scripts/summarize.py \
  --archive fixtures/archive-mini \
  --uth fixtures/uth-sample.json
```

Python 3.10+, no third-party dependencies.
