function ai {
    $arguments = $args -join ' '
    python "$AI_TERMINAL_ASSISTANT_HOME\ai.py" $arguments
}

function AiDo {
    param(
        [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
        [scriptblock[]]$Commands
    )

    foreach ($Command in $Commands) {
        try {
            & $Command -ErrorAction Stop 2>&1 | ForEach-Object {
                if ($_ -is [System.Management.Automation.ErrorRecord]) {
                    throw $_
                } else {
                    Write-Output $_
                }
            }
        } catch {
            Write-Error -ErrorRecord $_
            Write-Host "Command failed: $Command ($($_.InvocationInfo.MyCommand))"
            break
        }
    }
}
