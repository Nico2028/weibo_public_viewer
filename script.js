document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".media img").forEach(img => {
    img.style.cursor = 'pointer';
    img.addEventListener('click', () => {
      const overlay = document.createElement('div');
      Object.assign(overlay.style, {
        position: 'fixed', top: 0, left: 0,
        width: '100%', height: '100%',
        background: 'rgba(0,0,0,0.8)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 9999
      });
      const big = document.createElement('img');
      big.src = img.src;
      big.style.maxWidth = '90%';
      big.style.maxHeight = '90%';
      overlay.appendChild(big);
      overlay.addEventListener('click', () => overlay.remove());
      document.body.appendChild(overlay);
    });
  });
});
