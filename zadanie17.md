### Opis rozwiązania

Funkcja `getCompletedTaskTitles(tasks)` przyjmuje tablicę obiektów reprezentujących zadania. Jej zadaniem jest wybranie zadań o statusie `"completed"`, posortowanie ich według identyfikatora `id` w kolejności rosnącej, a następnie zwrócenie tablicy zawierającej wyłącznie tytuły tych zadań.

W rozwiązaniu wykorzystano trzy metody JavaScript:

1. `filter()` – filtruje tablicę i pozostawia tylko zadania o statusie `"completed"`.
2. `toSorted()` – sortuje zadania według identyfikatora `id` rosnąco, nie modyfikując oryginalnej tablicy.
3. `map()` – przekształca tablicę obiektów w tablicę zawierającą same tytuły zadań.

### Przykład użycia

```
function getCompletedTaskTitles(tasks) {
  return tasks
    .filter(task => task.status === "completed")
    .toSorted((a, b) => a.id - b.id)
    .map(task => task.title);
}

// Przykładowa tablica zadań
const tasks = [
  { id: 3, title: "Testowanie aplikacji", status: "completed" },
  { id: 1, title: "Przygotowanie projektu", status: "completed" },
  { id: 2, title: "Tworzenie API", status: "pending" },
  { id: 4, title: "Dokumentacja", status: "completed" },
  { id: 5, title: "Projektowanie interfejsu", status: "in progress" }
];

// Wywołanie funkcji
const result = getCompletedTaskTitles(tasks);

// Wyświetlenie wyniku
console.log(result);

// Wynik:
// [
//   "Przygotowanie projektu",
//   "Testowanie aplikacji",
//   "Dokumentacja"
// ]
```

### Wynik działania

Funkcja zwraca następującą tablicę:

```
[
  "Przygotowanie projektu",
  "Testowanie aplikacji",
  "Dokumentacja"
]
```

Podsumowanie: rozwiązanie wykorzystuje metody tablicowe JavaScript, dzięki czemu kod jest krótki, czytelny i łatwy w utrzymaniu. Jego złożoność czasowa wynosi średnio O(n log n) ze względu na sortowanie.