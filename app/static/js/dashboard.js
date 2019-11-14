$(document).ready(function(){
	$('[data-toggle="offcanvas"]').click(function(){
		$("#navigation").toggleClass("hidden-xs");
	});
 });
 
 
 // data-* attributes to scan when populating modal values
var ATTRIBUTES = ['myvalue', 'myvar', 'bb'];

$('[data-toggle="modal"]').on('click', function (e) {
  // convert target (e.g. the button) to jquery object
  var $target = $(e.target);
  // modal targeted by the button
  var modalSelector = $target.data('target');
  
  // iterate over each possible data-* attribute
  ATTRIBUTES.forEach(function (attributeName) {
    // retrieve the dom element corresponding to current attribute
    var $modalAttribute = $(modalSelector + ' #modal-' + attributeName);
    var dataValue = $target.data(attributeName);
    
    // if the attribute value is empty, $target.data() will return undefined.
    // In JS boolean expressions return operands and are not coerced into
    // booleans. That way is dataValue is undefined, the left part of the following
    // Boolean expression evaluate to false and the empty string will be returned
    $modalAttribute.text(dataValue || '');
  });
});

/* STUDENTS IGNORE THIS FUNCTION
 * All this does is create an initial
 * attendance record if one is not found
 * within localStorage.
 */
(function() {
  if (!localStorage.attendance) {
      console.log('Creating attendance records...');
      function getRandom() {
          return (Math.random() >= 0.5);
      }

      var nameColumns = $('tbody .name-col'),
          attendance = {};

      nameColumns.each(function() {
          var name = this.innerText;
          attendance[name] = [];

          for (var i = 0; i <= 11; i++) {
              attendance[name].push(getRandom());
          }
      });

      localStorage.attendance = JSON.stringify(attendance);
  }
}());


/* STUDENT APPLICATION */
$(function() {
  var attendance = JSON.parse(localStorage.attendance),
      $allMissed = $('tbody .missed-col'),
      $allCheckboxes = $('tbody input');

  // Count a student's missed days
  function countMissing() {
      $allMissed.each(function() {
          var studentRow = $(this).parent('tr'),
              dayChecks = $(studentRow).children('td').children('input'),
              numMissed = 0;

          dayChecks.each(function() {
              if (!$(this).prop('checked')) {
                  numMissed++;
              }
          });

          $(this).text(numMissed);
      });
  }

  // Check boxes, based on attendace records
  $.each(attendance, function(name, days) {
      var studentRow = $('tbody .name-col:contains("' + name + '")').parent('tr'),
          dayChecks = $(studentRow).children('.attend-col').children('input');

      dayChecks.each(function(i) {
          $(this).prop('checked', days[i]);
      });
  });

  // When a checkbox is clicked, update localStorage
  $allCheckboxes.on('click', function() {
      var studentRows = $('tbody .student'),
          newAttendance = {};

      studentRows.each(function() {
          var name = $(this).children('.name-col').text(),
              $allCheckboxes = $(this).children('td').children('input');

          newAttendance[name] = [];

          $allCheckboxes.each(function() {
              newAttendance[name].push($(this).prop('checked'));
          });
      });

      countMissing();
      localStorage.attendance = JSON.stringify(newAttendance);
  });

  countMissing();
}());

