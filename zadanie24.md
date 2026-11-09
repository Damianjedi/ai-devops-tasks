Metryki serwera API (ostatnie 24h):
- Średni czas odpowiedzi: 230ms
- 95 percentyl czasu odpowiedzi: 450ms
- 99 percentyl czasu odpowiedzi: 1200ms
- Liczba zapytań: 15,000
- Liczba błędów 5xx: 120
- Użycie CPU: średnio 45%, max 80%
- Użycie pamięci: średnio 2.1GB, max 3.5GB (z 4GB dostępnych)


# Analiza metryk serwera API – ostatnie 24 godziny

Na podstawie przedstawionych danych serwer działa stosunkowo dobrze pod względem średniego obciążenia CPU, ale widoczne są potencjalne problemy z czasem odpowiedzi, błędami serwera 5xx oraz wykorzystaniem pamięci RAM.

Najbardziej niepokojące są wolne odpowiedzi dla części zapytań oraz wysoki maksymalny poziom wykorzystania pamięci.

## 1. Interpretacja poszczególnych metryk

### Czas odpowiedzi API

| Metryka                | Wynik   | Interpretacja                              |
| ---------------------- | ------- | ------------------------------------------ |
| Średni czas odpowiedzi | 230 ms  | Umiarkowany, potencjalnie akceptowalny.    |
| 95. percentyl (P95)    | 450 ms  | 95% zapytań kończy się w czasie do 450 ms. |
| 99. percentyl (P99)    | 1200 ms | 1% zapytań trwa ponad 1,2 sekundy.         |



Średnia: 230 ms

P99: 1200 ms



Co to oznacza?

Średni czas odpowiedzi wynoszący 230 ms wygląda całkiem dobrze. Jednak P99 na poziomie 1200 ms wskazuje, że niektóre zapytania są znacznie wolniejsze od pozostałych.

Może to oznaczać:

- nieoptymalne zapytania do bazy danych;
- brak odpowiednich indeksów;
- przeciążenie serwera w określonych momentach;
- problemy z zewnętrznymi usługami API;
- blokowanie operacji przez synchroniczne zadania.

Warto sprawdzić, które endpointy odpowiadają za najwolniejsze zapytania.

### Liczba błędów 5xx

# 0,8%

Do zbadania

Obliczenie:

\\[ \frac{120}{15000}\times 100 = 0{,}8\\% \\]

Oznacza to, że na 15 000 zapytań wystąpiło 120 błędów serwera.

Błędy 5xx wskazują na problemy po stronie serwera lub infrastruktury. Przykładowo:

- `500 Internal Server Error` – nieoczekiwany błąd aplikacji;
- `502 Bad Gateway` – problem z komunikacją między serwerami;
- `503 Service Unavailable` – usługa niedostępna lub przeciążona;
- `504 Gateway Timeout` – przekroczenie czasu oczekiwania na odpowiedź.

Moja sugestia: należy sprawdzić logi aplikacji i ustalić, które kody 5xx występują najczęściej, na jakich endpointach i w jakich godzinach.

### Wykorzystanie CPU

| Metryka               | Wynik |
| --------------------- | ----- |
| Średnie użycie CPU    | 45%   |
| Maksymalne użycie CPU | 80%   |

Umiarkowane obciążenie

Średnie wykorzystanie procesora wynoszące 45% nie wskazuje na stałe przeciążenie.

Maksymalna wartość 80% może jednak oznaczać krótkotrwałe skoki obciążenia, np. podczas:

- wykonywania kosztownych zapytań;
- generowania raportów;
- przetwarzania dużych ilości danych;
- obsługi wielu równoczesnych żądań.

Na ten moment nie ma wystarczających danych, aby uznać CPU za główne źródło problemów.

### Wykorzystanie pamięci RAM

| Metryka                   | Wynik  |
| ------------------------- | ------ |
| Średnie użycie pamięci    | 2,1 GB |
| Maksymalne użycie pamięci | 3,5 GB |
| Dostępna pamięć           | 4 GB   |

Wysokie maksymalne wykorzystanie

Maksymalne wykorzystanie pamięci wynosi:

\\[ \frac{3{,}5}{4}\times 100 = 87{,}5\\% \\]

Serwer wykorzystuje momentami aż 87,5% dostępnej pamięci RAM. Pozostaje tylko 0,5 GB zapasu.

Może to prowadzić do:

- częstszego uruchamiania garbage collectora;
- spadku wydajności aplikacji;
- błędów związanych z brakiem pamięci;
- restartów procesu Node.js lub kontenera;
- problemów przy jednoczesnym zwiększeniu ruchu.

