Oto 5 kluczowych praktyk bezpieczeństwa dla aplikacji Dockerowych w środowisku produkcyjnym:

### 1. Uruchamianie kontenerów bez uprawnień administratora (Non-root)

Nie należy uruchamiać aplikacji wewnątrz kontenera jako użytkownik `root`. Warto utworzyć dedykowanego użytkownika z ograniczonymi uprawnieniami.

Przykład w `Dockerfile`:

```
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

CMD ["node", "server.js"]
```

Korzyść: ograniczenie potencjalnych szkód w przypadku przejęcia kontenera przez atakującego.

### 2. Regularne aktualizowanie obrazów Docker

Należy korzystać z aktualnych, oficjalnych obrazów i regularnie aktualizować ich wersje. Stare obrazy mogą zawierać znane luki bezpieczeństwa.

Przykład:

```
FROM node:20-alpine
```

Warto również skanować obrazy pod kątem podatności za pomocą narzędzi takich jak:

- Docker Scout
- Trivy
- Snyk

Przykład skanowania:

```
docker scout cves my-app:latest
```

Korzyść: zmniejszenie ryzyka wykorzystania znanych podatności w bibliotekach i systemie bazowym.

### 3. Bezpieczne przechowywanie sekretów

Nie należy umieszczać haseł, tokenów API ani kluczy dostępu bezpośrednio w `Dockerfile` lub obrazie Docker.

Zamiast tego można wykorzystać Docker Secrets lub bezpieczny menedżer sekretów.

Przykład w Docker Compose:

```
services:
  app:
    image: my-app:latest
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

W aplikacji sekret jest dostępny jako plik:

```
/run/secrets/db_password
```

Korzyść: ograniczenie ryzyka przypadkowego ujawnienia poufnych danych.

### 4. Ograniczanie uprawnień i dostępu do zasobów

Kontenery powinny mieć dostęp wyłącznie do zasobów niezbędnych do działania aplikacji.

Warto stosować:

- `--read-only` – system plików kontenera tylko do odczytu.
- `--memory` – ograniczenie wykorzystania pamięci RAM.
- `--cpus` – ograniczenie wykorzystania procesora.
- `--cap-drop=ALL` – usunięcie zbędnych uprawnień systemowych.
- Unikanie `--privileged`, które przyznaje kontenerowi szerokie uprawnienia.

Przykład:

```
docker run -d \
  --name secure-app \
  --read-only \
  --memory=512m \
  --cpus=1 \
  --cap-drop=ALL \
  my-app:latest
```

Korzyść: ograniczenie możliwości atakującego oraz zmniejszenie ryzyka wykorzystania zasobów hosta.

### 5. Izolacja sieciowa i monitorowanie kontenerów

Kontenery powinny komunikować się wyłącznie z usługami, które są im potrzebne. Nie należy bez potrzeby udostępniać portów baz danych publicznie.

Warto:

- Tworzyć osobne sieci Docker dla poszczególnych usług.
- Udostępniać na zewnątrz tylko niezbędne porty.
- Monitorować logi kontenerów.
- Konfigurować mechanizmy `healthcheck`.
- Monitorować nietypowe zachowania i restarty kontenerów.

Przykład konfiguracji Docker Compose:

```
services:
  app:
    image: my-app:latest
    ports:
      - "8080:8080"
    networks:
      - frontend
      - backend

  db:
    image: postgres:16
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true
```

Korzyść: ograniczenie nieautoryzowanego dostępu do usług oraz zmniejszenie ryzyka ataków sieciowych.

## Podsumowanie

| Praktyka                           | Główny cel                                |
| ---------------------------------- | ----------------------------------------- |
| Uruchamianie jako non-root         | Ograniczenie uprawnień                    |
| Aktualizowanie obrazów             | Eliminowanie podatności                   |
| Bezpieczne przechowywanie sekretów | Ochrona haseł i tokenów                   |
| Ograniczanie uprawnień i zasobów   | Ochrona hosta                             |
| Izolacja sieciowa i monitoring     | Ochrona komunikacji i wykrywanie zagrożeń |

Wniosek: bezpieczeństwo aplikacji Dockerowych w środowisku produkcyjnym wymaga stosowania wielu zabezpieczeń jednocześnie. Najlepszym podejściem jest zasada Defense in Depth (obrona warstwowa), czyli łączenie izolacji, ograniczania uprawnień, aktualizacji, ochrony sekretów i monitorowania.

Dzięki temu nawet w przypadku przejęcia pojedynczego kontenera potencjalne szkody zostają znacząco ograniczone.






Aby wdrożyć pierwszą praktykę, czyli uruchamianie kontenerów Docker jako użytkownik niebędący administratorem (`non-root`), musisz wprowadzić zmiany zarówno w `Dockerfile`, jak i w `docker-compose.yml`.

Dzięki temu aplikacja nie będzie działać z uprawnieniami administratora wewnątrz kontenera, co ograniczy potencjalne skutki ataku.

## 1. Zmiana w Dockerfile

Przykład dla aplikacji Node.js:

```
# Wybór obrazu bazowego
FROM node:20-alpine

