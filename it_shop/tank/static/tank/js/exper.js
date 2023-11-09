const my_str =
  "{'title': 'inception'\\054 'difficult': 1\\054 'level': 1\\054 'max_enemys': 4\\054 'speed': 400}";

const res = my_str.replace(/'/g, '"');
console.log(res);
