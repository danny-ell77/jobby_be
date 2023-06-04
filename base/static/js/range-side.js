//one range job
var slider = document.getElementById("myRange");
var output = document.getElementById("default-side");
output.innerHTML = slider.value;
slider.oninput = function () {
  output.innerHTML = this.value;
  const value = this.value;
  this.style.background = `linear-gradient(to right, #14A077 0%, #14A077 ${value}%, #ddd ${value}%, #ddd 0%)`;
};
