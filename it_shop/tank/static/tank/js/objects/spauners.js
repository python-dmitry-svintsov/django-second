export class Spauner {
  constructor(x, y, context, scale) {
    this.x = x;
    this.y = y;
    this.context = context;
    this.scale = scale;
    this.radius = this.scale / 2;
    this.health = 10;
    this.color_1 = "#7B68EE";
    this.color_2 = "#1E90FF";
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

  hit() {
    this.health--;
  }
}
