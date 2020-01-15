document.addEventListener('DOMContentLoaded', function() {
  var checkPageButton = document.getElementById('checkPage');
  checkPageButton.addEventListener('click', function() {

    chrome.tabs.getSelected(null, function(tab) {
      url = tab.url
      window.open("http://127.0.0.1:5000/api/extraction?url="+url)
    });
  }, false);
}, false);
