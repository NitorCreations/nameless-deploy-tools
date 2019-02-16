$url = "https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi"
$output = "C:\nameless\VCForPython27.msi"
(New-Object System.Net.WebClient).DownloadFile($url, $output)
Start-Process msiexec -ArgumentList @("/i", "C:\nameless\VCForPython27.msi", "/passive", "/quiet") -NoNewWindow -Wait

python.exe -m pip install -U pip
python.exe -m pip install -U setuptools certifi
pip install -U awscli boto3 nameless-deploy-tools
