Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

Duże zużycie pamięci ogranicza się limitem kontenera i sprawdza, czy rośnie przez wyciek w aplikacji, czy przez zbyt duży przydział.

Limit w Dockerze. Bez limitu kontener może zająć całą pamięć hosta. Ustaw sufit przy starcie:


docker run -m 512m --memory-swap 512m moja-app
W Compose:


services:
  app:
    image: moja-app
    mem_limit: 512m
Gdy proces przekroczy limit, jądro go zakończy (OOM). To chroni hosta, ale nie naprawia samej aplikacji.

Ustal, co zjada pamięć. docker stats pokazuje bieżące zużycie. Jeśli wartość stale rośnie przy stałym ruchu, to zwykle wyciek w aplikacji, a nie sam Docker. Dla Node.js warto też ograniczyć stertę, żeby proces padł kontrolowanie, zanim zabierze cały limit:


NODE_OPTIONS=--max-old-space-size=384
Co zwykle obniża zużycie. Mniej replik i workerów niż liczba rdzeni, jeden proces na kontener, obraz node:18-alpine zamiast pełnego Debiana oraz usunięcie zbędnych zależności z npm install. Restart kontenera tylko na chwilę zwalnia pamięć — jeśli po godzinie wraca do tego samego poziomu, trzeba szukać wycieku w kodzie (rosnące cache, otwarte połączenia, nasłuchiwacze zdarzeń).


Jesteś doświadczonym DevOps Engineerem z 10-letnim doświadczeniem. Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

Najpierw zmierz, co naprawdę rośnie, a dopiero potem ustawiaj limit. Sam limit chroni hosta, ale nie usuwa przyczyny.

1. Potwierdź objaw. docker stats pokazuje zużycie na żywo. W docker inspect pole State.OOMKilled: true oznacza, że jądro zabiło proces po przekroczeniu limitu cgroup. W logach jądra (dmesg albo journalctl -k) widać wpis o zabiciu procesu. Jeśli pamięć rośnie liniowo przy stałym ruchu i spada dopiero po restarcie, to wyciek w aplikacji. Jeśli skacze przy starcie i się stabilizuje, to za duży baseline (za dużo workerów, za duży heap, za ciężki obraz z niepotrzebnymi procesami).

2. Ogranicz kontener, zanim zje hosta.


docker run -m 512m --memory-reservation 256m --memory-swap 512m moja-app
-m to twardy sufit. --memory-reservation to miękki cel, od którego jądro zaczyna odbierać pamięć pod presją. --memory-swap równe -m wyłącza swap — przy wycieku proces dostaje OOM szybciej, zamiast zamulać dysk. W Compose to mem_limit i mem_reservation.

3. Dla Node.js ustaw stertę poniżej limitu kontenera. V8 nie widzi limitu cgroup w starszych wersjach i potrafi żądać więcej, niż kontener ma. Zostaw zapas na stos, bufory i sam runtime:


NODE_OPTIONS=--max-old-space-size=384
przy limicie kontenera 512 MB. To nie leczy wycieku — sprawia, że proces padnie z czytelnym błędem sterty, zanim zabierze całą maszynę.

4. Szukaj przyczyny w procesie, nie w Dockerze. Docker tylko rozlicza pamięć cgroup. Typowe źródła: nieograniczony cache w pamięci, połączenia do bazy trzymane bez puli, nasłuchiwacze zdarzeń, zbyt wiele replik albo workerów klastra Node. Obraz alpine i npm ci --omit=dev zmniejszają rozmiar obrazu na dysku, nie RSS w działaniu.

Restart jest obejściem na czas incydentu. Trwała poprawka to limit na kontenerze plus usunięcie wzrostu, który widać w docker stats między requestami.