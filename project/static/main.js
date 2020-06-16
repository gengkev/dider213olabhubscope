// Not using fancy js features for compatibility reasons, sry
(function () {
  'use strict';

  var elts = document.getElementsByClassName('replace-datetime');
  for (var i = 0; i < elts.length; i++) {
      var orig = elts[i].textContent.replace(/^\s+|\s+$/g, '');
      var dt = luxon.DateTime.fromISO(orig);
      var out = dt.setZone('local')
          .toLocaleString(luxon.DateTime.DATETIME_FULL);
      elts[i].textContent = out;
  }

  elts = document.getElementsByClassName('replace-timezone');
  for (i = 0; i < elts.length; i++) {
      elts[i].textContent = luxon.DateTime.local().zoneName;
  }

})();
