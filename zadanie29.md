# Uruchomienie Jenkins z plikiem JCasC – instrukcja krok po kroku

Jenkins Configuration as Code (JCasC) pozwala skonfigurować serwer Jenkins za pomocą pliku YAML. Dzięki temu nie trzeba ręcznie ustawiać wszystkich parametrów w panelu administracyjnym.

Wykorzystamy Docker, aby uruchomić Jenkins z wcześniej przygotowanym szablonem `jenkins.yaml`.

Cały proces obejmuje:

1. Instalację Dockera.
2. Przygotowanie plików konfiguracyjnych.
3. Instalację wtyczek Jenkins.
4. Zbudowanie obrazu Jenkins.
5. Uruchomienie kontenera.
6. Sprawdzenie poprawności konfiguracji.

## 1. Instalacja Dockera

Docker pozwoli nam uruchomić Jenkins w kontenerze.

Na Ubuntu wykonujemy:

```
sudo apt update
sudo apt install docker.io docker-compose-v2 -y
```

Uruchamiamy usługę:

```
sudo systemctl enable docker
sudo systemctl start docker
```

Sprawdzamy instalację:

```
docker --version
docker compose version
```

## 2. Przygotowanie struktury katalogów

Tworzymy katalog projektu:

```
mkdir jenkins-jcasc
cd jenkins-jcasc
```

Przygotowujemy strukturę:

```
jenkins-jcasc/
│
├── Dockerfile
├── docker-compose.yml
├── plugins.txt
│
└── casc_configs/
    └── jenkins.yaml
```

Każdy plik ma inne zastosowanie:

| Plik                 | Zastosowanie                            |
| -------------------- | --------------------------------------- |
| `Dockerfile`         | Przygotowuje obraz Jenkins              |
| `docker-compose.yml` | Definiuje sposób uruchomienia kontenera |
| `plugins.txt`        | Lista wymaganych wtyczek                |
| `jenkins.yaml`       | Konfiguracja Jenkins w formacie YAML    |

## 3. Przygotowanie pliku plugins.txt

Plik `plugins.txt` zawiera listę wtyczek, które będą potrzebne do działania naszego środowiska.

Tworzymy plik:

```
nano plugins.txt
```

Wprowadzamy:

```
configuration-as-code
workflow-aggregator
git
maven-plugin
nodejs
docker-workflow
job-dsl
ws-cleanup
pipeline-stage-view
```

Najważniejsze wtyczki:

- `configuration-as-code` – umożliwia odczytywanie konfiguracji YAML.
- `workflow-aggregator` – zapewnia obsługę Pipeline.
- `git` – umożliwia pobieranie kodu z Git.
- `maven-plugin` – integruje Jenkins z Maven.
- `nodejs` – umożliwia konfigurację Node.js.
- `job-dsl` – pozwala tworzyć zadania za pomocą skryptów DSL.
- `ws-cleanup` – umożliwia czyszczenie katalogów roboczych.

Ważne: JCasC nie instaluje wtyczek. Wtyczki instalujemy osobno, np. za pomocą `jenkins-plugin-cli`.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://plugins.jenkins.io\&sz=32)

Jenkins plugin+1



W środowisku produkcyjnym warto przypiąć konkretne wersje wtyczek, zamiast pozostawiać ich wersje nieokreślone.

## 4. Przygotowanie Dockerfile

Tworzymy plik:

```
nano Dockerfile
```

Wprowadzamy:

```
FROM jenkins/jenkins:lts-jdk21

USER root

# Instalacja Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Kopiowanie listy wtyczek
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Instalacja wtyczek
RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins

# Lokalizacja konfiguracji JCasC
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs/jenkins.yaml
```

Wyjaśnienie:

1. `FROM` – wybiera bazowy obraz Jenkins.
2. `USER root` – przełącza użytkownika na administratora systemu w kontenerze.
3. `RUN apt-get` – instaluje Docker CLI.
4. `COPY` – kopiuje plik z listą wtyczek.
5. `jenkins-plugin-cli` – instaluje wtyczki.
6. `USER jenkins` – przywraca użytkownika Jenkins.
7. `CASC_JENKINS_CONFIG` – wskazuje lokalizację pliku YAML.

