Co zostało zmienione?
1. Zastosowanie obiektu konfiguracyjnego

Zamiast wielu instrukcji warunkowych wykorzystujemy jeden obiekt environmentConfigs, który przechowuje konfigurację każdego środowiska.

2. Uproszczenie logiki

Zamiast sprawdzać kolejno każdy warunek if...else if, pobieramy konfigurację bezpośrednio na podstawie nazwy środowiska:
environmentConfigs[env]


3. Domyślna konfiguracja

Operator || pozwala zwrócić konfigurację development, jeśli podana nazwa środowiska nie istnieje w obiekcie.
return environmentConfigs[env] || environmentConfigs.development;


3. Przykłady użycia
console.log(getEnvironmentConfig('development'));


Wynik:
{
  apiUrl: 'http://localhost:3000/api',
  debug: true,
  timeout: 5000
}


Dla środowiska produkcyjnego:
console.log(getEnvironmentConfig('production'));


Wynik:
{
  apiUrl: 'https://api.example.com',
  debug: false,
  timeout: 15000
}


Dla nieznanego środowiska:
console.log(getEnvironmentConfig('unknown'));


Zostanie zwrócona konfiguracja środowiska development.
4. Zalety refaktoryzacji
| Kryterium | Przed refaktoryzacją | Po refaktoryzacji |
|---|---|---|
| Czytelność | Wiele warunków | Prosta struktura |
| Rozbudowa | Dodawanie kolejnych if | Dodanie wpisu w obiekcie |
| Utrzymanie | Więcej powtarzalnego kodu | Mniej powtórzeń |
| Wydajność | Wielokrotne sprawdzanie warunków | Bezpośredni dostęp do właściwości obiektu |
| Domyślna konfiguracja | Blok else | Operator || |
5. Dodatkowe ulepszenie – zabezpieczenie konfiguracji
Można również zastosować Object.freeze(), aby zabezpieczyć konfigurację przed przypadkową modyfikacją:
const environmentConfigs = Object.freeze({
  development: Object.freeze({
    apiUrl: 'http://localhost:3000/api',
    debug: true,
    timeout: 5000
  }),
  testing: Object.freeze({
    apiUrl: 'http://test-server:3000/api',
    debug: true,
    timeout: 5000
  }),
  staging: Object.freeze({
    apiUrl: 'https://staging.example.com/api',
    debug: false,
    timeout: 10000
  }),
  production: Object.freeze({
    apiUrl: 'https://api.example.com',
    debug: false,
    timeout: 15000
  })
});


Object.freeze() zabezpiecza obiekty przed zmianą ich właściwości na pierwszym poziomie.

Podsumowanie: Najważniejszą zmianą jest zastąpienie rozbudowanej instrukcji warunkowej obiektem konfiguracyjnym. Takie rozwiązanie stosuje się często w projektach JavaScript i Node.js, ponieważ ułatwia zarządzanie konfiguracją środowisk development, testing, staging i production.