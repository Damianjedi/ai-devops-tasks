# Wyjaśnienie zależności między etapami pipeline’u CI/CD w Jenkinsie

Pipeline CI/CD w Jenkinsie składa się z kolejnych etapów, które są ze sobą logicznie powiązane. Każdy etap wykorzystuje wyniki poprzedniego i sprawdza, czy aplikacja spełnia określone wymagania jakościowe, funkcjonalne oraz bezpieczeństwa.

Podstawowa zasada działania jest następująca: kolejny etap rozpoczyna się dopiero wtedy, gdy poprzedni zakończy się powodzeniem. W przypadku błędu pipeline może zostać zatrzymany, a zespół otrzymuje powiadomienie.

## 1. Zależności między poszczególnymi etapami

1\. Checkout kodu → Budowanie aplikacji

Jenkins pobiera kod źródłowy z repozytorium Git (np. GitHub lub GitLab). Następnie przekazuje go do procesu budowania. Bez pobrania aktualnego kodu nie można rozpocząć kompilacji ani dalszych operacji.

2\. Budowanie aplikacji → Testy jednostkowe

Po zbudowaniu aplikacji Jenkins uruchamia testy jednostkowe. Sprawdzają one poprawność działania poszczególnych funkcji i modułów. Jeśli budowanie zakończy się błędem, testy nie zostaną uruchomione.

3\. Testy jednostkowe → Analiza statyczna kodu

Po pomyślnym przejściu testów Jenkins wykonuje analizę statyczną kodu, np. za pomocą SonarQube. Analiza pozwala wykryć błędy programistyczne, duplikację kodu, problemy z czytelnością oraz naruszenia standardów programowania.

4\. Analiza statyczna → Analiza bezpieczeństwa

Kolejnym krokiem jest sprawdzenie bezpieczeństwa aplikacji. Jenkins może wykorzystać narzędzia SAST oraz skanery zależności, aby wykryć potencjalne podatności w kodzie i bibliotekach zewnętrznych.

5\. Analiza bezpieczeństwa → Budowanie obrazu Docker

Jeśli analiza jakości i bezpieczeństwa zakończy się sukcesem, Jenkins rozpoczyna budowanie obrazu Docker. Obraz zawiera aplikację oraz jej środowisko uruchomieniowe. Dzięki temu aplikacja może działać w sposób powtarzalny na różnych środowiskach.

6\. Budowanie Docker → Publikacja obrazu → Testy integracyjne

Gotowy obraz jest publikowany w Docker Registry (np. Docker Hub lub GitLab Container Registry). Następnie wykorzystywany jest do uruchomienia aplikacji i przeprowadzenia testów integracyjnych. Testy sprawdzają współpracę między komponentami, np. aplikacją, bazą danych i usługami zewnętrznymi.

7\. Testy integracyjne → Wdrożenie na Staging

Jeśli testy integracyjne zakończą się powodzeniem, Jenkins wdraża aplikację na środowisko staging. Jest to środowisko testowe możliwie zbliżone do produkcyjnego. Umożliwia ono sprawdzenie aplikacji w warunkach zbliżonych do rzeczywistego użytkowania.

8\. Staging → Testy akceptacyjne i smoke tests

Na środowisku staging wykonywane są dodatkowe testy, które sprawdzają, czy aplikacja działa zgodnie z wymaganiami biznesowymi. Smoke tests weryfikują podstawowe funkcjonalności, np. logowanie, dostępność strony i komunikację z API.

9\. Testy staging → Produkcja

Po pozytywnej weryfikacji środowiska staging następuje wdrożenie na produkcję. W praktyce często wymagane jest dodatkowe ręczne zatwierdzenie przez administratora lub osobę odpowiedzialną za wydanie.

10\. Produkcja → Health checks

Po wdrożeniu Jenkins sprawdza, czy aplikacja działa prawidłowo. Health checks mogą obejmować kontrolę dostępności endpointów, połączenia z bazą danych i poprawności działania usług.

## 2. Schemat zależności

Poniższy schemat przedstawia przepływ danych i warunki przechodzenia między etapami.

