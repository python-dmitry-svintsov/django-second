class Base_Animated {
  constructor(storage, context, x, y) {
    this.storage = storage;
    this.context = context;
    this.level_style = this.storage.level_style;
    this.scale = this.storage.scale;
    /*----------------------------------------------------------*/
    this.x = x;
    this.y = y;
    /*----------------------------------------------------------*/
    this.img = new Image();
    this.img.src;
    this.img_Width = this.scale;
    this.img_Height = this.scale;
    this.imageTick = 0;
    /*количество кадров анимации*/
    this.frames = 3;
  }
  draw() {
    const imageTickLimit = 18;
    /*Используя тернарный оператор задаем значение переменной
		которая отвечает за каоординаты картинки по иксу*/
    let subX = 0;
    if (this.imageTick > imageTickLimit) subX += this.img_Width;
    this.imageTick++;
    /*Если Наш счетчик вылез за пределы координат, обнуляем его*/
    if (this.imageTick > imageTickLimit * 2) this.imageTick = 0;
    if (subX > this.img_Width * this.frames) subX = 0;
    /*Этим методом мы рисуем картинку*/
    this.context.drawImage(
      this.img,
      subX,
      0,
      this.img_Width,
      this.img_Height,
      (this.x - 0.5) * this.scale,
      (this.y - 0.5) * this.scale,
      this.img_Width,
      this.img_Height
    );
  }
}

export class Key extends Base_Animated {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/0/key.png`;
    this.taked = false;
  }
}

export class Target extends Base_Animated {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/0/target.png`;
    this.frames = 4;
  }
}

export class Weapon extends Base_Animated {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/0/weapon.png`;
    this.frames = 3;
    this.taked = false;
  }
}

export class Spauner extends Base_Animated {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/0/spauner.png`;
    this.frames = 3;
    this.demaged = false;
  }
}
