Odpowiedniki poleceń Bash i PowerShell
Bash	PowerShell	Opis
mkdir -p	New-Item -ItemType Directory	Tworzenie katalogu
[ ! -d "$DIR" ]	Test-Path	Sprawdzanie istnienia katalogu
date	Get-Date	Pobieranie daty i czasu
echo	Write-Host	Wyświetlanie komunikatów
$?	$LASTEXITCODE	Sprawdzanie kodu zakończenia programu zewnętrznego
exit 1	exit 1	Zakończenie skryptu błędem
gzip	Compress-Archive	Kompresja (ZIP zamiast GZIP)