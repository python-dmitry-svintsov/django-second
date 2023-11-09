import { Player } from "./player.js";
import { Wall, Moove, Door_Hor, Door_Vert } from "./objects/basic_objects.js";
import { distanceBeetwenTwoPoints } from "./utils/distance.js";
import { Key, Target, Weapon, Spauner } from "./objects/animated.js";
import { Type_1, Spider } from "./npc/type_1.js";
import { ProjectTile } from "./projecttile.js";
/*----------------------------------------------------------------*/
function main(path) {
  var request = new XMLHttpRequest();
  request.open("GET", path);
  request.responseType = "json";
  request.send();
  request.onload = function () {
    level_data = request.response;
    level_name.innerHTML = level_data.data.title;
    level_enemy_limit.innerHTML = level_data.data.max_enemys;
    script = new Storage(
      context,
      canvas,
      level_data.data.max_enemys,
      level_data.data.speed,
      level_data.data.map,
      level_data.data.style
    );
    canvas.style.backgroundImage = level_data.data.background
      ? `url("/media/${level_data.data.background}")`
      : 'url("/static/lapi/img/0/fon.jpg")';
    run_canvas();
  };
}
/*----------------------------------------------------------------*/
const level_name = document.querySelector("#level-name");
const level_enemy_limit = document.querySelector("#enemy-limit");

const game_over = document.querySelector(".game-over");
const game_win = document.querySelector(".game-win");

const canvas = document.getElementsByClassName("lapi-canvas")[0];
canvas.width = 600;
canvas.height = 600;
const canvas_width = canvas.width;
const canvas_height = canvas.height;
const context = canvas.getContext("2d");
var game;
const game_score = document.querySelector("#score");
const player_health = document.querySelector("#health");
/*----------------------------------------------------------------*/
/*----------------------------------------------------------------*/

function run_canvas() {
  game = requestAnimationFrame(run_canvas);
  script.update();
  script.draw();
}

export class Storage {
  constructor(context, canvas, limit, speed, map, style) {
    this.context = context;
    this.canvas = canvas;
    this.widht = this.canvas.width;
    this.height = this.canvas.height;
    this.enemy_limit = limit;
    this.spaun_speed = speed;
    this.map = map;
    this.level_style = style ? Math.abs(style) : 0;
    this.scale = Math.floor(this.canvas.width / this.map.length);
    this.half_of_scale = Math.floor(this.scale / 2);
    this.delay = 0;
    /*-----------------------------------------------------------------*/
    this.collision_map = {};
    this.walls = [];
    this.mooving_walls = [];
    this.doors = [];
    this.keys = [];
    this.artifacts = [];
    this.enemys = [];
    this.project_tiles = [];
    this.spauners = [];
    this.player = undefined;
    /*-----------------------------------------------------*/
    this.key = document.querySelector("#key");
    this.crossbow = document.querySelector("#crossbow");
    this.key.hidden = true;
    this.crossbow.hidden = true;
    /*-----------------------------------------------------*/
    this.inition();
  }

  inition() {
    this.build_map();
  }

  build_map() {
    for (let y = 0; y < this.map.length; y++) {
      for (let x = 0; x < this.map[0].length; x++) {
        if (this.map[y][x] == 1) {
          this.walls.push(new Wall(this, this.context, x + 0.5, y + 0.5));
        }
        if (this.map[y][x] == 9 && !this.player) {
          this.player = new Player(this, x + 0.5, y + 0.5);
        }
        if (this.map[y][x] == 8) {
          this.target = new Target(this, this.context, x + 0.5, y + 0.5);
        }
        if (this.map[y][x] == 7) {
          if (this.map[y][x - 1] != 1) {
            this.doors.push(
              new Door_Vert(this, this.context, x + 0.5, y + 0.5)
            );
          } else {
            this.doors.push(new Door_Hor(this, this.context, x + 0.5, y + 0.5));
          }
        }
        if (this.map[y][x] == 6) {
          this.keys.push(new Key(this, this.context, x + 0.5, y + 0.5));
        }
        if (this.map[y][x] == 5) {
          this.enemys.push(new Type_1(this, x + 0.5, y + 0.5));
        }
        if (this.map[y][x] == 4) {
          this.artifacts.push(new Weapon(this, this.context, x + 0.5, y + 0.5));
        }
        if (this.map[y][x] == 3) {
          this.spauners.push(new Spauner(this, this.context, x + 0.5, y + 0.5));
        }
        if (this.map[y][x] == 2) {
          this.mooving_walls.push(
            new Moove(this, this.context, x + 0.5, y + 0.5)
          );
        }
      }
    }
  }

  draw() {
    this.context.clearRect(0, 0, this.widht, this.height);
    this.spauners.forEach((el) => {
      el.draw();
    });
    /*------------------------------------------------------*/
    this.artifacts.forEach((el) => {
      el.draw();
      var art_distance = distanceBeetwenTwoPoints(
        this.player.x,
        this.player.y,
        el.x,
        el.y
      );
      if (!this.player.bag.weapon && art_distance < 0.1) {
        this.toggle(this.crossbow);
        el.taked = true;
        this.player.bag.weapon = true;
      }
    });
    this.keys.forEach((el) => {
      el.draw();
      var key_distance = distanceBeetwenTwoPoints(
        this.player.x,
        this.player.y,
        el.x,
        el.y
      );
      if (!this.player.bag.key && key_distance < 0.1) {
        this.toggle(this.key);
        el.taked = true;
        this.player.bag.key = true;
      }
    });
    this.target.draw();
    /*---------------------------------------------*/
    this.project_tiles.forEach((el) => {
      el.draw();
    });
    /*---------------------------------------------*/
    this.walls.forEach((el) => {
      el.draw();
    });
    this.mooving_walls.forEach((el) => {
      el.draw();
    });
    this.doors.forEach((el) => {
      el.draw();
    });
    this.player.draw();
    this.enemys.forEach((el) => {
      el.draw();
    });
  }

