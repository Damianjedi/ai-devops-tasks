Tak! Obecny kod można zoptymalizować. Wykorzystuje on dwie zagnieżdżone pętle `for`, przez co jego złożoność czasowa wynosi O(n²). Przy dużych listach może to powodować znaczne spowolnienie działania programu.

### 1. Zoptymalizowana wersja kodu

Możemy wykorzystać strukturę danych `set` (zbiór), która pozwala bardzo szybko sprawdzać, czy dany element już wystąpił.

```
def find_duplicates(list_of_items):    seen = set()    duplicates = set()    for item in list_of_items:        if item in seen:            duplicates.add(item)        else:            seen.add(item)    return list(duplicates)
```

### 2. Jak działa zoptymalizowany kod?

- `seen` – przechowuje elementy, które już zostały napotkane.
- `duplicates` – przechowuje wykryte duplikaty.
- `if item in seen` – sprawdza, czy element wystąpił już wcześniej.
- `duplicates.add(item)` – dodaje element do zbioru duplikatów.
- `seen.add(item)` – zapisuje nowo napotkany element.

Dzięki zastosowaniu zbiorów `set` sprawdzanie obecności elementów jest średnio wykonywane w czasie O(1).

### 3. Porównanie wydajności

| Cecha                | Oryginalny kod | Zoptymalizowany kod |
| -------------------- | -------------- | ------------------- |
| Złożoność czasowa    | O(n²)          | O(n) średnio        |
| Złożoność pamięciowa | O(n)           | O(n)                |
| Zagnieżdżone pętle   | Tak            | Nie                 |
| Wykorzystanie `set`  | Nie            | Tak                 |

### 4. Przykład działania

```
numbers = [1, 2, 3, 2, 4, 5, 1, 3]print(find_duplicates(numbers))
```

Przykładowy wynik:

```
[1, 2, 3]
```

Kolejność elementów w wyniku może być różna, ponieważ zbiory `set` nie gwarantują zachowania kolejności w taki sposób jak listy.

### 5. Wersja zachowująca kolejność duplikatów

Jeśli zależy nam na zachowaniu kolejności występowania duplikatów, możemy zastosować następujące rozwiązanie:

```
def find_duplicates(list_of_items):    seen = set()    duplicates = []    duplicates_set = set()    for item in list_of_items:        if item in seen and item not in duplicates_set:            duplicates.append(item)            duplicates_set.add(item)        else:            seen.add(item)    return duplicates
```

Przykład:

```
numbers = [1, 2, 3, 2, 4, 1, 5, 3]print(find_duplicates(numbers))
```

Wynik:

```
[2, 1, 3]
```

### Podsumowanie

Najważniejszą optymalizacją jest zastąpienie zagnieżdżonych pętli strukturą `set`. Pozwala to zmniejszyć średnią złożoność czasową z O(n²) do O(n).

W praktyce oznacza to znacznie szybsze działanie programu, szczególnie podczas przetwarzania dużych zbiorów danych.

Uwaga: rozwiązania wykorzystujące `set` wymagają, aby elementy listy były hashowalne (np. liczby, napisy lub krotki zawierające hashowalne elementy).