Skrypt sprawdza, czy Docker odpowiada, a gdy milczy, próbuje go włączyć i sprawdza jeszcze raz.


#!/usr/bin/env bash
Pierwsza linia mówi systemowi, że plik ma wykonać program bash. Dzięki temu po nadaniu praw do uruchomienia (chmod +x check-docker.sh) wystarczy wpisać ./check-docker.sh.


if docker info >/dev/null 2>&1; then
docker info pyta demona Dockera o stan. To prawdziwy test „czy usługa żyje”, a nie tylko „czy komenda docker jest zainstalowana”. >/dev/null wyrzuca zwykły tekst odpowiedzi, a 2>&1 dokleja do niego komunikaty błędów, więc na ekranie nic z tego polecenia nie widać. if patrzy tylko na wynik: kod 0 oznacza sukces i wejście do tej gałęzi.


  echo "Docker działa."
  exit 0
fi
Gdy Docker już działa, skrypt wypisuje komunikat i kończy się kodem 0, czyli „wszystko w porządku”. fi zamyka blok if. Dalsze linie się nie wykonują.


echo "Docker nie działa. Próba uruchomienia..."
sudo systemctl start docker
Do tego miejsca skrypt dochodzi tylko wtedy, gdy docker info się nie udało. Wypisuje informację, a potem sudo systemctl start docker prosi system o uruchomienie usługi docker. sudo jest potrzebne, bo włączanie usług wymaga uprawnień administratora. systemctl działa na Linuksie ze systemd.


if docker info >/dev/null 2>&1; then
  echo "Docker został uruchomiony."
else
  echo "Nie udało się uruchomić Dockera." >&2
  exit 1
fi
Skrypt pyta Dockera drugi raz. Jeśli teraz odpowiada, wypisuje sukces. Jeśli nadal nie odpowiada, wypisuje błąd na stderr (>&2, osobny kanał na błędy) i kończy się kodem 1, czyli „coś poszło nie tak”. Inny program albo pipeline może po tym kodzie poznać, że uruchomienie się nie udało.