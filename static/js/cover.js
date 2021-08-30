const $tableID = $('#table');
const $BTN = $('#export-btn');
const $EXPORT = $('#export');
const TOTALSURFS = 6;

$(document).ready(function(){
  const elements = $tableID.find('tbody tr');
  var i = elements.length - 1;
  console.log(i)
  if (i > 1)
    document.getElementById("submit").disabled = false;
  else
    document.getElementById("submit").disabled = true;
});

$('.table-add').on('click', 'button', () => {
  const elements = $tableID.find('tbody tr');
  var i = elements.length - 1;
  let materials = ['E-SK10', 'J-LAF7', 'J-KZFH1', 'BASF6', 'P-SF68', 'SF56A', 'N-FK51A', 'N-FK58', 'N-FK5', 'N-PK51',
             'N-PK52A', 'N-BK10', 'N-BK7', 'N-BK7G18', 'N-PSK3', 'N-PSK53A', 'N-ZK7', 'N-ZK7A', 'N-K7', 'N-K5',
             'N-K10', 'N-KF9', 'N-BAK2', 'N-BAK1', 'N-BAK4', 'N-BALF5', 'N-KZFS2', 'N-BALF4', 'N-SK11', 'N-SK5',
             'N-SK14', 'N-SK16', 'N-SK4', 'N-SK2', 'N-SSK2', 'N-SSK5', 'N-SSK8', 'N-LAK21', 'N-LAK7', 'N-LAK22',
             'N-LAK12', 'N-LAK14', 'N-LAK9', 'N-LAK35', 'N-LAK34', 'N-LAK8', 'N-LAK10', 'N-LAK33B', 'N-LAK33A',
             'N-F2', 'N-SF2', 'N-SF5', 'N-SF8', 'N-SF15', 'N-SF1', 'N-SF10', 'N-SF4', 'N-SF14', 'N-SF11', 'N-SF6',
             'N-SF57', 'N-SF66', 'N-SF6HT', 'N-BAF10', 'N-BAF52', 'N-KZFS4', 'N-BAF4', 'N-BAF51', 'N-KZFS11',
             'N-KZFS5', 'N-BASF2', 'N-BASF64', 'N-KZFS8', 'N-LAF7', 'N-LAF2', 'N-LAF37', 'N-LAF35', 'N-LAF34',
             'N-LAF21', 'N-LAF33', 'N-LASF9', 'N-LASF44', 'N-LASF43', 'N-LASF41', 'N-LASF45', 'N-LASF31A',
             'N-LASF40', 'N-LASF46A', 'N-LASF46B', 'N-LASF35', 'N-LAK9CP', 'CAF2', 'AIR'];
  var options = '';
  materials.forEach(item => {
    if (item === 'AIR')
      options = options + `<option value="` + item + `" selected="selected">` + item + `</option>`
    else
      options = options + `<option value="` + item + `">` + item + `</option>`
  });
  
  if (i > 0)
    document.getElementById("submit").disabled = false;
  else
    document.getElementById("submit").disabled = true;

  const newTr = `
  <tr class="hide">
    <td class="pt-3-half">` + i + `</td>
    <td class="pt-3-half"><input type="number" name="position" value="0.0"></td>
    <td class="pt-3-half"><input type="number" name="max_apt" value="0.0"></td>
    <td class="pt-3-half">
      <select name="glass">` + options + `</select>
    </td>
    <td class="pt-3-half"><input type="number" name="stg_pts_obj" value="0.0"></td>
    <td class="pt-3-half"><input type="number" name="stg_pts_img" value="0.0"></td>
    <td>
      <span class="table-remove"><button type="button" class="btn btn-success" data-dismiss="modal"><i class="fas fa-trash-alt"></i></button></span>
    </td>
  </tr>`;
  if (elements.length < TOTALSURFS) {
    $tableID.find('table tr:last').before(newTr);
  }
});
$tableID.on('click', '.table-remove', function () {
  let tableBody = document.querySelector('tbody');
  let tableRows = tableBody.querySelectorAll('tr');
  var newIdx = 1;
  tableRows.forEach((row, currentIdx) => {
    if (row != $(this).parents('tr')[0] && currentIdx != 0 && currentIdx != tableRows.length - 1) {
      row.cells[0].innerHTML = newIdx;
      newIdx++;
    }
  });
  console.log(newIdx)
  if (newIdx <= 1)
    document.getElementById("submit").disabled = true;
  else
    document.getElementById("submit").disabled = false;

  $(this).parents('tr').detach();
});
// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;
$BTN.on('click', () => {
  const $rows = $tableID.find('tr:not(:hidden)');
  const headers = [];
  const data = [];
  // Get the headers (add special header logic here)
  $($rows.shift()).find('th:not(:empty)').each(function () {
    headers.push($(this).text().toLowerCase());
  });
  // Turn all existing rows into a loopable array
  $rows.each(function () {
    const $td = $(this).find('td');
    const h = {};
    // Use the headers from earlier to name our hash keys
    headers.forEach((header, i) => {
      h[header] = $td.eq(i).text();
    });
    data.push(h);
  });
  // Output the result
  $EXPORT.text(JSON.stringify(data));
});
