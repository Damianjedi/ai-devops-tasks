1.Znalezione błędy i poprawki
Błąd	Dlaczego jest problemem?	Jak naprawiono?
stesp zamiast steps	Jenkins nie rozpoznaje takiego bloku. Pipeline zakończy się błędem składni.	Zmieniono na steps.
npm build	To nie jest standardowa komenda npm do uruchamiania skryptu budowania projektu.	Zmieniono na npm run build.
docker build -t myapp .	Obraz otrzymuje tag myapp, a nie myapp:latest.	Dodano jawny tag :latest.
docker push myapp:latest	Wcześniej budowany obraz miał inną nazwę/tag.	Ujednolicono nazwę obrazu podczas budowania i publikowania.
when umieszczone po steps	W Declarative Pipeline warunek powinien znajdować się bezpośrednio wewnątrz stage, przed steps.	Przeniesiono when przed steps.
Brak końcowej klamry }	Pipeline nie jest poprawnie zamknięty.	Dodano brakującą klamrę.

2. Dodatkowe zalecenia
Warto rozważyć jeszcze kilka ulepszeń:

1. Użycie npm ci zamiast npm install

Jeśli projekt posiada plik package-lock.json, lepiej użyć:
sh 'npm ci'


Ta komenda instaluje zależności zgodnie z plikiem blokady, co zapewnia bardziej powtarzalne wyniki w środowisku CI.

2. Publikowanie obrazu do Docker Hub

Samo myapp:latest nie wskazuje konkretnego repozytorium Docker Hub. W praktyce należy użyć nazwy użytkownika lub organizacji:
sh 'docker build -t username/myapp:latest .'
sh 'docker push username/myapp:latest'


Do publikowania obrazu potrzebne jest również uwierzytelnienie, najlepiej przez Jenkins Credentials.

3. Używanie unikalnych tagów

Zamiast publikować wyłącznie latest, można wykorzystać numer kompilacji:
sh "docker build -t username/myapp:${BUILD_NUMBER} ."
sh "docker push username/myapp:${BUILD_NUMBER}"


Dzięki temu łatwiej ustalić, która wersja aplikacji została wdrożona.
4. Podsumowanie
Najważniejsze poprawki to:
- stesp → steps.
- npm build → npm run build.
- Ujednolicenie tagu obrazu Docker.
- Przeniesienie when przed steps.
- Dodanie brakującej klamry zamykającej.