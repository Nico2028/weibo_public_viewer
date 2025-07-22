#!/usr/bin/env python3
import os, re, ast
from datetime import datetime
from pathlib import Path

BASE_DIR    = Path(__file__).parent.resolve()
MEDIA_DIR   = BASE_DIR / 'media'
OUTPUT_FILE = BASE_DIR / 'index.html'

def parse_txt(path: Path):
    posts = []
    current = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("时间:"):
            if current: posts.append(current)
            tstr = line.split("时间:",1)[1].strip()
            try:
                ts = datetime.strptime(tstr, "%a %b %d %H:%M:%S %z %Y")
            except:
                ts = tstr
            current = {"time": ts, "content": "", "images": [], "videos": []}
        elif line.startswith("内容:") and current:
            current["content"] = line.split("内容:",1)[1].strip()
        elif line.startswith("图片文件:") and current:
            part = line.split("图片文件:",1)[1].strip() or "[]"
            imgs = ast.literal_eval(part)
            current["images"].extend(Path(p).name for p in imgs)
        elif line.startswith("视频文件:") and current:
            part = line.split("视频文件:",1)[1].strip() or "[]"
            vids = ast.literal_eval(part)
            current["videos"].extend(Path(p).name for p in vids)
        elif current:
            current["content"] += "\n" + line
    if current: posts.append(current)
    return posts

all_posts = []
for txt in sorted(BASE_DIR.glob("page_*.txt"),
                  key=lambda p: int(p.stem.split("_")[1])):
    all_posts.extend(parse_txt(txt))

all_posts.sort(key=lambda x: x["time"].timestamp() 
               if isinstance(x["time"], datetime) else x["time"])

lines = [
  "<!DOCTYPE html>",
  "<html lang='zh'>",
  "<head>",
  "  <meta charset='UTF-8'>",
  "  <meta name='viewport' content='width=device-width,initial-scale=1.0'>",
  "  <title>微博内容展示</title>",
  "  <style>",
  "    body {font-family:Arial,sans-serif;background:#f4f4f4;margin:0;padding:0;}",
  "    .container {max-width:800px;margin:20px auto;padding:20px;background:#fff;"
   "border-radius:6px;box-shadow:0 4px 8px rgba(0,0,0,0.1);}",
  "    .post {margin-bottom:30px;padding-bottom:20px;border-bottom:1px solid #ddd;}",
  "    .time {color:#888;font-size:14px;margin-bottom:8px;}",
  "    .content {white-space:pre-wrap;font-size:18px;color:#333;line-height:1.6;"
   "margin-bottom:8px;}",
  "    .media img, .media video {max-width:100%;display:block;margin-bottom:10px;"
   "border-radius:4px;}",
  "  </style>",
  "</head>",
  "<body>",
  "  <div class='container'>",
  "    <h1>微博内容展示</h1>"
]

for post in all_posts:
    ts = (post["time"].strftime("%Y-%m-%d %H:%M:%S")
          if isinstance(post["time"], datetime) else post["time"])
    lines += [
      "    <div class='post'>",
      f"      <div class='time'>{ts}</div>",
      f"      <div class='content'>{post['content'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}</div>"
    ]
    if post["images"] or post["videos"]:
        lines.append("      <div class='media'>")
        for img in post["images"]:
            lines.append(f"        <img src='media/{img}' alt='微博图片'>")
        for vid in post["videos"]:
            ext = Path(vid).suffix.lstrip('.')
            lines.append(
              f"        <video controls><source src='media/{vid}' type='video/{ext}'></video>"
            )
        lines.append("      </div>")
    lines.append("    </div>")

lines += [
  "  </div>",
  "  <script src='script.js'></script>",
  "</body>",
  "</html>"
]

OUTPUT_FILE.write_text("\n".join(lines), encoding='utf-8')
print("✅ index.html 已生成：", OUTPUT_FILE)
