const menu = document.querySelector("#menuIcon");
const list = document.querySelector('.nav-list');

menu.addEventListener('click', () => list.classList.toggle("hiddenMenu"));