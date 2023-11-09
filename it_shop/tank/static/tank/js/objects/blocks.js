export class Block1 {
  constructor(x, y, context, scale) {
    this.x = x;
    this.y = y;
    this.context = context;
    this.scale = scale;
    this.radius = this.scale / 2;
    this.color_1 = "#808080";
    this.color_2 = "#A9A9A9";
  }
  draw() {
    this.context.strokeStyle = this.color_1;
    this.context.beginPath();
    this.context.roundRect(
      (this.x - 0.5) * this.scale + 1,
      (this.y - 0.5) * this.scale + 1,
      this.scale - 2,
      this.scale - 2,
      2
    );
    this.context.fillStyle = this.color_2;
    this.context.fill();
    this.context.stroke();
  }
}

export class Block2 extends Block1 {
  constructor(x, y, context, scale) {
    super(x, y, context, scale);
    this.color_1 = "#DC143C";
    this.color_2 = "#CD5C5C";
  }
}

export class Block3 extends Block1 {
  constructor(x, y, context, scale) {
    super(x, y, context, scale);
    this.color_1 = "#2F4F4F";
    this.color_2 = "#000000";
  }
}
