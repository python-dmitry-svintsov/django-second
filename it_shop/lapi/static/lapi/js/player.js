const MOOVE_KEY_UP_CODES = ["ArrowUp", "KeyW"];
const MOOVE_DOWN_KEY_CODES = ["ArrowDown", "KeyS"];
const MOOVE_LEFT_KEY_CODES = ["ArrowLeft", "KeyA"];
const MOOVE_RIGHT_KEY_CODES = ["ArrowRight", "KeyD"];
/*Этот массив нам нужен для нашего флага this.isMooving*/
const ALL_MOOVE_KEY_CODES = [
  ...MOOVE_KEY_UP_CODES,
  ...MOOVE_DOWN_KEY_CODES,
  ...MOOVE_LEFT_KEY_CODES,
  ...MOOVE_RIGHT_KEY_CODES,
];

export class Player {
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
    this.image.src = "/static/lapi/img/player.png";
    this.imageWidth = 24;
    this.imageHeight = 24;
    this.imageLenght = 1;
    /*Эта переменная нам нужна будет как счетчик для прокрутки анимации*/
    this.imageTick = 0;
    /*Флажок движения*/
    this.isMooving = false;
    /*Speed of player_tank*/
    this.velocity = 1 / this.scale;
    /*Этот блок для управления клавишами*/
    /**/
    /*Создаем колекцию типа Мап - ее + в том что там можно в качестве ключа хранить что угодно*/
    /*При нажатии на клавишу в нее будет добавлятся код нажатой клавиши, при отпускании он будет удалятся*/
    this.keyMap = new Map();
    document.addEventListener("keydown", (event) => {
      if (!this.needKeys(ALL_MOOVE_KEY_CODES)) {
        this.keyMap.set(event.code, true);
        this.isMooving = true;
      }
      if (event.key == " " && this.bag.weapon) {
        this.main.add_project_tile(this.x, this.y, this.imageLenght);
        this.main.toggle(this.main.crossbow);
        this.bag.weapon = false;
      }
    });
    document.addEventListener("keyup", (event) => {
      this.keyMap.delete(event.code);
      this.isMooving = false;
    });
    /*-----------рюкзачок персонажа-----------------*/
    this.bag = { key: false, weapon: false };
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

  /*Метод проверяет наш массив на нажатые клавиши, ему в качестве аргшумента предается
	наши массивы с кодами клавиш, и он перебирает нашу коллекцию с ключами для поиска
	нужного кода клавиши и возвращает истину или ложь...*/
  needKeys(key) {
    return key.some((item) => this.keyMap.get(item));
  }

  /**/
  updatePosition() {
    if (this.needKeys(MOOVE_KEY_UP_CODES)) {
      this.imageLenght = 0;
      if (this.main.player_collision(this.x, this.y - this.velocity)) {
        this.y -= this.velocity;
      }
    }
    if (this.needKeys(MOOVE_DOWN_KEY_CODES)) {
      this.imageLenght = 1;
      if (this.main.player_collision(this.x, this.y + this.velocity)) {
        this.y += this.velocity;
      }
    }
    if (this.needKeys(MOOVE_LEFT_KEY_CODES)) {
      this.imageLenght = 2;
      if (this.main.player_collision(this.x - this.velocity, this.y)) {
        this.x -= this.velocity;
      }
    }
    if (this.needKeys(MOOVE_RIGHT_KEY_CODES)) {
      this.imageLenght = 3;
      if (this.main.player_collision(this.x + this.velocity, this.y)) {
        this.x += this.velocity;
      }
    }
  }
  hit() {
    this.health -= 1;
  }
}