# Katalog roboczy aplikacji
WORKDIR /app

# Kopiowanie plików zależności
COPY package*.json ./

# Instalacja zależności
RUN npm install --omit=dev

# Kopiowanie kodu aplikacji
COPY . .

# Utworzenie użytkownika bez uprawnień administratora
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

# Przypisanie użytkownikowi odpowiednich uprawnień
RUN chown -R appuser:appgroup /app

# Ustawienie użytkownika, jako którego działa aplikacja
USER appuser

# Udostępnienie portu aplikacji
EXPOSE 3000

# Uruchomienie aplikacji
CMD ["node", "server.js"]
```

Najważniejsze instrukcje:

- `addgroup` – tworzy grupę użytkowników `appgroup`.
- `adduser` – tworzy użytkownika `appuser`.
- `chown` – przypisuje użytkownikowi własność katalogu aplikacji.
- `USER appuser` – powoduje, że kolejne instrukcje uruchomieniowe kontenera działają jako `appuser`, a nie `root`.

## 2. Zmiana w docker-compose.yml

W pliku `docker-compose.yml` możesz dodatkowo jawnie określić użytkownika, jako którego uruchamiany jest kontener.

```
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile

    container_name: secure-app

    user: "appuser"

    ports:
      - "3000:3000"

    restart: unless-stopped

    security_opt:
      - no-new-privileges:true
```

Wyjaśnienie:

- `user: "appuser"` – wymusza uruchamianie procesu jako wskazany użytkownik.
- `no-new-privileges:true` – blokuje procesowi możliwość uzyskania dodatkowych uprawnień poprzez mechanizmy systemowe, takie jak setuid.

W tym przykładzie użytkownik `appuser` został wcześniej utworzony w Dockerfile.

## 3. Budowanie i uruchamianie kontenera

Po wprowadzeniu zmian wykonaj:

Budowanie obrazu:

```
docker compose build
```

Uruchomienie kontenera:

```
docker compose up -d
```

Sprawdzenie działającego kontenera:

```
docker ps
```

## 4. Sprawdzenie, czy aplikacja działa jako non-root

Możesz sprawdzić użytkownika, jako którego działa proces wewnątrz kontenera:

```
docker exec secure-app whoami
```

Oczekiwany wynik:

```
appuser
```

Możesz również sprawdzić identyfikator użytkownika:

```
docker exec secure-app id
```

Przykładowy wynik:

```
uid=100(appuser) gid=101(appgroup)
```

Prawidłowo skonfigurowany użytkownik non-root

## 5. Dlaczego to zwiększa bezpieczeństwo?

Porównanie obu rozwiązań:

| Cecha                         | Użytkownik root | Użytkownik non-root |
| ----------------------------- | --------------- | ------------------- |
| Uprawnienia administratora    | Tak             | Nie                 |
| Dostęp do plików systemowych  | Szeroki         | Ograniczony         |
| Możliwość modyfikacji systemu | Duża            | Ograniczona         |
| Ryzyko po przejęciu kontenera | Większe         | Mniejsze            |

## 6. Dodatkowe zalecenia

W środowisku produkcyjnym warto również:

- Nie uruchamiać kontenerów z flagą `--privileged`.
- Ograniczyć dostęp do katalogów hosta montowanych jako wolumeny.
- Nie przyznawać użytkownikowi `appuser` niepotrzebnych uprawnień.
- Rozważyć użycie `read_only: true` w Docker Compose, jeśli aplikacja nie musi zapisywać danych w systemie plików kontenera.

Przykładowo:

```
services:
  app:
    build: .
    user: "appuser"
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
```

Uwaga: `read_only: true` wymaga upewnienia się, że aplikacja nie zapisuje plików w innych katalogach kontenera. Jeśli zapisuje, trzeba odpowiednio skonfigurować wolumeny lub `tmpfs`.

Podsumowanie: Najważniejszą zmianą jest dodanie instrukcji `USER appuser` w Dockerfile. Dzięki temu aplikacja działa z ograniczonymi uprawnieniami. Dodatkowo `user` i `no-new-privileges:true` w Docker Compose wzmacniają kontrolę bezpieczeństwa kontenera.