Uwaga: instalacja Docker CLI nie oznacza, że Jenkins ma dostęp do działającego demona Docker. Do wykonywania poleceń Docker potrzebny będzie odpowiednio skonfigurowany agent.

## 5. Przygotowanie docker-compose.yml

Tworzymy plik:

```
nano docker-compose.yml
```

Wprowadzamy:

```
services:
  jenkins:
    build: .
    container_name: jenkins-server

    ports:
      - "8080:8080"
      - "50000:50000"

    environment:
      CASC_JENKINS_CONFIG: /var/jenkins_home/casc_configs/jenkins.yaml

    volumes:
      - jenkins_home:/var/jenkins_home
      - ./casc_configs:/var/jenkins_home/casc_configs:ro

    restart: unless-stopped

volumes:
  jenkins_home:
```

Wyjaśnienie najważniejszych elementów:

| Parametr       | Znaczenie                                    |
| -------------- | -------------------------------------------- |
| `8080:8080`    | Dostęp do panelu Jenkins                     |
| `50000:50000`  | Port agentów inbound                         |
| `jenkins_home` | Przechowywanie danych Jenkins                |
| `casc_configs` | Katalog z plikiem YAML                       |
| `restart`      | Automatyczne uruchomienie po restarcie hosta |

Wolumen `jenkins_home` przechowuje dane, konfigurację i historię buildów. Dzięki temu nie tracimy ich po ponownym utworzeniu kontenera.

## 6. Umieszczenie pliku jenkins.yaml

Teraz umieszczamy wcześniej przygotowany plik konfiguracyjny w katalogu:

```
jenkins-jcasc/casc_configs/jenkins.yaml
```

Możemy sprawdzić, czy plik istnieje:

```
ls -l casc_configs/
```

Powinniśmy zobaczyć:

```
jenkins.yaml
```

Najważniejszym elementem jest zmienna:

```
CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs/jenkins.yaml
```

Informuje ona wtyczkę JCasC, gdzie znajduje się konfiguracja.

Podczas uruchamiania Jenkins odczytuje plik YAML i próbuje zastosować zdefiniowane w nim ustawienia.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://plugins.jenkins.io\&sz=32)

Jenkins plugin+1



## 7. Budowanie obrazu Jenkins

W katalogu `jenkins-jcasc` wykonujemy:

```
docker compose build
```

Docker:

- pobiera bazowy obraz Jenkins;
- instaluje wymagane pakiety;
- kopiuje listę wtyczek;
- instaluje wtyczki;
- przygotowuje obraz do uruchomienia.

Możemy sprawdzić, czy obraz został utworzony:

```
docker images
```

## 8. Uruchomienie Jenkins

Uruchamiamy kontener:

```
docker compose up -d
```

Parametr `-d` oznacza uruchomienie w tle.

Sprawdzamy status:

```
docker ps
```

Powinniśmy zobaczyć kontener `jenkins-server` ze statusem `Up`.

Aby sprawdzić logi:

```
docker compose logs -f jenkins
```

W logach należy zwrócić uwagę na:

- poprawne uruchomienie Jenkins;
- załadowanie wtyczki Configuration as Code;
- odczyt pliku `jenkins.yaml`;
- ewentualne błędy konfiguracji.

## 9. Pierwsze logowanie do Jenkins

Otwieramy przeglądarkę internetową i wpisujemy:

```
http://localhost:8080
```

Jeżeli Jenkins wyświetli ekran odblokowania, hasło administratora odczytamy poleceniem:

```
docker exec jenkins-server \
  cat /var/jenkins_home/secrets/initialAdminPassword
```

Następnie:

1. Kopiujemy hasło.
2. Wprowadzamy je w przeglądarce.
3. Kończymy początkową konfigurację, jeżeli jest wymagana.
4. Logujemy się do Jenkins.

Jeżeli konfiguracja bezpieczeństwa jest już poprawnie zdefiniowana w JCasC, sposób pierwszego logowania może wyglądać inaczej. Nie należy pomijać konfiguracji uwierzytelniania i uprawnień w środowisku produkcyjnym.

## 10. Sprawdzenie konfiguracji JCasC

Po zalogowaniu przechodzimy do:

Manage Jenkins → Configuration as Code

W tym miejscu można sprawdzić konfigurację odczytaną przez Jenkins.

