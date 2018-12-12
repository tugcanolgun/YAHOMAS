function changeBody(name, url) {
    modal = document.querySelector('#myModal');
    content = modal.querySelector('.modal-body');
    content.innerHTML = 'Do you want to delete `<b>' + name + '</b>`?';
    link = modal.querySelector('#modal-delete-button');
    link.href = url;
    $('#myModal').modal('show');
}
$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text(recipient)
})

$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});

// Put a listener on start date for auto input to end date input
document.getElementById("id_start_date").addEventListener('change', doThing);

function doThing(){
    // This function is now absolete
    end_date = document.getElementById("id_end_date");
    end_date_value = end_date.value
    start_date_value = document.getElementById("id_start_date").value;
    // If end date value is empty
    if (end_date_value === '') {
        end_date.value = start_date_value;
        end_date.focus();
    } else {
        // If start date is earlier than end date
        if (new Date(start_date_value).valueOf() < new Date(end_date_value).valueOf()) {
            end_date.value = start_date_value;
            end_date.focus();
        }
    }
}

// Sortable tables
$(document).ready(function () {
$('#dtBasicExample').DataTable();
$('.dataTables_length').addClass('bs-select');
});