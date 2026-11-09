Poniżej znajduje się przykład prostego testu jednostkowego dla funkcji `sum(a, b)` z wykorzystaniem frameworka Jest w projekcie Node.js.

## 1. Czym jest Jest?

Jest to popularny framework do testowania kodu JavaScript. Jest wykorzystywany do tworzenia i uruchamiania testów jednostkowych (unit tests).

Jego najważniejsze zalety:

- Prosta konfiguracja i obsługa.
- Automatyczne wykrywanie plików testowych.
- Wbudowane funkcje sprawdzające wyniki (np. `expect`).
- Możliwość testowania funkcji, klas i modułów.
- Czytelne raporty z wykonanych testów.

## 2. Instalacja Jest w projekcie

W terminalu, w głównym katalogu projektu Node.js, wykonaj polecenie:

```
npm install --save-dev jest
```

Następnie w pliku `package.json` dodaj skrypt uruchamiający testy:

```
{
  "scripts": {
    "test": "jest"
  }
}
```

Dzięki temu testy będzie można uruchamiać za pomocą polecenia `npm test`.

## 3. Struktura plików projektu

Przykładowa struktura projektu:

```
my-project/
│
├── node_modules/
│
├── src/
│   └── sum.js
│
├── tests/
│   └── sum.test.js
│
├── package.json
├── package-lock.json
└── .gitignore
```

- `src/sum.js` – plik zawierający funkcję do przetestowania.
- `tests/sum.test.js` – plik zawierający test jednostkowy.
- `package.json` – konfiguracja projektu i zależności.
- `node_modules/` – zainstalowane biblioteki.

## 4. Implementacja funkcji

W pliku `src/sum.js` umieszczamy funkcję:

```
function sum(a, b) {
  return a + b;
}

module.exports = sum;
```

`module.exports` umożliwia wykorzystanie funkcji w innych plikach projektu.

## 5. Napisanie testu jednostkowego

W pliku `tests/sum.test.js` umieszczamy następujący kod:

```
const sum = require('../src/sum');

test('dodaje dwie liczby', () => {
  expect(sum(2, 3)).toBe(5);
});
```

Wyjaśnienie poszczególnych elementów:

- `require('../src/sum')` – importuje testowaną funkcję.
- `test()` – definiuje pojedynczy test jednostkowy.
- `expect(sum(2, 3))` – wykonuje funkcję i sprawdza otrzymany wynik.
- `.toBe(5)` – sprawdza, czy wynik jest równy liczbie 5.

## 6. Uruchomienie testu

W terminalu, w głównym katalogu projektu, wpisujemy:

```
npm test
```

Jest automatycznie wyszuka pliki testowe, w tym `sum.test.js`, i wykona zapisane w nich testy.

Przykładowy wynik:

Test zakończony pomyślnie

PASS

```
PASS tests/sum.test.js

✓ dodaje dwie liczby

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
```

Oznacza to, że funkcja `sum(2, 3)` zwróciła oczekiwany wynik `5`.

## 7. Podsumowanie

Jest pozwala automatycznie sprawdzać poprawność działania funkcji JavaScript. Dzięki testom jednostkowym można szybko wykrywać błędy, sprawdzać wyniki działania kodu i upewniać się, że wprowadzane zmiany nie powodują problemów w istniejących funkcjonalnościach.

W przedstawionym przykładzie przetestowaliśmy funkcję dodawania dwóch liczb, sprawdzając, czy zwraca prawidłowy wynik.