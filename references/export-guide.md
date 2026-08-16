# Export the two files

Do this on the user's own X account. The skill never logs in for them.

## 1. Archive

1. Open X → Settings → Your account → Download an archive of your data
2. Wait for the email, download the zip
3. Unzip it. You should see `twitter-YYYY-MM-DD-<hash>/data/tweets.js`

The zip also contains DMs, emails, and IPs. Leave it on the machine. Do not mail it, do not drop it into a web "诊断工具".

## 2. Under the Hood

1. Open [x.com/i/under_the_hood](https://x.com/i/under_the_hood)
2. Pick one full calendar month
3. Export / download the JSON

UTH is usually one month. Archive can cover many months. The report must say which month the labels belong to.

## 3. Hand both paths to the agent

Chinese:

```text
用 x-account-diagnose 诊断这个号。
Archive：/path/to/twitter-2026-08-15-...
UTH：/path/to/x-under-the-hood.json
```

English:

```text
Use x-account-diagnose on this account.
Archive: /path/to/twitter-2026-08-15-...
UTH: /path/to/x-under-the-hood.json
```

## Missing files

| Missing | What to say |
|---|---|
| No `tweets.js` | 这不是完整的账号数据包。重新解压，确认里面有 `data/tweets.js` |
| No UTH JSON | 先去 x.com/i/under_the_hood 导出最近一个完整自然月 |
| Only a screenshot | 截图不够。必须是官方 JSON 和官方数据包 |