Weryfikujemy między innymi:

- liczbę wykonawców (Executors);
- ustawiony komunikat systemowy;
- konfigurację Maven;
- konfigurację Node.js;
- utworzone zadania Pipeline.

Możemy również zmienić plik YAML i ponownie załadować konfigurację przez panel JCasC, wybierając opcję `Reload existing configuration`.

Warto pamiętać, że zmiany wykonane ręcznie w panelu mogą zostać nadpisane przy kolejnym zastosowaniu konfiguracji JCasC.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.jenkins.io\&sz=32)

Jenkins



## 11. Sprawdzenie utworzonego zadania Pipeline

Jeżeli w pliku `jenkins.yaml` znajduje się sekcja `jobs`, Jenkins powinien utworzyć zadanie zgodnie z zawartym w niej skryptem Job DSL.

Przykładowo może to być:

```
web-application-pipeline
```

W panelu Jenkins:

1. Otwieramy dashboard.
2. Wybieramy `web-application-pipeline`.
3. Klikamy `Build Now`.
4. Otwieramy `Console Output`.
5. Sprawdzamy przebieg kolejnych etapów.

Przykładowe etapy Pipeline:

| Etap              | Zadanie                      |
| ----------------- | ---------------------------- |
| Checkout          | Pobranie kodu z repozytorium |
| Build             | Budowanie aplikacji          |
| Test              | Uruchomienie testów          |
| Docker Build      | Budowanie obrazu Docker      |
| Deploy Staging    | Wdrożenie testowe            |
| Deploy Production | Wdrożenie produkcyjne        |

Pamiętaj, że przykładowy adres repozytorium Git trzeba zastąpić adresem własnego projektu. Narzędzia takie jak Maven, Node.js i Docker muszą być dostępne na agencie wykonującym Pipeline.

## 12. Najczęstsze problemy

| Problem                        | Możliwe rozwiązanie                    |
| ------------------------------ | -------------------------------------- |
| Jenkins nie uruchamia się      | Sprawdź `docker compose logs jenkins`  |
| Błąd YAML                      | Sprawdź wcięcia i nazwy właściwości    |
| Brak zadania Pipeline          | Sprawdź instalację `job-dsl`           |
| Maven nie działa               | Sprawdź konfigurację narzędzi          |
| Node.js nie działa             | Sprawdź wtyczkę NodeJS                 |
| Docker Build kończy się błędem | Sprawdź dostęp agenta do Docker Engine |
| Nie można otworzyć Jenkins     | Sprawdź port 8080 i zaporę sieciową    |

Do sprawdzenia składni pliku Compose używamy:

```
docker compose config
```

To polecenie nie sprawdza jednak poprawności właściwości JCasC. Schemat konfiguracji zależy od zainstalowanych wtyczek i ich wersji.

## 13. Przydatne polecenia administracyjne

| Polecenie                        | Działanie                      |
| -------------------------------- | ------------------------------ |
| `docker compose up -d`           | Uruchamia Jenkins              |
| `docker compose stop`            | Zatrzymuje Jenkins             |
| `docker compose start`           | Ponownie uruchamia Jenkins     |
| `docker compose restart`         | Restartuje Jenkins             |
| `docker compose down`            | Usuwa kontener i sieć Compose  |
| `docker compose logs -f jenkins` | Wyświetla logi                 |
| `docker compose build`           | Buduje obraz                   |
| `docker ps`                      | Pokazuje uruchomione kontenery |

Uwaga: `docker compose down` bez `-v` zachowuje nazwany wolumen `jenkins_home`. Nie używaj `docker compose down -v`, jeśli chcesz zachować dane Jenkins.

## Podsumowanie

W całym procesie każdy element ma określoną odpowiedzialność:

| Element            | Odpowiedzialność                      |
| ------------------ | ------------------------------------- |
| Docker             | Uruchamia Jenkins w kontenerze        |
| Dockerfile         | Przygotowuje obraz Jenkins            |
| plugins.txt        | Określa wymagane wtyczki              |
| docker-compose.yml | Definiuje środowisko uruchomieniowe   |
| jenkins.yaml       | Definiuje konfigurację Jenkins        |
| JCasC              | Odczytuje i stosuje konfigurację YAML |

