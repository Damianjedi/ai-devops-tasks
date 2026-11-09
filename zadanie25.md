# Wyjaśnienie Jenkinsfile – Simple Node.js Pipeline

Przedstawiony Jenkinsfile realizuje proces CI/CD (Continuous Integration / Continuous Delivery) dla aplikacji Node.js. Automatyzuje pobieranie kodu, instalację zależności, testowanie, budowanie aplikacji oraz tworzenie i publikowanie obrazu Docker.

Poniżej omawiam działanie poszczególnych etapów oraz najlepsze praktyki tworzenia pipeline'ów Jenkins.

## 1. Struktura pipeline

Na początku pliku znajduje się deklaracja:

```
pipeline {
    agent any
```

- `pipeline` – rozpoczyna deklaratywną definicję procesu CI/CD.
- `agent any` – pozwala Jenkinsowi uruchomić pipeline na dowolnym dostępnym agencie.

Agent to maszyna lub kontener, na którym wykonywane są polecenia pipeline'u.

W praktyce warto wybrać agenta posiadającego wymagane narzędzia, takie jak Node.js, npm i Docker.

## 2. Sekcja environment

```
environment {
    DOCKER_IMAGE = 'username/simple-node-app'
    DOCKER_TAG = "${BUILD_NUMBER}"
    DOCKER_CREDENTIALS = 'dockerhub-credentials'
}
```

Sekcja `environment` definiuje zmienne środowiskowe dostępne w pipeline.

| Zmienna              | Znaczenie                                             |
| -------------------- | ----------------------------------------------------- |
| `DOCKER_IMAGE`       | Nazwa obrazu Docker wraz z repozytorium.              |
| `DOCKER_TAG`         | Tag obrazu, tutaj numer kompilacji Jenkins.           |
| `DOCKER_CREDENTIALS` | ID danych logowania zapisanych w Jenkins Credentials. |

Przykładowo, jeśli numer kompilacji wynosi `15`, obraz otrzyma nazwę:

```
username/simple-node-app:15
```

Dobra praktyka: nie należy przechowywać haseł ani tokenów bezpośrednio w Jenkinsfile. Do tego celu służy Jenkins Credentials.

## 3. Etap Checkout

```
stage('Checkout') {
    steps {
        checkout scm
    }
}
```

Cel: pobranie kodu źródłowego z repozytorium Git.

Polecenie `checkout scm` korzysta z konfiguracji repozytorium przypisanej do pipeline'u w Jenkins.

W tym etapie:

1. Jenkins łączy się z repozytorium.
2. Pobiera kod źródłowy.
3. Przygotowuje katalog roboczy.
4. Udostępnia pliki kolejnym etapom.

Przykładowa zawartość katalogu:

```
project/
├── src/
├── tests/
├── package.json
├── package-lock.json
├── Dockerfile
└── Jenkinsfile
```

Dobra praktyka: korzystaj z kontroli wersji i uruchamiaj pipeline dla określonych gałęzi, np. `main` lub `develop`.

## 4. Etap Install Dependencies

```
stage('Install Dependencies') {
    steps {
        sh 'npm install'
    }
}
```

Cel: instalacja bibliotek wymaganych przez aplikację Node.js.

Polecenie `npm install` odczytuje plik `package.json` i instaluje wymagane zależności.

Przykładowo:

- Express – obsługa HTTP i REST API.
- Mongoose – komunikacja z MongoDB.
- Jest – testowanie aplikacji.

Po wykonaniu polecenia powstaje katalog:

```
node_modules/
```

Dobra praktyka: w pipeline CI lepiej stosować:

```
npm ci
```

`npm ci` instaluje zależności zgodnie z `package-lock.json`, zapewniając bardziej powtarzalne środowisko budowania.

## 5. Etap Run Tests

```
stage('Run Tests') {
    steps {
        sh 'npm test'
    }
}
```

Cel: automatyczne uruchomienie testów aplikacji.

Jenkins wykonuje skrypt `test` zdefiniowany w `package.json`.

Przykładowa konfiguracja:

```
{
  "scripts": {
    "test": "jest"
  }
}
```

Przykładowe testy mogą sprawdzać:

- poprawność działania endpointów API;
- walidację danych wejściowych;
- obsługę błędów;
- poprawność operacji CRUD;
- komunikację z bazą danych.

Jeśli testy zakończą się błędem, Jenkins oznaczy etap jako nieudany i standardowo nie przejdzie do kolejnych etapów.

Dobra praktyka: testy powinny być wykonywane przed budowaniem i publikowaniem obrazu Docker.

## 6. Etap Build Application

```
stage('Build Application') {
    steps {
        sh 'npm run build'
    }
}
```

Cel: przygotowanie aplikacji do uruchomienia lub wdrożenia.

Polecenie `npm run build` wykonuje skrypt `build` zdefiniowany w `package.json`.

Przykładowa konfiguracja:

```
{
  "scripts": {
    "build": "tsc"
  }
}
```

W zależności od projektu etap może:

- kompilować TypeScript do JavaScript;
- optymalizować pliki frontendowe;
- przygotowywać pliki produkcyjne;
- generować artefakty aplikacji.

Ważne: jeśli aplikacja Node.js nie wymaga procesu budowania, skrypt `build` może nie być potrzebny.

## 7. Etap Build Docker Image

```
stage('Build Docker Image') {
    steps {
        sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
    }
}
```

Cel: utworzenie obrazu Docker zawierającego aplikację.

Polecenie:

```
docker build -t username/simple-node-app:15 .
```

oznacza:

- `docker build` – budowanie obrazu;
- `-t` – nadanie nazwy i tagu;
- `.` – wykorzystanie bieżącego katalogu jako kontekstu budowania.

Docker korzysta z pliku `Dockerfile`.

Przykładowy Dockerfile:

```
FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY . .

EXPOSE 3000

CMD ["node", "src/index.js"]
```

W efekcie powstaje obraz zawierający środowisko uruchomieniowe Node.js oraz pliki aplikacji.

Dobra praktyka: stosuj obrazy bazowe o określonych wersjach, plik `.dockerignore` i użytkownika niebędącego rootem.

## 8. Etap Push Docker Image

```
stage('Push Docker Image') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: "${DOCKER_CREDENTIALS}",
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASSWORD'
            )
        ]) {
            sh '''
                echo "$DOCKER_PASSWORD" | docker login \
                    -u "$DOCKER_USER" --password-stdin

                docker push ${DOCKER_IMAGE}:${DOCKER_TAG}

                docker logout
            '''
        }
    }
}
```

Cel: opublikowanie obrazu Docker w rejestrze, np. Docker Hub.

Proces przebiega następująco:

1. `withCredentials` pobiera dane logowania z bezpiecznego magazynu Jenkins.
2. `docker login` uwierzytelnia użytkownika w rejestrze.
3. `docker push` wysyła obraz do repozytorium.
4. `docker logout` kończy sesję uwierzytelnioną.

Przykładowa publikacja:

```
docker push username/simple-node-app:15
```

Po zakończeniu obraz będzie dostępny w rejestrze Docker.

Dobra praktyka: używaj tokenów dostępu zamiast hasła do konta, ogranicz uprawnienia do publikowania i nie wypisuj sekretów w logach.

## 9. Sekcja post

```
post {
    success {
        echo 'Pipeline zakończony pomyślnie!'
    }

    failure {
        echo 'Pipeline zakończony błędem!'
    }

    always {
        echo 'Zakończono wykonywanie pipeline.'
    }
}
```

Sekcja `post` definiuje działania wykonywane po zakończeniu pipeline'u.

| Blok      | Kiedy jest wykonywany?              |
| --------- | ----------------------------------- |
| `success` | Gdy pipeline zakończy się sukcesem. |
| `failure` | Gdy pipeline zakończy się błędem.   |
| `always`  | Niezależnie od wyniku pipeline'u.   |

Można tu również umieścić:

- wysyłanie powiadomień e-mail;
- publikowanie raportów testowych;
- archiwizowanie artefaktów;
- czyszczenie plików tymczasowych.

# 10. Najlepsze praktyki tworzenia pipeline'ów Jenkins

Poniżej najważniejsze zasady, które warto stosować w projektach produkcyjnych.

