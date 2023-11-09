const quantity_input = document.querySelector("#quantity-input");
const minus = document.querySelector("#minus");
const plus = document.querySelector("#plus");
const span = document.querySelector("#span-input");
const max = quantity_input.max;

var quantity = 1;
span.innerHTML = quantity;

plus.addEventListener("click", (evt) => {
  quantity += 1;
  quantity = Math.max(1, Math.min(max, quantity));
  span.innerHTML = quantity;
  quantity_input.value = quantity;
});

minus.addEventListener("click", (evt) => {
  quantity -= 1;
  quantity = Math.max(1, Math.min(max, quantity));
  span.innerHTML = quantity;
  quantity_input.value = quantity;
});
