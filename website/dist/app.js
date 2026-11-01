const filter = document.querySelector('#filter');
filter.addEventListener('change', () => {
  let visible = 0;
  document.querySelectorAll('[data-type]').forEach(card => {
    card.hidden = filter.value !== 'all' && card.dataset.type !== filter.value;
    if (!card.hidden) visible += 1;
  });
  document.querySelector('#count').textContent = `显示 ${visible} 个规划方向`;
});
