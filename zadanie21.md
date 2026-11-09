## Opis procesu konwersji JSON do CSV

Konwersja danych z formatu JSON do CSV polega na przekształceniu struktury obiektów JSON w tabelę, w której każdy obiekt reprezentuje jeden wiersz, a jego właściwości stają się kolumnami.

W przedstawionym przykładzie dane zawierają tablicę `users`, w której znajdują się dwa obiekty użytkowników.

### 1. Etapy konwersji

Krok 1. Analiza struktury JSON

Najpierw należy zidentyfikować:

- główną tablicę `users`;
- właściwości każdego użytkownika: `id`, `name`, `email`, `roles`;
- typy danych poszczególnych właściwości.

Krok 2. Utworzenie nagłówków CSV

Nazwy właściwości obiektów stają się nazwami kolumn:

```
id,name,email,roles
```

Krok 3. Przekształcenie obiektów w wiersze

Każdy obiekt z tablicy `users` zostaje przekształcony w osobny wiersz CSV.

Krok 4. Obsługa tablicy `roles`

Właściwość `roles` jest tablicą, a CSV nie obsługuje bezpośrednio zagnieżdżonych struktur ani tablic. Dlatego trzeba wybrać sposób jej reprezentacji.

W tym przypadku role zostały połączone średnikiem:

```
1,Jan Kowalski,jan@example.com,admin;user
2,Anna Nowak,anna@example.com,user
```

### 2. Potencjalne wyzwania

| Wyzwanie             | Opis                                                                      | Możliwe rozwiązanie                                     |
| -------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------- |
| Tablice              | CSV nie obsługuje tablic bezpośrednio.                                    | Połączenie elementów separatorem, np. `;`.              |
| Zagnieżdżone obiekty | JSON może zawierać obiekty wewnątrz innych obiektów.                      | Spłaszczenie struktury lub osobne pliki CSV.            |
| Znaki specjalne      | Przecinki, cudzysłowy i znaki nowej linii mogą zaburzyć strukturę CSV.    | Ujęcie wartości w cudzysłowy i odpowiednie escapowanie. |
| Brakujące wartości   | Niektóre obiekty mogą nie zawierać wszystkich właściwości.                | Pozostawienie pustej komórki.                           |
| Różne typy danych    | JSON obsługuje liczby, tekst, wartości logiczne i `null`.                 | Ustalenie spójnego sposobu zapisu wartości.             |
| Kodowanie znaków     | Polskie znaki mogą być nieprawidłowo wyświetlane w niektórych programach. | Zapis pliku w kodowaniu UTF-8.                          |

### 3. Alternatywne sposoby reprezentacji tablicy `roles`

Istnieje kilka sposobów zapisania tablicy ról w CSV.

Metoda A – połączenie średnikiem

```
id,name,email,roles
1,Jan Kowalski,jan@example.com,admin;user
2,Anna Nowak,anna@example.com,user
```

Zalety:

- prosta implementacja;
- niewielka liczba kolumn;
- czytelny zapis.

Wada: podczas odczytu trzeba ponownie podzielić wartość według średnika.

Metoda B – osobne kolumny dla ról

```
id,name,email,role1,role2
1,Jan Kowalski,jan@example.com,admin,user
2,Anna Nowak,anna@example.com,user,
```

Zaleta: łatwe filtrowanie w arkuszach kalkulacyjnych.

Wada: liczba kolumn zależy od maksymalnej liczby ról.

Metoda C – osobny wiersz dla każdej roli

```
id,name,email,role
1,Jan Kowalski,jan@example.com,admin
1,Jan Kowalski,jan@example.com,user
2,Anna Nowak,anna@example.com,user
```

Zaleta: wygodne filtrowanie, sortowanie i analizowanie danych.

Wada: dane użytkownika powtarzają się w kilku wierszach.

### 4. Która metoda jest najlepsza?

Wybór zależy od przeznaczenia pliku:

- Prosty eksport danych: metoda A – średnik jako separator ról.
- Analiza w Excelu: metoda B – osobne kolumny.
- Import do bazy danych i dalsze przetwarzanie: metoda C – osobny wiersz dla każdej roli.

Warto również pamiętać, że jeśli wartości mogą zawierać przecinki, cudzysłowy lub znaki nowej linii, należy stosować standardowe zasady escapowania CSV, np. zgodne z RFC 4180.

### 5. Podsumowanie

Konwersja JSON do CSV wymaga nie tylko zmiany formatu, ale również podjęcia decyzji dotyczących reprezentacji bardziej złożonych danych.

W przedstawionym przykładzie połączenie ról średnikiem jest prostym i czytelnym rozwiązaniem. Jeśli jednak dane mają być później filtrowane lub przetwarzane automatycznie, warto rozważyć osobny wiersz dla każdej roli.