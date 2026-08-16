# x-account-diagnose

本机诊断 X 账号的 Agent Skill。

你从 X 下载两份官方数据，交给 Cursor / Claude Code / Codex。Skill 只在本地读文件，输出一篇报告：风险、定位、下一步只改一件事。

不上传 Archive。不上传 Under the Hood。不保证涨粉。

## 你要准备的两份文件

1. **账号数据包（Archive）**  
   X → 设置 → 你的账号 → 下载你的数据归档。解压后应有 `data/tweets.js`。
2. **Under the Hood 月报**  
   打开 [x.com/i/under_the_hood](https://x.com/i/under_the_hood)，导出最近一个完整自然月的 JSON。

数据包里还有私信、邮箱、IP。不要发给陌生人，也不要丢进网页版「诊断工具」。这个 Skill 的脚本只读推文和公开资料，不读私信。

## 安装

克隆后，把整个目录拷到 Agent 能发现的 skills 目录：

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

## 使用

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

然后只读这份摘要，写成报告。报告结构见 `references/report-template.md`。

## 报告里有什么

- **风险识别**：账号级标签、帖子级 NSFW/Spam、回复占比、单日连发、关注结构
- **定位梳理**：简介声称的定位 vs 原创实际在写什么
- **优化建议**：只改一件和开源打分公式拧着的事

权重对照 [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)。复制链接默认权重 20，赞是 0.5。数字以你这份导出和当前代码为准。

## 不会做的事

- 不代发帖
- 不写互关、刷回复、规避平台规则
- 不承诺粉丝、阅读或创作者分成
- 不把数据包上传到任何服务器

## 开发

```bash
python3 scripts/summarize.py \
  --archive fixtures/archive-mini \
  --uth fixtures/uth-sample.json
```

需要 Python 3.10+，无第三方依赖。
