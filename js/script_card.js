const animatedElement = document.querySelector('.animated');
    window.addEventListener('scroll', function() {
      const rect = animatedElement.getBoundingClientRect();
      if (rect.top <= window.innerHeight) {
        animatedElement.classList.add('visible');
      } else {
        animatedElement.classList.remove('visible');
      }
    });