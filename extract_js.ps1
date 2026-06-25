$html = Get-Content 7.0.html -Raw
$scripts = [regex]::Matches($html, '(?si)<script[^>]*>(.*?)</script>')
$scripts | ForEach-Object { $_.Groups[1].Value } | Out-File -FilePath test.js
cscript //E:JScript test.js
