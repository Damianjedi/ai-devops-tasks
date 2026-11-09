/**
 * Pobiera dane użytkownika z zewnętrznego API.
 *
 * Wysyła żądanie HTTP GET pod wskazany adres API,
 * sprawdza poprawność odpowiedzi i przekształca otrzymane dane.
 *
 * @async
 * @function fetchUserData
 * @param {string|number} userId - Unikalny identyfikator użytkownika.
 * @returns {Promise<{name: string, email: string, lastLogin: Date}|null>}
 * Obietnica zwracająca obiekt z danymi użytkownika:
 * - name – imię lub nazwa użytkownika,
 * - email – adres e-mail użytkownika,
 * - lastLogin – data ostatniego logowania.
 * W przypadku błędu zwraca null.
 *
 * @throws {Error} Błąd odpowiedzi HTTP, np. status 404 lub 500.
 *
 * @example
 * fetchUserData(123).then(user => {
 *   if (user) {
 *     console.log(user.name);
 *     console.log(user.email);
 *     console.log(user.lastLogin);
 *   }
 * });
 */
function fetchUserData(userId) {
  return fetch(`https://api.example.com/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return {
        name: data.name,
        email: data.email,
        lastLogin: new Date(data.lastLoginTimestamp)
      };
    })
    .catch(error => {
      console.error('Fetch error:', error);
      return null;
    });
}
