W tym pliku są dwa błędy składni. Przy app brakuje dwukropka po ports, a hasło Postgresa jest zapisane jak polecenie w powłoce, a nie jako para klucz–wartość.

Poprawiona wersja:


services:
  web:
    image: nginx
    ports:
      - "80:80"
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: password
ports: musi być kluczem mapy, tak jak przy usłudze web. W environment Compose oczekuje mapy KLUCZ: wartość (albo listy w postaci - POSTGRES_PASSWORD=password). Bez POSTGRES_PASSWORD obraz postgres i tak nie wystartuje.