\#chatgpt-mermaid-\_r_2j4\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_2j4\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_2j4\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_2j4\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_2j4\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_2j4\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_2j4\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_2j4\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_2j4\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_2j4\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2j4\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2j4\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:16px;}#chatgpt-mermaid-\_r_2j4\_ p{margin:0;}#chatgpt-mermaid-\_r_2j4\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_2j4\_ .label text,#chatgpt-mermaid-\_r_2j4\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ .node rect,#chatgpt-mermaid-\_r_2j4\_ .node circle,#chatgpt-mermaid-\_r_2j4\_ .node ellipse,#chatgpt-mermaid-\_r_2j4\_ .node polygon,#chatgpt-mermaid-\_r_2j4\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .rough-node .label text,#chatgpt-mermaid-\_r_2j4\_ .node .label text,#chatgpt-mermaid-\_r_2j4\_ .image-shape .label,#chatgpt-mermaid-\_r_2j4\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_2j4\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .rough-node .label,#chatgpt-mermaid-\_r_2j4\_ .node .label,#chatgpt-mermaid-\_r_2j4\_ .image-shape .label,#chatgpt-mermaid-\_r_2j4\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_2j4\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_2j4\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2j4\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2j4\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_2j4\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_2j4\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_2j4\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_2j4\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_2j4\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_2j4\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2j4\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_2j4\_ .icon-shape,#chatgpt-mermaid-\_r_2j4\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_2j4\_ .icon-shape p,#chatgpt-mermaid-\_r_2j4\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_2j4\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_2j4\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_2j4\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_2j4\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_2j4\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_2j4\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_2j4\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_2j4\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_2j4\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2j4\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_2j4\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2j4\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_2j4\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_2j4\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_2j4\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_2j4\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .node rect,#chatgpt-mermaid-\_r_2j4\_ .node circle,#chatgpt-mermaid-\_r_2j4\_ .node ellipse,#chatgpt-mermaid-\_r_2j4\_ .node polygon,#chatgpt-mermaid-\_r_2j4\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_2j4\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_2j4\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2px,2px;}#chatgpt-mermaid-\_r_2j4\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_2j4\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2j4\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,Segoe UI,Helvetica,Apple Color Emoji,Arial,sans-serif,Segoe UI Emoji,Segoe UI Symbol;}Checkout GitBuild aplikacjiTesty jednostkoweAnaliza statyczna - SonarQubeSkanowanie bezpieczeństwaQuality GatePrzerwanie pipelineBuild DockerDocker RegistryTesty integracyjneTesty OK?Deploy StagingTesty akceptacyjne i SmokeTestsAkceptacja?Deploy ProductionHealth ChecksPipeline zakończony sukcesemPowiadomienie o błędzieNiepowodzenieSukcesNieTakNieTak

## 3. Co się dzieje, gdy jeden z etapów zakończy się błędem?

Pipeline wykorzystuje mechanizm kontroli jakości i warunków przejścia (Quality Gates).

| Etap, na którym wystąpi błąd | Konsekwencja                                               |
| ---------------------------- | ---------------------------------------------------------- |
| Checkout                     | Brak możliwości pobrania kodu, pipeline zostaje zatrzymany |
| Build                        | Aplikacja nie zostaje zbudowana                            |
| Testy jednostkowe            | Wykryte błędy blokują dalsze etapy                         |
| Analiza statyczna            | Niespełnienie Quality Gate blokuje pipeline                |
| Bezpieczeństwo               | Krytyczne podatności mogą zablokować wydanie               |
| Docker Build                 | Nie powstaje obraz aplikacji                               |
| Testy integracyjne           | Obraz nie zostaje dopuszczony do staging                   |
| Staging                      | Nieprawidłowe działanie blokuje wdrożenie produkcyjne      |
| Production                   | Nieudane wdrożenie może uruchomić procedurę rollbacku      |

## 4. Dlaczego kolejność etapów jest ważna?

Kolejność etapów została zaprojektowana tak, aby jak najwcześniej wykrywać błędy i ograniczać koszty ich naprawy.

- Wczesne wykrywanie błędów – testy jednostkowe i analiza kodu pozwalają wykryć problemy przed utworzeniem obrazu Docker.
- Kontrola bezpieczeństwa – podatności są wykrywane przed wdrożeniem aplikacji.
- Powtarzalność wdrożeń – ten sam obraz Docker może być testowany na staging i następnie wdrażany na produkcję.
- Ograniczenie ryzyka – środowisko staging pozwala zweryfikować aplikację przed udostępnieniem jej użytkownikom.
- Automatyzacja – Jenkins wykonuje kolejne operacje bez konieczności ręcznego uruchamiania każdego etapu.

## 5. Podsumowanie

Najważniejsza zależność w całym pipeline polega na tym, że każdy etap dostarcza wynik niezbędny do wykonania kolejnego:

Kod źródłowy → Zbudowana aplikacja → Zweryfikowany kod → Bezpieczna aplikacja → Obraz Docker → Przetestowany obraz → Staging → Produkcja.

Dzięki takiej organizacji Jenkins zapewnia kontrolowany, powtarzalny i zautomatyzowany proces dostarczania aplikacji webowej. Błędy są wykrywane możliwie wcześnie, a na produkcję trafia wersja aplikacji, która przeszła wszystkie wymagane kontrole.