document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a.reference.external').forEach(a => {
    a.setAttribute('target','_blank');
    a.setAttribute('rel','noopener noreferrer');
  });
});