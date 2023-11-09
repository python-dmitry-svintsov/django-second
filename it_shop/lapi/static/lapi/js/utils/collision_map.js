class Collision_Map {
  constructor(main) {
    this.main = main;
    this.storage = new Map();
  }

  add(x, y) {
    this.storage.set(Element(x, y));
  }

  eql(x, y) {
    var result = true;
    this.storage.forEach((el) => {
			if (el.x == x && el.y == y)
		});
  }
}

class Element {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}