  update() {
    this.delay += 1;
    this.keys = this.keys.filter((el) => !el.taked);
    this.artifacts = this.artifacts.filter((el) => !el.taked);
    this.player.updatePosition();
    this.enemys.forEach((el) => {
      /* enemy mooving */
      el.moove();
      /*Смерть игрока от соприкосновения с монстром*/
      if (
        distanceBeetwenTwoPoints(el.x, el.y, this.player.x, this.player.y) < 0.7
      ) {
        cancelAnimationFrame(game);
        game_over.style.display = "block";
      }
    });
    this.project_tiles.forEach((el) => {
      el.update();
      this.walls.forEach((wall) => {
        if (distanceBeetwenTwoPoints(wall.x, wall.y, el.x, el.y) < 0.2) {
          el.active = false;
        }
      });
      this.doors.forEach((door) => {
        if (
          distanceBeetwenTwoPoints(door.x, door.y, el.x, el.y && door.close) <
          0.2
        ) {
          el.active = false;
        }
      });
      this.mooving_walls.forEach((m_wall) => {
        if (distanceBeetwenTwoPoints(m_wall.x, m_wall.y, el.x, el.y) < 0.2) {
          el.active = false;
        }
      });
      this.enemys.forEach((enemy) => {
        if (distanceBeetwenTwoPoints(enemy.x, enemy.y, el.x, el.y) < 0.2) {
          el.active = false;
          enemy.demaged = true;
        }
      });
      this.spauners.forEach((spauner) => {
        if (distanceBeetwenTwoPoints(spauner.x, spauner.y, el.x, el.y) < 0.2) {
          el.active = false;
          spauner.demaged = true;
        }
      });
    });
    this.project_tiles = this.project_tiles.filter((el) => el.active);
    this.enemys = this.enemys.filter((el) => !el.demaged);
    this.spauners = this.spauners.filter((el) => !el.demaged);
    this.spawn_enemies();
  }

  player_collision(x, y) {
    var result = true;
    this.walls.forEach((el) => {
      var distance = distanceBeetwenTwoPoints(el.x, el.y, x, y);
      if (distance < 0.9) {
        result = false;
      }
    });
    this.doors.forEach((el) => {
      var distance = distanceBeetwenTwoPoints(el.x, el.y, x, y);
      if (distance < 1 && el.close && this.player.bag.key) {
        this.player.bag.key = false;
        this.toggle(this.key);
        el.close = false;
        el.subX = 24;
      }
      if (distance < 0.9 && el.close) {
        result = false;
      }
    });
    /*проверка для движемых блоков*/
    this.mooving_walls.forEach((el) => {
      var distance = distanceBeetwenTwoPoints(el.x, el.y, x, y);
      if (distance < 0.9) {
        var cur_pos = el.direction.get(this.player.imageLenght);
        var cur_x = Math.floor(el.x + cur_pos[0]);
        var cur_y = Math.floor(el.y + cur_pos[1]);
        if (this.map_collison(cur_x, cur_y)) {
          el.x += cur_pos[0];
          el.y += cur_pos[1];
        } else {
          result = false;
        }
      }
    });
    /*Если игрок достиг цели уровня*/
    if (
      distanceBeetwenTwoPoints(
        this.target.x,
        this.target.y,
        this.player.x,
        this.player.y
      ) < 0.1
    ) {
      cancelAnimationFrame(game);
      game_win.style.display = "block";
    }
    return result;
  }

  map_collison(x, y) {
    var result = true;
    this.walls.forEach((el) => {
      if (x == Math.floor(el.x) && y == Math.floor(el.y)) {
        result = false;
      }
    });
    this.doors.forEach((el) => {
      if (x == Math.floor(el.x) && y == Math.floor(el.y) && el.close) {
        result = false;
      }
    });
    this.enemys.forEach((el) => {
      if (
        x == Math.floor(el.ceil_coord[0]) &&
        y == Math.floor(el.ceil_coord[1])
      ) {
        result = false;
      }
    });
    this.mooving_walls.forEach((el) => {
      if (x == Math.floor(el.x) && y == Math.floor(el.y)) {
        result = false;
      }
    });
    return result;
  }

  toggle(elem) {
    elem.hidden = elem.hidden ? false : true;
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
    this.project_tiles.push(new ProjectTile(this, x, y, direct));
  }

  spawn_enemies() {
    if (this.delay % this.spaun_speed == 0) {
      let index = Math.floor(Math.random() * this.spauners.length);
      let object = this.spauners[index];
      if (this.enemys.length < this.enemy_limit) {
        this.enemys.push(new Spider(this, object.x, object.y));
      }
    }
  }
}

/*----------------------------------------------------------------*/
var script;
var level_data;
const slug = document.querySelector(".slug").value;
main(`/lapi/get_data/${slug}`);
/*----------------------------------------------------------------*/
