import { distanceBeetwenTwoPoints } from "../utils/distance.js";

class Npc {
  constructor(main, x, y) {
    this.main = main;
    this.x = x;
    this.y = y;
    this.context = this.main.context;
    this.scale = this.main.scale;
    /**/
    this.radius = 12;
    this.health = 1;
    /*Ипортируем наш спрайт что мы рисовали в GIMP*/
    this.image = new Image();
    this.image.src;
    this.imageWidth = 24;
    this.imageHeight = 24;
    this.imageLenght = 0;
    this.direction_pointer = this.imageLenght;
    /*ways*/
    this.ways = new Map();
    this.direction = new Map();
    this.get_ways();
    /*Эта переменная нам нужна будет как счетчик для прокрутки анимации*/
    this.imageTick = 0;
    /*Флажок движения*/
    this.isMooving = true;
    /* флажок занятости*/
    this.isGo = false;
    this.previous_typic = false;
    this.previous_cord = [this.x, this.y];
    this.ceil_coord = [this.x, this.y];
    /*Speed of player_tank*/
    this.velocity = 1 / this.scale;
    this.demaged = false;
  }

  get_ways() {
    /*Смотрим по правую руку от нашего текущего положения*/
    this.ways.set(0, [1, 0]);
    this.ways.set(1, [0, -1]);
    this.ways.set(2, [-1, 0]);
    this.ways.set(3, [0, 1]);
    /*-------------------------------------------------------------------------*/
    this.direction.set(0, [0, -1]);
    this.direction.set(1, [-1, 0]);
    this.direction.set(2, [0, 1]);
    this.direction.set(3, [1, 0]);
  }

  draw() {
    const imageTickLimit = 18;
    /*Используя тернарный оператор задаем значение переменной
		которая отвечает за каоординаты картинки по иксу*/
    let subX = 0;
    if (!this.isMooving) {
      subX = 0;
      this.imageTick = 0;
    } else {
      subX =
        this.imageTick > imageTickLimit ? this.imageWidth * 2 : this.imageWidth;
      this.imageTick++;
    }
    /*Если Наш счетчик вылез за пределы координат, обнуляем его*/
    if (this.imageTick > imageTickLimit * 2) this.imageTick = 0;
    /*Этим методом мы рисуем картинку*/
    this.context.drawImage(
      this.image,
      subX,
      this.imageLenght * this.imageHeight,
      this.imageWidth,
      this.imageHeight,
      (this.x - 0.5) * this.scale,
      (this.y - 0.5) * this.scale,
      this.imageWidth,
      this.imageHeight
    );
  }

  moove() {
    if (!this.isGo) {
      var cur_pos = this.ways.get(this.direction_pointer);
      var x = Math.floor(cur_pos[0] + this.x);
      var y = Math.floor(cur_pos[1] + this.y);
      if (this.main.map_collison(x, y)) {
        this.isGo = true;
        this.ceil_coord = [x + 0.5, y + 0.5];
        this.direction_pointer -= 1;
        if (this.direction_pointer < 0) this.direction_pointer = 3;
        this.imageLenght = this.direction_pointer;
      } else {
        /*Ввожу эту переменную для того чтобы картинка не мельтешила при поиске пути, опитимизировал алгоритм*/
        this.direction_pointer += 1;
        if (this.direction_pointer > 3) this.direction_pointer = 0;
      }
    }

    /*-------------------------------------*/
    if (this.isGo) {
      var dir = this.direction.get(this.direction_pointer);
      this.x += dir[0] * this.velocity;
      this.y += dir[1] * this.velocity;
    }
    /*---------------------------------- */
    if (
      distanceBeetwenTwoPoints(
        this.x,
        this.y,
        this.ceil_coord[0],
        this.ceil_coord[1]
      ) < 0.05
    ) {
      this.x = this.ceil_coord[0];
      this.y = this.ceil_coord[1];
      this.isGo = false;
    }
  }
}

export class Type_1 extends Npc {
  constructor(main, x, y) {
    super(main, x, y);
    this.image.src = "/static/lapi/img/enemy_1.png";
  }
}

export class Spider extends Npc {
  constructor(main, x, y) {
    super(main, x, y);
    this.image.src = "/static/lapi/img/spider.png";
    this.velocity = 1 / (this.scale * 2);
  }
}
