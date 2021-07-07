<#
.SYNOPSIS
    Simple base64 encoding/decoding for Windows machines
.EXAMPLE
    PS C:\> .\base64.PS1 --decode "SGVsbG8gV29ybGQ="
    Hello World

    PS C:\> "Hello World" | .\base64.PS1 --encode
    SGVsbG8gV29ybGQ=
.INPUTS
    --encode: encode plaintext into base64
    --decode: decode base64 into plaintext
#>

[CmdletBinding()]
# using positional arguments to allow values to be piped in fixed order
param (
    [Parameter(Position=0, Mandatory=$true, ValueFromPipeline=$true)] [string]$option,
    [parameter(Position=1, Mandatory=$true, ValueFromPipeline=$true)] [string]$input_text
)

if ($option -ceq "--encode") {
    [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($input_text))
} elseif ($option -ceq "--decode") {
    [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($input_text))
} else {
    Write-Host "Please specify --encode or --decode flag" -ForegroundColor Red
}
