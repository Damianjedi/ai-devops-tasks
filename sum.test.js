const sum = require('../src/sum');

test('dodaje dwie liczby', () => {
  expect(sum(2, 3)).toBe(5);
});