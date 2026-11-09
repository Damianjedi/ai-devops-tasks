## Analiza złożoności algorytmu `findPairs`

### 1. Złożoność czasowa pierwotnego algorytmu

Pierwotna implementacja wykorzystuje dwie zagnieżdżone pętle `for`.

- Pętla zewnętrzna przechodzi przez wszystkie elementy tablicy.
- Pętla wewnętrzna sprawdza kolejne elementy, które znajdują się za aktualnym elementem.
- Dla każdej pary elementów wykonywane jest sprawdzenie, czy ich suma jest równa `targetSum`.

Liczba porównań wynosi:

\\[ \frac{n(n-1)}{2} \\]

Gdzie `n` oznacza liczbę elementów tablicy.



O(n²)

&#x20;Złożoność czasowa



Oznacza to, że wraz ze wzrostem liczby elementów czas wykonywania algorytmu rośnie kwadratowo.

Przykładowo:

- 10 elementów – 45 porównań.
- 100 elementów – 4950 porównań.
- 1000 elementów – 499 500 porównań.

### 2. Złożoność pamięciowa pierwotnego algorytmu

Algorytm przechowuje znalezione pary w tablicy `pairs`.

W najgorszym przypadku, gdy wiele kombinacji spełnia warunek, liczba zapisanych par może wynosić:

\\[ O(n^2) \\]

Sama pamięć pomocnicza, nieuwzględniająca tablicy wynikowej, wynosi O(1), ponieważ algorytm nie tworzy dodatkowych struktur danych.

### 3. Opis optymalizacji

Aby poprawić wydajność, można zastąpić dwie zagnieżdżone pętle pojedynczą pętlą i wykorzystać strukturę danych `Set`.

Zasada działania:

1. Utworzenie pustego zbioru `seen`.
2. Przejście przez elementy tablicy.
3. Obliczenie brakującej wartości:

\\[ complement = targetSum - num \\]

4. Sprawdzenie, czy brakująca wartość znajduje się już w zbiorze.
5. Jeśli tak, dodanie znalezionej pary do tablicy wynikowej.
6. Dodanie aktualnej liczby do zbioru.

Dzięki temu nie trzeba porównywać każdego elementu ze wszystkimi pozostałymi.

### 4. Złożoność zoptymalizowanego algorytmu

| Rodzaj złożoności          | Pierwotny algorytm | Zoptymalizowany algorytm |
| -------------------------- | ------------------ | ------------------------ |
| Czasowa                    | O(n²)              | O(n) średnio             |
| Pamięciowa pomocnicza      | O(1)               | O(n)                     |
| Pamięciowa wraz z wynikiem | O(n²)              | O(n²)                    |

Warto zaznaczyć, że operacje `Set.has()` i `Set.add()` mają średnio złożoność O(1), dlatego przejście przez całą tablicę zajmuje średnio O(n).

### 5. Wnioski

Zastosowanie struktury `Set` pozwala znacząco poprawić wydajność algorytmu. Zamiast kwadratowej złożoności czasowej otrzymujemy liniową złożoność średnią.

Najważniejsze korzyści optymalizacji:

- zmniejszenie liczby operacji;
- wyeliminowanie zagnieżdżonych pętli;
- szybsze wyszukiwanie brakujących wartości;
- lepsza wydajność dla dużych tablic.

Kompromis: Optymalizacja wymaga dodatkowej pamięci na przechowywanie odwiedzonych elementów. Mimo tego rozwiązanie z `Set` jest zazwyczaj znacznie korzystniejsze dla dużych zbiorów danych.