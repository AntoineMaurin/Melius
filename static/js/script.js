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

function createTitle(title_id, title_name) {
  var new_title = document.createElement("p");

  document.getElementById(title_id).appendChild(new_title);

  new_title.classList.add("ml-3");
  new_title.innerHTML = title_name;

}

$(document).ready(function() {


  $(".new-task-button").click(function(){

    $("#empty-task-form-header").css('background-color', '#21756b');
    $("#empty-task-form-title").html("Nouvelle tâche");

    $("#empty-task-form-name").val("");
    $("#empty-task-form-date").val("");
    $("#empty-task-form-description").val("");

    $("#empty-task-form-submit-add-button").html('Ajouter');
    $("#empty-task-form-submit-action").attr("action", "/addtask");

  });

  $(".task-box").click(function(){
    var task_id = $(this).attr('id');

    $.ajax({
      type: "GET",
      url: "/edittask/" + task_id,
      data: {},
      dataType: "json",
      success: function editTaskForm(response) {
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


  $(".del-task").click(function(){
      var task_id = $(this).parent().parent().parent().parent().attr('id');

      $.ajax({
        type: "GET",
        url: "/deltask/" + task_id,
        data: {},
        dataType: "json",
        success: function() {


          if ( $("#" + task_id).siblings().length < 2 ) {
            var title_class = $("#" + task_id).parent().attr('class');
            console.log(title_class);
            $("." + title_class).remove();
          }

          $("#" + task_id).remove();
          $(".new-task-button").trigger('click');

        },
        error: function(rs, e) {
          console.log(e);
        }
      });
    });

});








// var task_element = $("#" + response['task_id']).remove().clone();
//
// if (response['is_done']) {
//
//   if ($("#finished-tasks-list > * ").length < 1) {
//
//     createTitle("finished-tasks-list", "Tâches terminées");
//
//   }
//
//   $("#finished-tasks-list").append(task_element);
//   $("#" + response['task_id'] + " .last-icon-task").removeClass().addClass("fas fa-arrow-circle-up fa-2x text-darkblue last-icon-task");
//
// } else {
//
//   if ($("#finished-tasks-list > * ").length < 2) {
//     removeTitle("finished-tasks-list");
//   }
//
//   $("#no-date-tasks-list").append(task_element);
// }
