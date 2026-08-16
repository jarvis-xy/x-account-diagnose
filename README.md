# x-account-diagnose

[中文](#中文) · [English](#english)

本机诊断 X 账号的 Agent Skill。你下载两份官方数据，交给 Cursor / Claude Code / Codex。文件只在你的电脑上读取，不会上传。

A local Agent Skill for diagnosing an X account. Download two official exports, hand them to Cursor / Claude Code / Codex. Files stay on your machine.

---

## 中文

你从 X 下载两份官方数据，交给 Agent。它在本地读完，输出一篇排好版的诊断报告：

1. 账号有没有被限制推荐
2. 个人简介和实际内容对不对得上
3. 下一步只改一件事——停掉那个和 X 开源推荐规则相违背的动作

不上传账号数据包。不上传 Under the Hood。不保证涨粉。

### 你要准备的两份文件

1. **账号数据包（Archive）**  
   X → 设置 → 你的账号 → 下载你的数据归档。解压后应有 `data/tweets.js`。
2. **Under the Hood 月报**  
   打开 [x.com/i/under_the_hood](https://x.com/i/under_the_hood)，导出最近一个完整自然月的 JSON。

数据包里还有私信、邮箱、IP。不要发给陌生人，也不要丢进网页版「诊断工具」。这个 Skill 的脚本只读推文和公开资料，不读私信。

### 安装

```bash
git clone https://github.com/jarvis-xy/x-account-diagnose.git

# Cursor
cp -R x-account-diagnose ~/.cursor/skills/x-account-diagnose

# Claude Code
cp -R x-account-diagnose ~/.claude/skills/x-account-diagnose

# Codex
cp -R x-account-diagnose "${CODEX_HOME:-$HOME/.codex}/skills/x-account-diagnose"
```

也可以不拷贝，直接在对话里写：`用 /path/to/x-account-diagnose 这份 skill`。

### 使用

对 Agent 说：

```text
用 x-account-diagnose 诊断这个号。
Archive：/path/to/twitter-2026-08-15-...
UTH：/path/to/x-under-the-hood.json
```

它会先跑：

```bash
python3 scripts/summarize.py \
  --archive /path/to/twitter-2026-08-15-... \
  --uth /path/to/x-under-the-hood.json \
  --out /tmp/x-account-summary.json
```

`--archive` 也可以是官方 zip。脚本只会从压缩包里抽出允许的文件，不会解压私信。

然后按 `references/report-template.md` 写成中文报告。英文用户用 `references/report-template.en.md`。

### 报告里有什么

- **账号有没有被限制推荐**：整个账号的标签、单条帖子的成人 / 垃圾信息标签、回复别人评论的占比、单日有没有连发
- **个人简介和实际内容对不对得上**：简介写了什么，原创帖实际在写什么
- **下一步建议**：只改一件和 X 开源推荐规则相违背的事

权重对照 [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)。别人复制你帖子链接的默认权重是 20，点赞只有 0.5。数字以你这份导出和当前代码为准。

### 不会做的事

- 不代发帖
- 不写互关、刷回复、规避平台规则
- 不承诺粉丝、阅读或创作者分成
- 不把数据包上传到任何服务器

---

## English

A local Agent Skill. You download two official X exports and give them to Cursor / Claude Code / Codex. The skill reads the files on your machine and writes a formatted report:

1. Whether the account or some posts are restricted from recommendations
2. Whether the profile bio matches what you actually post
3. One change for this month — stop the habit that goes against X's open-source ranking rules

No upload. No promised follower growth.

### The two files you need

1. **Account archive**  
   X → Settings → Your account → Download an archive of your data. After unzipping you should see `data/tweets.js`.
2. **Under the Hood monthly report**  
   Open [x.com/i/under_the_hood](https://x.com/i/under_the_hood) and export JSON for the latest full calendar month.

The archive also contains DMs, email, and IPs. Do not send it to anyone. Do not upload it to a website "diagnosis tool". This skill only reads posts and public profile fields.

### Install

```bash
git clone https://github.com/jarvis-xy/x-account-diagnose.git

# Cursor
cp -R x-account-diagnose ~/.cursor/skills/x-account-diagnose

# Claude Code
cp -R x-account-diagnose ~/.claude/skills/x-account-diagnose

# Codex
cp -R x-account-diagnose "${CODEX_HOME:-$HOME/.codex}/skills/x-account-diagnose"
```

Or skip the copy and tell the agent: `use the skill at /path/to/x-account-diagnose`.

### Use

```text
Use x-account-diagnose on this account.
Archive: /path/to/twitter-2026-08-15-...
UTH: /path/to/x-under-the-hood.json
```

The agent runs:

```bash
python3 scripts/summarize.py \
  --archive /path/to/twitter-2026-08-15-... \
  --uth /path/to/x-under-the-hood.json \
  --out /tmp/x-account-summary.json
```

`--archive` can also be the official zip. The script extracts allowlisted files only. It does not unpack DMs.

English reports follow `references/report-template.en.md`.

### What the report contains

- **Are recommendations restricted?** Account labels, adult/spam post labels, share of replies, same-day posting volume
- **Does the bio match the posts?** Profile bio vs what originals actually say
- **What to change next** One action that goes against X's open-source ranking rules

Weights come from [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm). Copy-link defaults to 20; like is 0.5. Recheck the repo before treating a weight as current.

### What this will not do

- Post on your behalf
- Suggest follow-for-follow, reply spam, or evasion
- Promise followers, views, or creator payouts
- Upload your archive anywhere

---

## Develop

```bash
python3 scripts/summarize.py \
  --archive fixtures/archive-mini \
  --uth fixtures/uth-sample.json
```

Python 3.10+, no third-party dependencies.