### 1. Bezpieczne przechowywanie danych

Nie umieszczaj haseł, tokenów i kluczy API bezpośrednio w kodzie.

Wykorzystuj:

- Jenkins Credentials;
- zmienne środowiskowe;
- tokeny o ograniczonych uprawnieniach.

### 2. Powtarzalne budowanie aplikacji

Używaj:

```
npm ci
```

Zamiast:

```
npm install
```

Dzięki temu instalacja zależności będzie zgodna z plikiem `package-lock.json`.

### 3. Wykorzystanie cache

Cache może przyspieszyć instalowanie zależności i skrócić czas wykonywania pipeline'u.

Przykładowo można cache'ować katalog npm:

```
~/.npm
```

Cache powinien być odpowiednio izolowany, np. według wersji Node.js i sumy kontrolnej pliku `package-lock.json`.

### 4. Testowanie przed publikacją

Obraz Docker powinien być publikowany dopiero po pomyślnym przejściu testów.

Warto również dodać:

- testy integracyjne;
- analizę statyczną kodu;
- skanowanie podatności;
- testy obrazu Docker.

### 5. Wykorzystanie unikalnych tagów

Nie polegaj wyłącznie na tagu `latest`.

Przykładowe tagi:

```
simple-node-app:15
simple-node-app:16
simple-node-app:17
```

Dzięki temu można łatwo zidentyfikować wersję obrazu i odtworzyć wcześniejsze wdrożenie.

W środowisku produkcyjnym warto dodatkowo używać tagów opartych na identyfikatorze commita lub digest obrazu.

### 6. Ograniczenie uprawnień

Agent Jenkins powinien mieć tylko takie uprawnienia, jakie są niezbędne do wykonania pipeline'u.

Nie należy uruchamiać wszystkich procesów jako administrator lub root.

### 7. Obsługa błędów i timeoutów

Warto stosować `timeout`, aby pipeline nie wykonywał się bez końca.

Przykład:

```
options {
    timeout(time: 20, unit: 'MINUTES')
    timestamps()
}
```

- `timeout` – przerywa pipeline po przekroczeniu określonego czasu.
- `timestamps()` – dodaje znaczniki czasu do logów.

### 8. Archiwizowanie raportów

Warto przechowywać wyniki testów, np. raporty JUnit:

```
post {
    always {
        junit 'reports/**/*.xml'
    }
}
```

Dzięki temu można analizować błędy testów pomiędzy kolejnymi kompilacjami.

## 11. Przykładowy przebieg całego pipeline'u

## Proces CI/CD

1. Checkout

   Pobieranie kodu

   Git → kod źródłowy
2. Install Dependencies

   Instalacja

   npm ci → zależności
3. Run Tests

   Weryfikacja

   npm test → testy aplikacji
4. Build Application

   Budowanie

   npm run build → artefakty
5. Build Docker Image

   Pakowanie

   docker build → obraz
6. Push Docker Image

   Publikacja

   docker push → rejestr Docker

Gotowy obraz aplikacji w rejestrze Docker

## 12. Podsumowanie

Jenkins Pipeline automatyzuje cały proces przygotowania aplikacji do wdrożenia. Dzięki temu programista nie musi ręcznie wykonywać kolejnych poleceń, a każda zmiana w kodzie może być automatycznie sprawdzana.

Najważniejsze praktyki to:

1. Bezpieczne przechowywanie poświadczeń.
2. Powtarzalne instalowanie zależności przez `npm ci`.
3. Automatyczne testowanie kodu.
4. Optymalizacja budowania obrazów Docker.
5. Stosowanie unikalnych tagów obrazów.
6. Monitorowanie błędów i czasu wykonywania pipeline'u.
7. Ograniczanie uprawnień agentów Jenkins.

Ważne rozróżnienie: przedstawiony Jenkinsfile realizuje przede wszystkim CI oraz etap publikowania artefaktu. Nie wykonuje jeszcze wdrożenia aplikacji na serwerze produkcyjnym (CD). Do pełnego procesu CI/CD można dodać osobny etap `Deploy`, który wdroży opublikowany obraz na wybranym środowisku.