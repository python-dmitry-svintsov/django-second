import { Block1, Block2, Block3 } from "../objects/blocks.js";
import { Spauner } from "../objects/spauners.js";

import { level0Array } from "./level_0.js";
import { level1Array } from "./level_1.js";
import { level2Array } from "./level_2.js";
import { level3Array } from "./level_3.js";
import { level4Array } from "./level_4.js";
import { level5Array } from "./level_5.js";
import { level6Array } from "./level_6.js";
import { level7Array } from "./level_7.js";

export class Maps {
  constructor(main) {
    this.main = main;
    this.scale = this.main.game_scale;
    this.screen = main.context;
    this.levels = [];
    this.get_levels();
    this.current_level = this.levels[this.main.current_level];
    this.level_concreteBlocksArray = [];
    this.playerBlocksArray = [];
    this.enemyBlocksArray = [];
    this.spaunerBlocksArray = [];
    this.collision_map = new Map();
    this.get_map();
  }

  get_levels() {
    this.levels.push(level0Array);
    this.levels.push(level1Array);
    this.levels.push(level2Array);
    this.levels.push(level3Array);
    this.levels.push(level4Array);
    this.levels.push(level5Array);
    this.levels.push(level6Array);
    this.levels.push(level7Array);
  }

  get_map() {
    let x = 0;
    let y = 0;
    for (let row = 0; row < this.current_level.length; row++) {
      x = 0;
      for (let column = 0; column < this.current_level[0].length; column++) {
        if (this.current_level[row][column] == 1) {
          this.level_concreteBlocksArray.push(
            new Block1(x + 0.5, y + 0.5, this.screen, this.scale)
          );
          this.collision_map.set(x * 100 + y, 1);
        }
        if (this.current_level[row][column] == 2) {
          this.level_concreteBlocksArray.push(
            new Block2(x + 0.5, y + 0.5, this.screen, this.scale)
          );
          this.collision_map.set(x * 100 + y, 1);
        }
        if (this.current_level[row][column] == 3) {
          this.level_concreteBlocksArray.push(
            new Block3(x + 0.5, y + 0.5, this.screen, this.scale)
          );
          this.collision_map.set(x * 100 + y, 1);
        }
        if (this.current_level[row][column] == 8) {
          this.main.store.spauners.push(
            new Spauner(x + 0.5, y + 0.5, this.screen, this.scale)
          );
        }
        if (this.current_level[row][column] == 9) {
          this.player_pos = [x + 0.5, y + 0.5];
        }
        x += 1;
      }
      y += 1;
    }
  }

  draw() {
    this.level_concreteBlocksArray.forEach((elem) => {
      elem.draw();
    });
  }

  colllision(pos) {
    return this.collision_map.has(pos);
  }
}
