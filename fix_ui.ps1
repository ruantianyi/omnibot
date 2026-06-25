$filepath = "c:\Users\ruant\OneDrive\Documents\Omnibot\6.4.html"
$lines = Get-Content $filepath -Encoding UTF8

$new_lines = @()
$skip = $false

foreach ($line in $lines) {
    if ($line -match "<!-- ═══ Advanced ═══ -->") {
        $skip = $true
    }
    
    if ($skip -and ($line -match "<!-- OK Button -->")) {
        $skip = $false
    }
    
    if (-not $skip) {
        if ($line -match '<h4 class="text-xs font-bold text-white">Alpha Engine</h4>') {
            $line = $line.Replace('text-white', 'text-slate-800 dark:text-white')
        }
        elseif ($line -match '<h4 class="text-xs font-bold text-white">Nova Engine</h4>') {
            $line = $line.Replace('text-white', 'text-slate-800 dark:text-white')
        }
        elseif ($line -match '<h4 class="text-xs font-bold text-white">Luna Engine</h4>') {
            $line = $line.Replace('text-white', 'text-slate-800 dark:text-white')
        }
        $new_lines += $line
    }
}

Set-Content -Path $filepath -Value $new_lines -Encoding UTF8
