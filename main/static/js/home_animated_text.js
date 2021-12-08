let parent = document.querySelectorAll('.animate-text');
for (let i = 0; i < parent.length; i++) {
  parent[i].style.width = parent[i].children[0].clientWidth + "px";
};