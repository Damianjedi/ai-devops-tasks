
flowchart TD
    A([Start pipeline CI/CD]) --> B[Checkout kodu z Git]
    B --> C[Budowanie aplikacji]
    C --> D[Testy jednostkowe]
    D --> E[Analiza statyczna kodu<br/>SonarQube]
    E --> F[Analiza bezpieczeństwa<br/>SAST / Dependency Scan]

    F --> G{Wszystkie kontrole<br/>zakończone sukcesem?}
    G -->|Nie| X[Przerwanie pipeline]
    G -->|Tak| H[Budowanie obrazu Docker]

    H --> I[Publikacja obrazu<br/>Docker Registry]
    I --> J[Testy integracyjne]
    J --> K{Testy zakończone<br/>sukcesem?}

    K -->|Nie| X
    K -->|Tak| L[Wdrożenie na środowisko Staging]

    L --> M[Testy akceptacyjne<br/>i smoke tests]
    M --> N{Akceptacja wdrożenia?}

    N -->|Nie| X
    N -->|Tak| O[Wdrożenie na środowisko Production]

    O --> P[Weryfikacja wdrożenia<br/>Health checks]
    P --> Q([Koniec pipeline])

    X --> R([Powiadomienie o błędzie])

    style A fill:#d1fae5,stroke:#059669,color:#064e3b
    style Q fill:#d1fae5,stroke:#059669,color:#064e3b
    style X fill:#fee2e2,stroke:#dc2626,color:#991b1b
    style R fill:#fef3c7,stroke:#d97706,color:#92400e
    style O fill:#dbeafe,stroke:#2563eb,color:#1e40af
