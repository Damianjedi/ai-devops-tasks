# Zadanie 5

## Prompt 1

Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych.

## Diagram 1

```
+--------+        +--------------------+        +-------------+
| Klient | -----> | Serwer aplikacji   | -----> | Baza danych |
+--------+        +--------------------+        +-------------+
```

## Prompt 2

Dodaj do diagramu opisy elementów i kierunki przepływu danych.

## Diagram 2

```
+-------------------+     1. żądanie HTTP      +----------------------+     2. zapytanie SQL      +------------------+
| KLIENT            | -----------------------> | SERWER APLIKACJI     | -----------------------> | BAZA DANYCH      |
| przeglądarka albo |                          | API, logika          |                          | tabele i rekordy |
| aplikacja mobilna | <----------------------- | biznesowa, port 3000 | <----------------------- |                  |
+-------------------+     4. odpowiedź HTTP    +----------------------+     3. wynik zapytania    +------------------+
```

Przepływ: klient wysyła żądanie HTTP, serwer wykonuje logikę i odpytuje bazę, baza zwraca wynik, serwer odsyła odpowiedź HTTP do klienta.
