document.addEventListener('DOMContentLoaded', function () {
  var routes = ['company-registration.html', 'properties.html', 'agent-accounting.html', 'investment.html'];
  var buttons = document.querySelectorAll('[class*="_taskGrid_"] button');
  buttons.forEach(function (button, index) {
    button.addEventListener('click', function () { window.location.href = routes[index] || 'contact.html'; });
  });
});
