-- MD 阅读器  (AppleScript applet)
-- 双击 .md 文件时由 Finder 通过 "on open" 调用；直接打开 App 时走 "on run"

on run
	try
		set chosen to choose file with prompt "选择要阅读的 Markdown 文件：" of type {"md", "markdown", "mdown", "txt", "public.text"}
		doRender(POSIX path of chosen)
	on error number -128
		-- 用户取消，忽略
	end try
end run

on open theItems
	repeat with f in theItems
		doRender(POSIX path of (f as alias))
	end repeat
end open

on doRender(posixFile)
	set appPath to POSIX path of (path to me)
	set pyScript to appPath & "Contents/Resources/render.py"
	set pythonPath to "/usr/bin/python3"
	repeat with c in {"/opt/homebrew/bin/python3", "/usr/local/bin/python3", "/usr/bin/python3"}
		try
			do shell script "/usr/bin/test -x " & quoted form of (c as text)
			set pythonPath to (c as text)
			exit repeat
		end try
	end repeat
	do shell script quoted form of pythonPath & " " & quoted form of pyScript & " " & quoted form of posixFile
end doRender
