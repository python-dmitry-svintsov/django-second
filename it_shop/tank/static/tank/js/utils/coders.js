export function coding(x, y) {
  return x * 100 + y;
}

export function coding_unit(x, y) {
  return Math.floor(x) * 100 + Math.floor(y);
}

export function decoding_unit(val) {
  let res = val % 100;
  return [(val - res) / 100 + 0.5, res + 0.5];
}
