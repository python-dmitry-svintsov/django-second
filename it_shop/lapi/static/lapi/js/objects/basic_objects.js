class Base {
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
  }

  draw() {
    this.context.drawImage(
      this.img,
      0,
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

export class Wall extends Base {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/${this.level_style}/wall.jpg`;
  }
}

export class Door_Hor extends Base {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/0/door.png`;
    /*проходимость*/
    this.subX = 0;
    this.close = true;
  }
  draw() {
    this.context.drawImage(
      this.img,
      this.subX,
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

export class Door_Vert extends Base {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/0/door-vert.png`;
    /*проходимость*/
    this.subX = 0;
    this.close = true;
  }
  draw() {
    this.context.drawImage(
      this.img,
      this.subX,
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

export class Moove extends Base {
  constructor(storage, context, x, y) {
    super(storage, context, x, y);
    this.img.src = `/static/lapi/img/${this.level_style}/moove.png`;
    this.velocity = 1 / this.scale;
    this.direction = new Map();
    this.get_ways();
  }
  get_ways() {
    this.direction.set(0, [0, -1]);
    this.direction.set(1, [0, 1]);
    this.direction.set(2, [-1, 0]);
    this.direction.set(3, [1, 0]);
  }
}
