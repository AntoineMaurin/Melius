const pickr = Pickr.create({
    el: '.color-picker',
    theme: 'classic', // or 'monolith', or 'nano'
    default: '#21756b',

    swatches: [
        '#1abc9c',
        '#16a085',
        '#2ecc71',
        '#27ae60',
        '#3498db',
        '#2980b9',
        '#9b59b6',
        '#8e44ad',
        '#34495e',
        '#e67e22',
        '#d35400',
        '#e74c3c',
        '#c0392b',
        '#f39c12'
    ],

    components: {

        // Main components
        preview: true,
        opacity: false,
        hue: true,

        // Input / output Options
        interaction: {
            hex: true,
            rgba: false,
            hsla: false,
            hsva: false,
            cmyk: false,
            input: true,
            clear: false,
            save: true
        }
    }
});

function openEditListForm() {
  var list_element = document.getElementById("tasklists");

  var list_selected_name = list_element.options[list_element.selectedIndex].text;
  var list_id = list_element.options[list_element.selectedIndex].value;

  document.getElementById("edit-list-title").innerHTML = list_selected_name;
  document.getElementById("edit-list-name").value = list_selected_name;
  document.getElementById("edit-list-id").value = list_id;

  document.getElementById("EditListForm").style.display = "block";

  pickr.on('save', (color, instance) => {

    var color = pickr.getSelectedColor().toHEXA().toString();
    document.getElementById("edit-list-color").value = color;
    console.log($("input[name='list_color']").val());
  });

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


  $(".new-list-form").click(function(){

    $("#NewListForm").css("display", "block");

    pickr.on('save', (color, instance) => {

      var color = pickr.getSelectedColor().toHEXA().toString();
      $("input[name='list_color']").val(color);
      console.log($("input[name='list_color']").val());
    });
  });

});
