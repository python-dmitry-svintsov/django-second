import { distanceBeetwenTwoPoints } from "../utils/distance.js";
import { ProjectTile } from "./projectTile.js";
import { TypeA } from "./enemy_type_a.js";

export class Store {
  constructor(main) {
    this.main = main;
    this.context = this.main.context;
    this.scale = this.main.game_scale;
    this.projectTile = [];
    this.enemy = [];
    this.spauners = [];
    this.enemy_limit = this.main.enemy_limit;
    this.speed_game = this.main.speed;
  }

  spawn_enemies() {
    if (this.main.delay % this.speed_game == 0) {
      if (this.enemy.length < this.enemy_limit) {
        let index = Math.floor(Math.random() * this.spauners.length);
        let object = this.spauners[index];
        this.enemy.push(new TypeA(this, object.x, object.y));
      }
    }
  }

  add_project_tile(x, y, direct) {
    if (direct == 0) {
      y -= 0.5;
    }
    if (direct == 1) {
      y += 0.5;
    }
    if (direct == 2) {
      x -= 0.5;
    }
    if (direct == 3) {
      x += 0.5;
    }
    this.projectTile.push(
      new ProjectTile(
        this,
        Math.floor(x * this.scale),
        Math.floor(y * this.scale),
        direct
      )
    );
  }

  check_project_tile(item, index) {
    this.main.map.level_concreteBlocksArray.forEach((elem) => {
      let distance = distanceBeetwenTwoPoints(
        item.x,
        item.y,
        elem.x * this.scale,
        elem.y * this.scale
      );
      if (distance < 14) {
        this.projectTile.splice(index, 1);
        return;
      }
    });
    this.enemy.forEach((elem) => {
      let distance = distanceBeetwenTwoPoints(
        item.x,
        item.y,
        elem.x * this.scale,
        elem.y * this.scale
      );
      if (distance < 10) {
        elem.hit();
        this.projectTile.splice(index, 1);
        return;
      }
    });
    this.spauners.forEach((elem) => {
      let distance = distanceBeetwenTwoPoints(
        item.x,
        item.y,
        elem.x * this.scale,
        elem.y * this.scale
      );
      if (distance < 10) {
        elem.hit();
        this.projectTile.splice(index, 1);
        this.main.score += 5;
        return;
      }
    });

    let player_dist = distanceBeetwenTwoPoints(
      item.x,
      item.y,
      this.main.player.x * this.scale,
      this.main.player.y * this.scale
    );
    if (player_dist < 10) {
      this.main.player.hit();
      this.projectTile.splice(index, 1);
    }
  }

  update() {
    this.enemy = this.enemy.filter((elem) => elem.health > 0);
    this.spauners = this.spauners.filter((elem) => elem.health > 0);
    let index = 0;
    this.projectTile.forEach((elem) => {
      elem.update();
      this.check_project_tile(elem, index);
      index++;
    });
    this.enemy.forEach((elem) => {
      elem.update();
    });
    this.spawn_enemies();
  }

  draw() {
    this.projectTile.forEach((elem) => elem.draw());
    this.spauners.forEach((elem) => elem.draw());
    this.enemy.forEach((elem) => elem.draw());
  }
}
