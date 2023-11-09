export function distanceBeetwenTwoPoints(x1, y1, x2, y2) {
  const xDiff = x1 - x2;
  const yDiff = y1 - y2;
  /*Высчитываем гипотенузу с помозью метода*/
  return Math.hypot(xDiff, yDiff);
}
