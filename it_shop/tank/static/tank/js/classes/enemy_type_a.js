import { coding_unit, decoding_unit } from "../utils/coders.js";

export class TypeA {
  constructor(main, x, y) {
    this.main = main;
    this.x = x;
    this.y = y;
    this.scale = this.main.scale;
    this.context = this.main.context;
    this.image = new Image();
    this.image.src = "/static/tank/img/tank2.png";
    this.imageWith = 24;
    this.imageHeight = 24;
    this.imageLenght = 0;
    this.velocity = 1 / this.scale / 2;
    this.imageTick = 0;
    this.ImageTickLimit = 18;
    this.health = 3;
    // this.moovingLimit = 700;
    // this.update();
  }
  draw() {
    let subX =
      this.imageTick > this.ImageTickLimit
        ? this.imageWith * 2
        : this.imageWith;
    this.imageTick++;
    if (this.imageTick > this.ImageTickLimit * 2) this.imageTick = 0;
    this.context.drawImage(
      this.image,
      subX,
      this.imageHeight * this.imageLenght,
      this.imageWith,
      this.imageHeight,
      (this.x - 0.5) * this.scale,
      (this.y - 0.5) * this.scale,
      this.imageWith,
      this.imageHeight
    );
  }

  moove_by_path(x, y) {
    let direction = this.imageLenght;
    let dx = x - this.x;
    let dy = y - this.y;
    if (dx !== 0) {
      this.x += (dx / Math.abs(dx)) * this.velocity;

      if (dx > 1e-1) {
        direction = 3;
      }
      if (dx < -1e-1) {
        direction = 2;
      }
    }
    if (dy !== 0) {
      this.y += (dy / Math.abs(dy)) * this.velocity;

      if (dy > 1e-1) {
        direction = 1;
      }
      if (dy < -1e-1) {
        direction = 0;
      }
    }

    this.imageLenght = direction;
  }

  create_projectile() {
    if (this.main.main.delay % 200 === 0) {
      this.main.add_project_tile(this.x, this.y, this.imageLenght);
    }
  }

  shoot() {
    if (Math.floor(this.y) == Math.floor(this.main.main.player.y)) {
      if (this.x - this.main.main.player.x > 0) {
        this.imageLenght = 2;
      } else {
        this.imageLenght = 3;
      }
      this.create_projectile();
    }
    if (Math.floor(this.x) == Math.floor(this.main.main.player.x)) {
      if (this.y - this.main.main.player.y > 0) {
        this.imageLenght = 0;
      } else {
        this.imageLenght = 1;
      }
      this.create_projectile();
    }
  }

  update() {
    let unit_pos = coding_unit(this.x, this.y);
    let player_pos = coding_unit(
      this.main.main.player.x,
      this.main.main.player.y
    );
    let path = this.main.main.path_finder.get_path(unit_pos, player_pos);
    if (path.length > 0) {
      let cur_pos = decoding_unit(path.pop());
      this.moove_by_path(cur_pos[0], cur_pos[1]);
    }
    this.shoot();
  }

  hit() {
    this.health--;
    this.main.main.score += 2;
  }
}
