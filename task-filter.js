function getCompletedTaskTitles(tasks) {
    return tasks
      .filter(task => task.status === "completed")
      .toSorted((a, b) => a.id - b.id)
      .map(task => task.title);
  }
  
  const tasks = [
    { id: 3, title: "Testowanie aplikacji", status: "completed" },
    { id: 1, title: "Przygotowanie projektu", status: "completed" },
    { id: 2, title: "Tworzenie API", status: "pending" },
    { id: 4, title: "Dokumentacja", status: "completed" }
  ];
  
  const result = getCompletedTaskTitles(tasks);
  
  console.log(result);
  
  // Wynik:
  // [
  //   "Przygotowanie projektu",
  //   "Testowanie aplikacji",
  //   "Dokumentacja"
  // ]