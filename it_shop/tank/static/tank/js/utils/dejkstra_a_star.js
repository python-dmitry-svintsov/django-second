import { coding } from "./coders.js";

export class A_Star {
  constructor(main) {
    this.main = main;
    this.graf = new Object();
    this.current_level = this.main.map.current_level;
    this.graf = new Map();
    this.ways = [
      [-1, 0],
      [0, -1],
      [1, 0],
      [0, 1],
    ];
    this.get_graf();
    // this.for_debaging();
  }

  // decoding(val) {
  //   let res = val % 100;
  //   return [(val - res) / 100, res];
  // }

  // coding(x, y) {
  //   return x * 100 + y;
  // }

  get_nearly_position(x, y) {
    let elem = [];
    for (const item in this.ways) {
      let res = coding(x + this.ways[item][0], y + this.ways[item][1]);
      let check = this.main.map.colllision(res);
      if (!check) {
        elem.push(res);
      }
    }
    return elem;
  }

  get_graf() {
    let x = 0;
    let y = 0;
    for (let row = 0; row < this.current_level.length; row++) {
      x = 0;
      for (let column = 0; column < this.current_level[0].length; column++) {
        if (this.current_level[row][column] !== 1) {
          if (this.current_level[row][column] !== 2) {
            if (this.current_level[row][column] !== 3) {
              let nearly_coorinates = this.get_nearly_position(x, y);
              this.graf.set(coding(x, y), nearly_coorinates);
            }
          }
        }
        x += 1;
      }
      y += 1;
    }
  }

  bfs(start, goal) {
    let visited = new Map();
    let steck = [start];
    visited.set(start, false);
    while (steck.length > 0) {
      let current = steck.shift();
      if (current == goal) {
        break;
      }
      if (this.graf.has(current)) {
        let next = this.graf.get(current);
        for (let index in next) {
          if (!visited.has(next[index])) {
            steck.push(next[index]);
            visited.set(next[index], current);
          }
        }
      }
    }
    return visited;
  }

  get_path(start, goal) {
    let visited = this.bfs(start, goal);
    let path = [goal];
    let step = visited.get(goal);
    while (step && step != start) {
      path.push(step);
      step = visited.get(step);
    }
    return path;
  }

  for_debaging() {
    let a = 303;
    let b = 101;
    let res = this.get_path(a, b);
    console.log(res);
  }
}
