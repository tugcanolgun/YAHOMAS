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