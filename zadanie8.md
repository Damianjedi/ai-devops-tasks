ERROR: for app  Cannot start service app: driver failed programming external connectivity on endpoint app (172.18.0.2): Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use


Port 3000 na twoim komputerze jest już zajęty, więc Docker nie może podpiąć pod niego kontenera app. Kontener w sieci Dockera dostał adres 172.18.0.2, ale publikacja portu na hoście (0.0.0.0:3000) się nie udała.

Najpierw sprawdź, kto trzyma ten port:


netstat -ano | findstr :3000
Ostatnia kolumna to identyfikator procesu. Często jest to poprzedni kontener albo lokalny npm start.

Zatrzymaj to, co zajmuje port. Jeśli to inny kontener:


docker ps
docker stop <nazwa-lub-id>
Potem uruchom usługę ponownie.

Albo opublikuj aplikację na wolnym porcie hosta, bez zmiany portu wewnątrz kontenera. W Compose zamiast 3000:3000 ustaw na przykład:


ports:
  - "3001:3000"
Aplikacja dalej słucha na 3000 w kontenerze, a z przeglądarki wchodzisz na http://localhost:3001.