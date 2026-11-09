^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$

Fragment	Znaczenie
^	Początek tekstu.
25[0-5]	Liczby od 250 do 255.
2[0-4][0-9]	Liczby od 200 do 249.
1[0-9]{2}	Liczby od 100 do 199.
[1-9]?[0-9]	Liczby od 0 do 99.
\.	Dosłowna kropka.
{3}	Powtórzenie poprzedniej grupy trzy razy.
$	Koniec tekstu.

Dzięki temu wzorzec:
- wymaga dokładnie czterech segmentów;
- dopuszcza wyłącznie wartości od 0 do 255;
- wymaga kropek jako separatorów;
- odrzuca dodatkowe znaki i zera wiodące, np. 01.
3. Przykłady testów
Adres IPv4	Wynik	Powód
192.168.1.1	Poprawny	Prawidłowy adres.
10.0.0.1	Poprawny	Wszystkie segmenty są w zakresie.
255.255.255.255	Poprawny	Maksymalna wartość każdego segmentu.
0.0.0.0	Poprawny	Minimalna wartość każdego segmentu.
256.1.1.1	Niepoprawny	256 przekracza dozwolony zakres.
192.168.1	Niepoprawny	Brakuje jednego segmentu.
192.168.1.300	Niepoprawny	300 przekracza zakres.
192.168.-1.1	Niepoprawny	Niedozwolony znak minus.
192.168.1.1.1	Niepoprawny	Pięć segmentów zamiast czterech.
192.168.01.1	Niepoprawny	Zero wiodące.