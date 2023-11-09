export class ProjectTile {
  constructor(store, x, y, direct) {
    this.main = store;
    this.x = x;
    this.y = y;
    this.direct = direct;
    this.context = this.main.context;
    this.color = "#8B0000";
    this.radius = 3;
    this.velocity = 3;
  }

  draw() {
    this.context.beginPath();
    this.context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    //! This.color is color of fill figure
    this.context.fillStyle = this.color;
    this.context.fill();
  }

  update() {
    if (this.direct === 0) {
      this.y -= this.velocity;
    }
    if (this.direct === 1) {
      this.y += this.velocity;
    }
    if (this.direct === 2) {
      this.x -= this.velocity;
    }
    if (this.direct === 3) {
      this.x += this.velocity;
    }
  }
}
