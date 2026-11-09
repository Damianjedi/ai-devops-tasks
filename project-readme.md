# Simple Task API

REST API do zarządzania zadaniami, stworzone przy użyciu Node.js, Express i MongoDB.

## Opis

Simple Task API umożliwia zarządzanie zadaniami oraz podstawową autoryzację użytkowników.

Główne funkcje:
- Tworzenie, odczytywanie, aktualizowanie i usuwanie zadań (CRUD).
- Filtrowanie zadań według statusu i priorytetu.
- Podstawowa autoryzacja użytkowników.
- Przechowywanie danych w bazie MongoDB.

### Technologie

- **Node.js** – środowisko uruchomieniowe JavaScript.
- **Express.js** – framework do tworzenia REST API.
- **MongoDB** – baza danych NoSQL.

## Instalacja

### Wymagania

Przed instalacją upewnij się, że masz:
- Node.js (zalecana wersja LTS).
- npm.
- MongoDB (lokalnie lub w chmurze).

### Kroki instalacji

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/username/simple-task-api.git
   ```

2. Przejdź do katalogu projektu:

   ```bash
   cd simple-task-api
   ```

3. Zainstaluj zależności:

   ```bash
   npm install
   ```

4. Utwórz plik `.env` w głównym katalogu projektu:

   ```env
   PORT=3000
   MONGODB_URI=mongodb://localhost:27017/simple-task-api
   JWT_SECRET=your_secret_key
   ```

5. Uruchom aplikację:

   ```bash
   npm start
   ```

   W trybie deweloperskim możesz użyć:

   ```bash
   npm run dev
   ```

API będzie dostępne pod adresem:

`http://localhost:3000`

## Użycie

Do komunikacji z API możesz wykorzystać narzędzia takie jak Postman, Insomnia lub `curl`.

### Przykład tworzenia zadania

**Żądanie:**

```http
POST /api/tasks
Content-Type: application/json
Authorization: Bearer <token>
```

**Treść żądania:**

```json
{
  "title": "Przygotować dokumentację",
  "description": "Utworzyć README projektu",
  "status": "pending",
  "priority": "high"
}
```

### Przykład filtrowania zadań

Pobranie wszystkich zadań o statusie `pending` i priorytecie `high`:

```http
GET /api/tasks?status=pending&priority=high
```

### Autoryzacja

Endpointy wymagające uwierzytelnienia powinny otrzymywać token JWT w nagłówku:

```http
Authorization: Bearer <token>
```

## Endpointy API

Poniżej przedstawiono przykładową strukturę endpointów. Dokładne ścieżki i formaty odpowiedzi należy dostosować do implementacji aplikacji.

| Metoda | Endpoint | Opis |
|---|---|---|
| POST | `/api/auth/register` | Rejestracja użytkownika |
| POST | `/api/auth/login` | Logowanie użytkownika |
| GET | `/api/tasks` | Pobieranie listy zadań |
| GET | `/api/tasks/:id` | Pobieranie zadania według ID |
| POST | `/api/tasks` | Tworzenie nowego zadania |
| PUT | `/api/tasks/:id` | Aktualizacja zadania |
| DELETE | `/api/tasks/:id` | Usuwanie zadania |

### Filtrowanie zadań

Endpoint `GET /api/tasks` obsługuje przykładowe parametry:

| Parametr | Opis | Przykład |
|---|---|---|
| `status` | Filtrowanie według statusu | `?status=completed` |
| `priority` | Filtrowanie według priorytetu | `?priority=high` |

Przykładowe wartości statusu: `pending`, `in-progress`, `completed`.

Przykładowe wartości priorytetu: `low`, `medium`, `high`.

---

## Licencja

Projekt przeznaczony do celów edukacyjnych i demonstracyjnych. W razie potrzeby dodaj plik `LICENSE` z wybraną licencją.