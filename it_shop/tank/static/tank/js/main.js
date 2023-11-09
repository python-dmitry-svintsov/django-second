function get_data() {
  var result;
  const cookie = document.cookie.split("; ").forEach((item) => {
    var data = item.split("=");
    if (data[0] == "data") {
      result = JSON.parse(
        data[1].slice(1, -1).replace(/'/g, '"').replace(/\\054/g, ",")
      );
    }
  });
  return result;
}
const level_data = get_data();
const level_name = document.querySelector("#level-name");
level_name.innerHTML = level_data.title;
const level_enemy_limit = document.querySelector("#enemy-limit");
level_enemy_limit.innerHTML = level_data.max_enemys;

const game_over = document.querySelector(".game-over");
const game_win = document.querySelector(".game-win");

const canvas = document.getElementsByClassName("tank-canvas")[0];
canvas.width = 600;
canvas.height = 600;
const canvas_width = canvas.width;
const canvas_height = canvas.height;
const context = canvas.getContext("2d");
var game;
const game_score = document.querySelector("#score");
const player_health = document.querySelector("#health");

import { Player } from "./classes/player.js";
import { Store } from "./classes/store.js";
import { Maps } from "./levels/map.js";
import { A_Star } from "./utils/dejkstra_a_star.js";

class Game {
  constructor(level, limit, speed) {
    this.context = context;
    this.widht = canvas_width;
    this.height = canvas_height;
    this.current_level = level;
    this.game_scale = 24;
    this.delay = 0;
    this.delay_limit = 1000;
    this.enemy_limit = limit;
    this.speed = speed;
    this.score = 0;
    this.init();
  }

  init() {
    document.addEventListener("keydown", (evnt) => {
      if (!this.program_switcher) {
        if (evnt.key == "Escape") {
          console.log("exit");
        }
      }
    });
    this.store = new Store(this);
    this.map = new Maps(this);
    this.player = new Player(this);
    this.path_finder = new A_Star(this);
  }

  update() {
    player_health.innerHTML = this.player.health;
    game_score.innerHTML = this.score;
    this.delay = this.delay % this.delay_limit;
    this.delay++;
    this.player.updatePosition();
    this.store.update();
    if (this.player.health < 1) {
      cancelAnimationFrame(game);
      game_over.style.display = "block";
    }
    if (this.store.enemy.length < 1 && this.store.spauners.length < 1) {
      cancelAnimationFrame(game);
      game_win.style.display = "block";
    }
  }

  draw() {
    this.context.clearRect(0, 0, this.widht, this.height);
    this.map.draw();
    this.player.draw();
    this.store.draw();
  }
}

const script = new Game(
  level_data.level,
  level_data.max_enemys,
  level_data.speed
);
run_canvas();
function run_canvas() {
  game = requestAnimationFrame(run_canvas);
  script.update();
  script.draw();
}
