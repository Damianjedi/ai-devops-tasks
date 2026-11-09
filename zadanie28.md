# Wyjaśnienie działania skryptu Python komunikującego się z Jenkins API

Skrypt służy do automatyzacji zarządzania zadaniami (Jobs) w Jenkinsie. Wykorzystuje Jenkins REST API, dzięki czemu może komunikować się z serwerem Jenkins bez konieczności korzystania z interfejsu graficznego.

Pozwala wykonywać trzy podstawowe operacje:

1. Pobierać listę wszystkich zadań Jenkins.
2. Sprawdzać status ostatnich buildów.
3. Uruchamiać wybrane zadania.

## 1. Jakich bibliotek używa skrypt?

Skrypt korzysta z kilku standardowych bibliotek Pythona oraz jednej zewnętrznej biblioteki.

| Biblioteka            | Typ         | Zastosowanie                                       |
| --------------------- | ----------- | -------------------------------------------------- |
| `requests`            | Zewnętrzna  | Wysyłanie zapytań HTTP do Jenkins API              |
| `os`                  | Standardowa | Odczytywanie zmiennych środowiskowych              |
| `sys`                 | Standardowa | Zamykanie programu i obsługa kodów błędów          |
| `argparse`            | Standardowa | Obsługa argumentów przekazywanych w terminalu      |
| `urllib.parse`        | Standardowa | Kodowanie nazw zadań i ścieżek URL                 |
| `requests.auth`       | Requests    | Uwierzytelnianie użytkownika przez HTTP Basic Auth |
| `requests.exceptions` | Requests    | Obsługa błędów komunikacji HTTP                    |

### Najważniejsza biblioteka – requests

Biblioteka `requests` odpowiada za komunikację z Jenkins API.

Instalacja:

```
pip install requests
```

Przykład wysłania zapytania do Jenkinsa:

```
import requestsresponse = requests.get(    "http://localhost:8080/api/json")print(response.json())
```

Metoda `requests.get()` pobiera dane z serwera Jenkins, a `response.json()` przekształca odpowiedź JSON na obiekt Pythona.

W przypadku uruchamiania zadania wykorzystywana jest metoda `requests.post()`.

## 2. Jak działa skrypt?

Skrypt został podzielony na kilka logicznych części.

### A. Konfiguracja połączenia z Jenkins API

Na początku tworzona jest klasa `JenkinsAPI`:

```
class JenkinsAPI:    def __init__(self, url, username, token):        self.url = url.rstrip("/")        self.session = requests.Session()        self.session.auth = HTTPBasicAuth(username, token)
```

Odpowiada ona za:

- zapisanie adresu serwera Jenkins;
- skonfigurowanie sesji HTTP;
- ustawienie danych uwierzytelniających;
- przygotowanie połączenia do wykonywania kolejnych zapytań.

Dzięki `requests.Session()` nie trzeba za każdym razem konfigurować autoryzacji.

### B. Autoryzacja

Jenkins może wymagać uwierzytelnienia użytkownika przed udostępnieniem API.

W skrypcie wykorzystywany jest mechanizm HTTP Basic Authentication:

```
self.session.auth = HTTPBasicAuth(username, token)
```

Zamiast hasła użytkownika stosowany jest API Token wygenerowany w Jenkinsie.

Dane dostępowe są pobierane ze zmiennych środowiskowych:

```
url = os.getenv("JENKINS_URL")username = os.getenv("JENKINS_USER")token = os.getenv("JENKINS_TOKEN")
```

Takie rozwiązanie jest bezpieczniejsze niż wpisywanie danych logowania bezpośrednio w kodzie programu.

### C. Pobieranie listy zadań

Za pobieranie wszystkich zadań odpowiada metoda:

```
def get_all_jobs(self):
```

Wysyła ona zapytanie GET do Jenkins API:

```
http://localhost:8080/api/json
```

Jenkins zwraca dane w formacie JSON, zawierające informacje o zadaniach.

Przykładowa odpowiedź:

```
{
  "jobs": [
    {
      "name": "frontend-app",
      "url": "http://localhost:8080/job/frontend-app/"
    },
    {
      "name": "backend-api",
      "url": "http://localhost:8080/job/backend-api/"
    }
  ]
}
```

Skrypt odczytuje nazwy zadań i wyświetla je w terminalu.

Dodatkowo obsługuje foldery Jenkins, dzięki czemu może pobierać również zadania zagnieżdżone.

### D. Sprawdzanie statusu ostatniego buildu

Za tę funkcjonalność odpowiada metoda:

```
def get_last_build_status(self, job_name):
```

Wykorzystuje endpoint:

```
/job/NAZWA_ZADANIA/lastBuild/api/json
```

Przykładowo:

```
http://localhost:8080/job/frontend-app/lastBuild/api/json
```

Jenkins zwraca informacje o ostatnim buildzie, m.in.:

- numer buildu;
- wynik wykonania;
- informację, czy build nadal trwa;
- adres URL buildu.

Skrypt interpretuje te informacje i wyświetla status.

Najważniejszy fragment:

```
if build.get("building"):    status = "BUILDING"else:    status = build.get("result") or "UNKNOWN"
```

Oznacza to, że jeśli build nadal trwa, otrzymamy `BUILDING`. W przeciwnym przypadku wyświetlony zostanie wynik, np. `SUCCESS` lub `FAILURE`.

### E. Uruchamianie zadania Jenkins

Za uruchamianie zadania odpowiada metoda:

```
def run_job(self, job_name):
```

Wysyła ona zapytanie HTTP POST do endpointu:

```
/job/NAZWA_ZADANIA/build
```

Przykład:

```
http://localhost:8080/job/frontend-app/build
```

Przed wysłaniem żądania skrypt pobiera token CSRF (Crumb), jeśli Jenkins go wymaga.

Po otrzymaniu poprawnej odpowiedzi Jenkins zwraca nagłówek `Location`, który wskazuje zadanie oczekujące w kolejce.

Ważne: uruchomienie buildu nie oznacza, że został on już wykonany. Jenkins może umieścić go w kolejce i rozpocząć później.

## 3. Obsługa błędów

Skrypt wykorzystuje mechanizm `try-except`, aby reagować na problemy podczas komunikacji z serwerem.

| Błąd               | Znaczenie                          |
| ------------------ | ---------------------------------- |
| HTTP 401           | Nieprawidłowy login lub API Token  |
| HTTP 403           | Brak uprawnień lub problem z CSRF  |
| HTTP 404           | Nie znaleziono zadania lub buildu  |
| Connection Error   | Brak połączenia z serwerem Jenkins |
| Timeout            | Przekroczony czas oczekiwania      |
| API Response Error | Nieprawidłowa odpowiedź API        |

Przykład obsługi błędu:

```
except requests.HTTPError as error:    print(f"HTTP ERROR: {error}")except RequestException as error:    print(f"CONNECTION ERROR: {error}")
```

Dzięki temu program nie kończy działania niekontrolowanym wyjątkiem.

## 4. Jak używać skryptu? Przykładowe polecenia

Załóżmy, że plik ze skryptem nazywa się:

```
jenkins_manager.py
```

Adres Jenkins:

```
http://localhost:8080
```

### Krok 1. Konfiguracja zmiennych środowiskowych

Linux / macOS:

```
export JENKINS_URL="http://localhost:8080"
export JENKINS_USER="admin"
export JENKINS_TOKEN="twoj_api_token"
```

Windows PowerShell:

```
$env:JENKINS_URL="http://localhost:8080"
$env:JENKINS_USER="admin"
$env:JENKINS_TOKEN="twoj_api_token"
```

### Krok 2. Wyświetlenie wszystkich zadań

```
python jenkins_manager.py list
```

Przykładowy rezultat:

```
=== LISTA ZADAŃ JENKINS ===
- frontend-app
- backend-api
- deploy-production
- DevOps/test-application

Liczba zadań: 4
```

### Krok 3. Sprawdzenie statusu buildu

```
python jenkins_manager.py status --job frontend-app
```

Przykładowy rezultat:

```
=== STATUS OSTATNIEGO BUILDU ===
Job:    frontend-app
Build:  15
Status: SUCCESS
URL:    http://localhost:8080/job/frontend-app/15/
```

### Krok 4. Uruchomienie wybranego zadania

```
python jenkins_manager.py run --job frontend-app
```

Przykładowy rezultat:

```
=== URUCHOMIENIE ZADANIA ===
Job:    frontend-app
Status: TRIGGERED
Queue:  http://localhost:8080/queue/item/125/
```

### Krok 5. Sprawdzenie statusu kolejnego buildu

Po uruchomieniu zadania można ponownie wykonać:

```
python jenkins_manager.py status --job frontend-app
```

Pozwoli to sprawdzić, czy build jest w trakcie wykonywania, czy zakończył się sukcesem lub błędem.



## 5. Podsumowanie

Skrypt wykorzystuje Jenkins REST API oraz bibliotekę `requests` do zautomatyzowania podstawowych operacji administracyjnych.

Najważniejsze zalety rozwiązania:

- Automatyzacja – możliwość zarządzania zadaniami bez interfejsu graficznego.
- Bezpieczeństwo – wykorzystanie API Token i zmiennych środowiskowych.
- Elastyczność – obsługa różnych zadań i folderów Jenkins.
- Łatwość integracji – możliwość wykorzystania skryptu w innych aplikacjach Python, systemach monitoringu lub procesach CI/CD.

W praktyce takie rozwiązanie może być wykorzystane np. do stworzenia zewnętrznego systemu monitorowania pipeline'ów CI/CD, który automatycznie sprawdza wyniki buildów i uruchamia wybrane zadania Jenkins.