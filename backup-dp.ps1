```powershell
# Prosty skrypt do backupu bazy danych

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\Backups\DB"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"

# Sprawdź czy katalog istnieje
if (!(Test-Path -Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    Write-Host "Utworzono katalog $BACKUP_DIR"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DB_NAME..."

try {
    # Wykonaj eksport bazy danych MySQL
    & mysqldump -u root -p $DB_NAME --result-file="$BACKUP_DIR\$($DB_NAME)_$($DATE).sql"

    if ($LASTEXITCODE -ne 0) {
        throw "Błąd podczas wykonywania mysqldump!"
    }

    # Kompresja pliku SQL do formatu GZIP
    $SQL_FILE = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql"

    Compress-Archive -Path $SQL_FILE -DestinationPath "$SQL_FILE.zip"

    # Zmiana rozszerzenia na .gz nie zmienia formatu kompresji.
    # Do utworzenia prawdziwego pliku .gz użyj np. 7-Zip lub gzip.exe.

    Write-Host "Backup zakończony sukcesem: $SQL_FILE.zip"

    # Usuń niepotrzebny plik SQL po kompresji
    Remove-Item $SQL_FILE
}
catch {
    Write-Host "Błąd podczas wykonywania backupu: $_" -ForegroundColor Red
    exit 1
}
```