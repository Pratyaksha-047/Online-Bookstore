const books = document.querySelectorAll(".book");

[...books].map(book => {
  const cover = book.querySelector('.cover');
  const pattern = document.createElement('div');

  const coverIcon = book.querySelector('.cover-icon');
  const coverTitle = book.querySelector('.cover-title');

  const iconElement = document.createElement('div');
  iconElement.className = "icon"

  const title = cover.dataset.title;
  const svg = cover.dataset.icon;
  const coverPattern = cover.dataset.pattern;

  iconElement.style.backgroundImage = `url(${svg})`;
  coverIcon.appendChild(iconElement)

  coverTitle.textContent = title;

  cover.appendChild(pattern);
})