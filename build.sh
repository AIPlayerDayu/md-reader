#!/bin/bash
# 从 src/ 构建 MD阅读器.app，并注册到系统 Launch Services。
# 用法： ./build.sh
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$DIR/MD阅读器.app"
SRC="$DIR/src"
PB=/usr/libexec/PlistBuddy

echo "==> 编译 AppleScript ..."
rm -rf "$APP"
osacompile -o "$APP" "$SRC/main.applescript"

echo "==> 拷贝资源 ..."
cp "$SRC/render.py" "$SRC/lib/marked.min.js" "$SRC/lib/hljs.min.js" "$SRC/lib/hljs.css" \
   "$APP/Contents/Resources/"
chmod +x "$APP/Contents/Resources/render.py"

echo "==> 写入 Info.plist（注册为 Markdown 文档处理程序）..."
PLIST="$APP/Contents/Info.plist"
$PB -c "Set :CFBundleName MD阅读器" "$PLIST"
$PB -c "Add :CFBundleDisplayName string MD阅读器" "$PLIST" 2>/dev/null || true
$PB -c "Set :CFBundleIdentifier com.local.mdreader" "$PLIST" 2>/dev/null || \
  $PB -c "Add :CFBundleIdentifier string com.local.mdreader" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes array" "$PLIST" 2>/dev/null || true
$PB -c "Add :CFBundleDocumentTypes:0 dict" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes:0:CFBundleTypeName string 'Markdown Document'" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes:0:CFBundleTypeRole string Viewer" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes:0:LSHandlerRank string Alternate" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes:0:CFBundleTypeExtensions array" "$PLIST"
i=0; for ext in md markdown mdown mkd; do
  $PB -c "Add :CFBundleDocumentTypes:0:CFBundleTypeExtensions:$i string $ext" "$PLIST"; i=$((i+1))
done
$PB -c "Add :CFBundleDocumentTypes:0:LSItemContentTypes array" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes:0:LSItemContentTypes:0 string net.daringfireball.markdown" "$PLIST"
$PB -c "Add :CFBundleDocumentTypes:0:LSItemContentTypes:1 string public.plain-text" "$PLIST"

echo "==> 代码签名（ad-hoc）..."
codesign --force --deep -s - "$APP" || true

echo "==> 注册到 Launch Services ..."
LSREG=/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister
"$LSREG" -f "$APP"

echo "✅ 构建完成： $APP"
echo
echo "（可选）设为 .md 默认打开程序，需要先安装 duti： brew install duti"
echo "    for ext in md markdown mdown mkd; do duti -s com.local.mdreader .\$ext all; done"
