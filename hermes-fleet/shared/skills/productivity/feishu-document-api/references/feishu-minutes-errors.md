# Feishu Minutes API — Error Codes & Resolutions

## App-level REST API (tenant_access_token)

### 404 on `/open-apis/vc/v1/minutes/{token}`
- **Cause:** App has no VC (视频会议) permissions in Feishu developer console
- **Fix:** Don't use app-level API for minutes. Switch to lark-cli user auth with `--domain minutes`.

### 99991668 on `/open-apis/minutes/v1/`
- **Cause:** Wrong token type — this endpoint needs user_access_token, not tenant_access_token
- **Fix:** Use lark-cli user auth.

## lark-cli user auth

### 99991679 — missing_scope
- **Message:** `missing required scope(s): minutes:minute:download, minutes:minutes.transcript:export`
- **Context:** Calling transcript API after basic `--domain minutes` auth
- **Fix:** Re-auth with `--scope "minutes:minute:download minutes:minutes.transcript:export"`

### im:chat:read missing
- **Context:** `lark-cli im +chat-search`
- **Fix:** Add `--scope "im:chat:read"` or use `channel_directory.json` instead

### im:message.send_as_user / im:message missing
- **Context:** `lark-cli im +messages-send --as user`
- **Fix:** Add those scopes, or use bot identity (if app has permissions)

## File upload

### "Feishu file upload missing file_key"
- **Context:** `send_message` with `MEDIA:/path/to/file.txt` on Feishu
- **Fix:** Can't upload files via gateway. Use `lark-cli im +messages-send --file` with bot identity.

### im:resource:upload — app-level permission missing
- **Message:** `Access denied. One of the following scopes is required: [im:resource:upload, im:resource]`
- **Fix:** Admin must enable `im:resource:upload` in Feishu developer console for app `cli_aa952e66a6799ceb`

## QR code

### "unsafe output path"
- **Context:** `lark-cli auth qrcode <url> -o /tmp/qr.png`
- **Fix:** `-o` requires relative path. `cd /tmp && lark-cli auth qrcode <url> -o qr.png`

## Drive upload fallback (when im:resource:upload is blocked)

When you can't push files directly to a group chat (missing `im:resource:upload`), upload to Feishu Drive instead and share the link:

```python
import subprocess, os

token = open('/tmp/fs_token.txt').read().strip()
file_path = "/path/to/file.txt"
file_name = os.path.basename(file_path)
auth = "Authorization: Bearer *** + token

cmd = [
    'curl', '-s', '-X', 'POST',
    'https://open.feishu.cn/open-apis/drive/v1/files/upload_all',
    '-H', auth,
    '-F', 'file_name=' + file_name,
    '-F', 'parent_type=explorer',
    '-F', 'parent_node=',
    '-F', 'size=' + str(os.path.getsize(file_path)),
    '-F', 'file=@' + file_path
]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout)  # Returns: {"code":0,"data":{"file_token":"...","url":"https://..."}}
```

Then use `send_message` to push the Drive link to the group. Caveat: files uploaded this way belong to the tenant app's Drive and may need permission adjustment for group members to access.

**`lark-cli drive +push` is NOT a shortcut** — it requires `--folder-token` which is hard to discover. Use the REST API above instead.

## API Path Gotchas

| What | Wrong path | Right path |
|------|-----------|------------|
| Minutes basic info | — | `/open-apis/vc/v1/minutes/{token}` |
| Minutes transcript | `/open-apis/vc/v1/minutes/{token}/transcript` (404) | `/open-apis/minutes/v1/minutes/{token}/transcript` |
| Document raw_content | — | `/open-apis/docx/v1/documents/{token}/raw_content` |
| Document blocks | — | `/open-apis/docx/v1/documents/{token}/blocks` |
