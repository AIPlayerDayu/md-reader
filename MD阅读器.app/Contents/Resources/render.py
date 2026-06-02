#!/usr/bin/env python3
# MD 阅读器 — 把指定的 .md 文件渲染成自包含 HTML 并用默认浏览器打开
import sys, os, json, hashlib, tempfile, subprocess

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>__HLJSCSS__</style>
<style>
  :root{--bg:#fff;--fg:#1f2328;--muted:#656d76;--border:#d0d7de;--side-bg:#f6f8fa;--accent:#0969da;--code-bg:#f6f8fa}
  html[data-theme="dark"]{--bg:#0d1117;--fg:#e6edf3;--muted:#8b949e;--border:#30363d;--side-bg:#161b22;--accent:#4493f8;--code-bg:#161b22}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
  header{position:sticky;top:0;display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--border);background:var(--side-bg);z-index:10}
  header .title{font-weight:600;font-size:14px;margin-right:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  button.tb{border:1px solid var(--border);background:var(--bg);color:var(--fg);padding:5px 11px;border-radius:7px;cursor:pointer;font-size:13px}
  .wrap{display:flex;justify-content:center}
  article{max-width:860px;width:100%;padding:36px 56px 120px;line-height:1.7;font-size:16px}
  article h1,article h2{border-bottom:1px solid var(--border);padding-bottom:.3em}
  article h1{font-size:2em}article h2{font-size:1.5em}
  article h1,article h2,article h3,article h4{margin-top:1.4em;margin-bottom:.6em;font-weight:600}
  article p{margin:0 0 1em}
  article a{color:var(--accent);text-decoration:none}article a:hover{text-decoration:underline}
  article code{background:var(--code-bg);padding:.2em .4em;border-radius:6px;font-size:85%;font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace}
  article pre{background:var(--code-bg);padding:16px;border-radius:8px;overflow:auto;border:1px solid var(--border)}
  article pre code{background:none;padding:0;font-size:14px}
  article blockquote{margin:0 0 1em;padding:0 1em;color:var(--muted);border-left:4px solid var(--border)}
  article table{border-collapse:collapse;margin:0 0 1em;display:block;overflow:auto}
  article th,article td{border:1px solid var(--border);padding:6px 13px}
  article tr:nth-child(2n){background:var(--side-bg)}
  article img{max-width:100%}
  article hr{border:none;border-top:1px solid var(--border);margin:1.6em 0}
  article ul,article ol{padding-left:2em;margin:0 0 1em}
  article li{margin:.25em 0}
  article .task-list-item{list-style:none}
</style>
</head>
<body>
<header>
  <span class="title">📖 __TITLE__</span>
  <button class="tb" id="toggleTheme">🌓 主题</button>
</header>
<div class="wrap"><article id="content"></article></div>
<script>__MARKED__</script>
<script>__HLJS__</script>
<script>
  const MD = __MD__;
  marked.setOptions({gfm:true,breaks:false,highlight:function(code,lang){
    try{ if(lang&&hljs.getLanguage(lang)) return hljs.highlight(code,{language:lang}).value; return hljs.highlightAuto(code).value;}catch(e){return code;}
  }});
  const content=document.getElementById("content");
  content.innerHTML=marked.parse(MD);
  content.querySelectorAll("pre code").forEach(b=>{try{hljs.highlightElement(b)}catch(e){}});
  const saved=localStorage.getItem("md-theme"); if(saved)document.documentElement.dataset.theme=saved;
  document.getElementById("toggleTheme").onclick=()=>{
    const cur=document.documentElement.dataset.theme==="dark"?"":"dark";
    document.documentElement.dataset.theme=cur; localStorage.setItem("md-theme",cur);
  };
</script>
</body>
</html>"""

def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        sys.exit(0)
    md_path = sys.argv[1]
    res = os.path.dirname(os.path.abspath(__file__))
    md = read(md_path)
    title = os.path.basename(md_path)
    html = (TEMPLATE
            .replace("__HLJSCSS__", read(os.path.join(res, "hljs.css")))
            .replace("__MARKED__", read(os.path.join(res, "marked.min.js")))
            .replace("__HLJS__", read(os.path.join(res, "hljs.min.js")))
            .replace("__MD__", json.dumps(md))
            .replace("__TITLE__", title.replace("<", "&lt;").replace(">", "&gt;")))
    # 同一文件用稳定的临时文件名，避免每次打开都堆积新文件
    key = hashlib.md5(os.path.abspath(md_path).encode("utf-8")).hexdigest()[:12]
    out = os.path.join(tempfile.gettempdir(), "mdreader_%s.html" % key)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run(["/usr/bin/open", out])

if __name__ == "__main__":
    main()
