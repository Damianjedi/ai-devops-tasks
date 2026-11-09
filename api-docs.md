Poniżej znajduje się kompletna dokumentacja endpointu `GET /api/users` w formacie Markdown.

# GET /api/users

## 1. Opis endpointu

Endpoint `GET /api/users` służy do pobierania listy użytkowników systemu.

Obsługuje paginację wyników oraz filtrowanie użytkowników według ich roli. Dzięki temu możliwe jest pobieranie danych partiami oraz ograniczenie wyników do określonej grupy użytkowników.

## 2. Parametry zapytania (Query Parameters)

| Parametr | Typ     | Wymagany | Domyślna wartość | Opis                                                       |
| -------- | ------- | -------- | ---------------- | ---------------------------------------------------------- |
| `page`   | Integer | Nie      | `1`              | Numer strony wyników.                                      |
| `limit`  | Integer | Nie      | `10`             | Liczba użytkowników na stronie. Maksymalna wartość: `100`. |
| `role`   | String  | Nie      | Brak             | Filtruje użytkowników według przypisanej roli.             |

### Szczegóły parametrów

- **page** – określa numer strony, od której mają zostać pobrane wyniki. Numer strony musi być większy lub równy 1.
- **limit** – określa maksymalną liczbę użytkowników zwracanych w jednym żądaniu. Wartość nie może przekraczać 100.
- **role** – pozwala pobrać użytkowników posiadających określoną rolę, np. `admin`, `user` lub `moderator`.

## 3. Przykładowe żądanie

Pobranie pierwszych 10 użytkowników:

```
GET /api/users HTTP/1.1
Host: example.com
Accept: application/json
```

Pobranie drugiej strony z 20 użytkownikami:

```
GET /api/users?page=2&limit=20
```

Pobranie użytkowników z rolą administratora:

```
GET /api/users?role=admin
```

Pobranie drugiej strony administratorów (maksymalnie 50 wyników):

```
GET /api/users?page=2&limit=50&role=admin
```

## 4. Przykładowa odpowiedź

**Kod HTTP: `200 OK`**

```
{
  "data": [
    {
      "id": 1,
      "name": "Jan Kowalski",
      "email": "jan@example.com",
      "role": "admin"
    },
    {
      "id": 2,
      "name": "Anna Nowak",
      "email": "anna@example.com",
      "role": "user"
    },
    {
      "id": 3,
      "name": "Piotr Wiśniewski",
      "email": "piotr@example.com",
      "role": "moderator"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 3,
    "totalPages": 1
  }
}
```

### Opis pól odpowiedzi

| Pole                    | Typ     | Opis                                                         |
| ----------------------- | ------- | ------------------------------------------------------------ |
| `data`                  | Array   | Tablica zawierająca listę użytkowników.                      |
| `data[].id`             | Integer | Unikalny identyfikator użytkownika.                          |
| `data[].name`           | String  | Imię i nazwisko użytkownika.                                 |
| `data[].email`          | String  | Adres e-mail użytkownika.                                    |
| `data[].role`           | String  | Rola użytkownika w systemie.                                 |
| `pagination.page`       | Integer | Aktualny numer strony.                                       |
| `pagination.limit`      | Integer | Maksymalna liczba wyników na stronie.                        |
| `pagination.total`      | Integer | Łączna liczba użytkowników spełniających kryteria zapytania. |
| `pagination.totalPages` | Integer | Łączna liczba stron wyników.                                 |

## 5. Kody odpowiedzi HTTP

| Kod   | Nazwa                 | Opis                                                                                  |
| ----- | --------------------- | ------------------------------------------------------------------------------------- |
| `200` | OK                    | Żądanie zakończone sukcesem.                                                          |
| `400` | Bad Request           | Nieprawidłowe parametry zapytania, np. ujemny numer strony lub limit większy niż 100. |
| `401` | Unauthorized          | Użytkownik nie jest uwierzytelniony (jeśli endpoint wymaga uwierzytelnienia).         |
| `403` | Forbidden             | Użytkownik nie ma uprawnień do pobierania listy użytkowników.                         |
| `500` | Internal Server Error | Wystąpił wewnętrzny błąd serwera.                                                     |

## 6. Przykładowa odpowiedź w przypadku błędu

**Kod HTTP: `400 Bad Request`**

```
{
  "error": "Invalid query parameters",
  "message": "The limit parameter must be between 1 and 100."
}
```

## 7. Podsumowanie

Endpoint `GET /api/users` umożliwia:

- Pobieranie listy użytkowników.
- Paginację wyników za pomocą parametrów `page` i `limit`.
- Filtrowanie użytkowników według roli za pomocą parametru `role`.
- Kontrolowanie liczby zwracanych wyników (maksymalnie 100).

**Metoda HTTP:** `GET`

**Ścieżka:** `/api/users`

**Format odpowiedzi:** `JSON`

**Domyślne ustawienia:** `page=1`, `limit=10`.

