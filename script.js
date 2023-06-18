window.addEventListener("scroll", function() {
    var fadeContainers = document.querySelectorAll(".fade-container");
    var screenPosition;
  
    // Adjust screenPosition based on device screen size
    if (window.innerWidth < 768) {
      // For screens smaller than 768px (mobile devices)
      screenPosition = window.innerHeight / 1.1;
    } else {
      // For larger screens
      screenPosition = window.innerHeight / 1.3;
    }
  
    fadeContainers.forEach(function(container) {
      var fadeContainerPosition = container.getBoundingClientRect().top;
  
      if (fadeContainerPosition < screenPosition) {
        container.classList.add("fade-in");
      }
    });
  });

  const containers = document.querySelectorAll('.fade-down-container');

  containers.forEach((container, index) => {
    container.style.animationDelay = `${index * 0.25}s`;
  });
  