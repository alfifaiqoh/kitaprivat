document.addEventListener('DOMContentLoaded', function () {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebarOverlay');
  var toggle = document.getElementById('sidebarToggle');

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  if (toggle && sidebar) {
    toggle.addEventListener('click', function () {
      if (sidebar.classList.contains('open')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }

  if (sidebar) {
    sidebar.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth < 768) closeSidebar();
      });
    });
  }
});
