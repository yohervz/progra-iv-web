// Main interactive scripts for Yoher Vazquez Tech Courses platform

document.addEventListener("DOMContentLoaded", () => {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // Copy enrollment code to clipboard if button exists
  const copyBtn = document.getElementById("copyEnrollmentBtn");
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const codeElement = document.getElementById("enrollmentCodeText");
      if (codeElement) {
        navigator.clipboard.writeText(codeElement.innerText.trim()).then(() => {
          const originalText = copyBtn.innerHTML;
          copyBtn.innerHTML = '<i class="bi bi-check-lg"></i> ¡Copiado!';
          setTimeout(() => {
            copyBtn.innerHTML = originalText;
          }, 2000);
        });
      }
    });
  }

  // Auto-dismiss alerts after 6 seconds
  const autoDismissAlerts = document.querySelectorAll(".alert-dismissible");
  autoDismissAlerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 6000);
  });
});
