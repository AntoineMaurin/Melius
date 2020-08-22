function openNewListForm() {
  document.getElementById("NewListForm").style.display = "block";
}

function openEditListForm() {
  var list_element = document.getElementById("tasklists");

  var list_selected_name = list_element.options[list_element.selectedIndex].text;
  var list_id = list_element.options[list_element.selectedIndex].value;

  document.getElementById("list_title").innerHTML = list_selected_name;
  document.getElementById("list_name").value = list_selected_name;
  document.getElementById("list_id").value = list_id;

  document.getElementById("EditListForm").style.display = "block";
}

function closeNewListForm() {
  document.getElementById("NewListForm").style.display = "none";
}

function closeEditListForm() {
  document.getElementById("EditListForm").style.display = "none";
}

function openDeleteListForm() {
  var list_element = document.getElementById("tasklists");

  var list_selected_name = list_element.options[list_element.selectedIndex].text;
  var list_id = list_element.options[list_element.selectedIndex].value;


  var start_msg = "Êtes-vous sûr de vouloir supprimer la catégorie "
  var end_msg =  " et toutes les tâches qu'elle contient ?";

  document.getElementById("list_title_to_delete").innerHTML = list_selected_name
  document.getElementById("delete_message").innerHTML = start_msg + list_selected_name + end_msg;
  document.getElementById("delete_list_id").value = list_id;


  document.getElementById("DeleteListForm").style.display = "block";
}

function closeDeleteListForm() {
  document.getElementById("DeleteListForm").style.display = "none";
}


$(document).ready(function() {

  $(".task-box").click(function(){
    var task_id = $(this).attr('name');
    $.ajax({
      type: "GET",
      url: "/ajaxedit/" + task_id,
      data: {},
      dataType: "json",
      success: function(response) {
        // $("#empty-task-form").fadeTo(300);
        $("#empty-task-form-header").css('background-color', response['category_color']);
        $("#empty-task-form-title").html(response["task_name"]);

        var category = response['category_name'];

        $('option:contains('+ category +')').attr("selected","selected");
        $("#empty-task-form-name").val(response["task_name"]);
        $("#empty-task-form-date").val(response["due_date"]);
        $("#empty-task-form-description").val(response["description"]);

        $("#empty-task-form-submit-add-button").html('Modifier');
        $("#empty-task-form-submit-action").attr("action", "/updatetask/" + response["task_id"]);


      },
      error: function(rs, e) {
        console.log(e);
      }
    });
  });
  $("#change-task-state").click(function(){
      // var task_id = $(this).attr('name');
      // console.log(task_id);
      console.log("helloow");
    });

});
//
// $(document).ready(function() {
//
//   $('#like').click(function(){
//       $.ajax({
//                type: "POST",
//                url: "{% url 'like' %}",
//                data: {'slug': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//                dataType: "json",
//                success: function(response) {
//                       alert(response.message);
//                       alert('Company likes count is now ' + response.likes_count);
//                 },
//                 error: function(rs, e) {
//                        alert(rs.responseText);
//                 }
//           });
//     })
//
// })