Warto sprawdzić, czy aplikacja nie ma wycieków pamięci (memory leaks), np. przez niekontrolowane przechowywanie danych w tablicach, cache lub zmiennych globalnych.

## 2. Podsumowanie potencjalnych problemów

| Obszar                 | Ocena                                  | Priorytet |
| ---------------------- | -------------------------------------- | --------- |
| Średni czas odpowiedzi | Akceptowalny                           | Niski     |
| P95 i P99              | Możliwe problemy z wolnymi zapytaniami | Wysoki    |
| Błędy 5xx              | 0,8% wszystkich żądań                  | Wysoki    |
| CPU                    | Brak oznak stałego przeciążenia        | Średni    |
| Pamięć RAM             | Maksymalnie 87,5% wykorzystania        | Wysoki    |

## 3. Rekomendacje dotyczące poprawy wydajności

### 1. Optymalizacja zapytań do bazy danych

Jeśli API korzysta z MongoDB, warto:

- przeanalizować najwolniejsze zapytania;
- dodać indeksy dla często filtrowanych pól;
- unikać pobierania niepotrzebnych danych;
- stosować paginację wyników;
- wykorzystać `explain()` do analizy planów zapytań.

Przykład indeksu:

```
db.tasks.createIndex({ status: 1, priority: 1 });
```

### 2. Wprowadzenie cache

Warto zastosować Redis lub inny mechanizm cache dla często pobieranych danych.

Przykładowe zastosowania:

- lista zadań;
- dane użytkowników;
- konfiguracja aplikacji;
- dane, które rzadko się zmieniają.

Pozwoli to ograniczyć liczbę zapytań do bazy danych i skrócić czas odpowiedzi API.

### 3. Monitorowanie i optymalizacja pamięci

W przypadku Node.js warto:

- monitorować wykorzystanie heap;
- analizować garbage collection;
- sprawdzać, czy nie występują memory leaks;
- usuwać niepotrzebne referencje do dużych obiektów;
- ograniczać wielkość cache.

Przykładowe monitorowanie pamięci:

```
setInterval(() => {
  const memory = process.memoryUsage();

  console.log({
    heapUsed: `${(memory.heapUsed / 1024 / 1024).toFixed(2)} MB`,
    heapTotal: `${(memory.heapTotal / 1024 / 1024).toFixed(2)} MB`,
    rss: `${(memory.rss / 1024 / 1024).toFixed(2)} MB`
  });
}, 10000);
```

### 4. Analiza błędów 5xx

Należy przeanalizować logi serwera i ustalić przyczyny błędów.

Przydatne działania:

- rejestrowanie wyjątków i stack trace;
- identyfikowanie endpointów generujących błędy;
- monitorowanie błędów połączenia z bazą danych;
- dodanie odpowiedniej obsługi wyjątków;
- zastosowanie timeoutów dla zewnętrznych usług.

Warto również wdrożyć mechanizm alertów, np. gdy liczba błędów 5xx przekroczy ustalony próg.

### 5. Testy obciążeniowe

Warto wykorzystać narzędzia takie jak:

- k6
- Apache JMeter
- Artillery

Pozwolą one sprawdzić, jak API zachowuje się przy zwiększonej liczbie jednoczesnych użytkowników.

## 4. Proponowana kolejność działań

1. Przeanalizować błędy 5xx

   Ustalić ich przyczyny, częstotliwość i endpointy, których dotyczą.
2. Zbadać wolne zapytania

   Zidentyfikować operacje odpowiedzialne za wysokie wartości P95 i P99.
3. Zoptymalizować wykorzystanie pamięci

   Sprawdzić heap, garbage collection i potencjalne wycieki pamięci.
4. Wprowadzić cache i indeksy

   Ograniczyć niepotrzebne operacje na bazie danych.
5. Przeprowadzić testy obciążeniowe

   Zweryfikować efekty zmian i odporność API na większy ruch.

## 5. Wnioski końcowe

Serwer nie wykazuje obecnie jednoznacznych oznak stałego przeciążenia procesora. Jednak trzy obszary wymagają uwagi:

1. P99 = 1200 ms – część zapytań odpowiada zbyt wolno w porównaniu ze średnią.
2. Błędy 5xx = 0,8% – należy znaleźć i wyeliminować przyczyny błędów.
3. RAM = 87,5% maksymalnego wykorzystania – niewielki zapas pamięci może powodować problemy przy wzroście obciążenia.

Moja rekomendacja: w pierwszej kolejności zbadałbym błędy 5xx i najwolniejsze endpointy, a następnie przeprowadził profilowanie pamięci. Nie zwiększałbym od razu zasobów serwera, ponieważ najpierw warto ustalić, czy problem wynika z nieoptymalnego kodu, zapytań do bazy danych czy ograniczeń infrastruktury.