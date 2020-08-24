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



function closeBaseListForm() {
  document.getElementById("BaseListForm").style.display = "none";
}

function closeDeleteListForm() {
  document.getElementById("DeleteListForm").style.display = "none";
}


$(document).ready(function() {

  set_current_category();

  set_category_colors();

  $(document).on('change','#tasklists', function(){
    set_category_colors();
  });

  function set_category_colors() {

    var selected_id = $('#tasklists').children("option:selected").val();
    var category_color = $("[href='/show_tasklist/" + selected_id + "']").css("background-color");

    $("#empty-task-form-header").css('background-color', category_color);
    $("#empty-task-form-submit-add-button").css('background-color', category_color);
    $(".category-buttons").css('color', category_color);
    $(".category-buttons").css('transition', '0.3s');
    $(".category-buttons").children().css('color', 'inherit');

  }

   function update_form_when_color_saved() {
     pickr.on('save', (color, instance) => {

       var color = pickr.getSelectedColor().toHEXA().toString();
       $("input[name='list_color']").val(color);

       $(".category_header").css("background-color", color);
       $(".submit-list-form").css("background-color", color);
     });
   }

   function set_current_category() {
     var current_category_color = $(".sort-by-buttons").attr("href");
     current_category_id = current_category_color.replace(/[^0-9]/gi, '');

     category_to_set = $("option[value='" + current_category_id + "']")
     category_to_set.attr("selected", "selected");
   }

  $(".new-task-button").click(function () {

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
        $("#empty-task-form-header").css('background-color', response['category_color']);
        $("#empty-task-form-title").html(response["task_name"]);

        var category = response['category_name'];

        $('option:contains('+ category +')').attr("selected","selected");
        $("#empty-task-form-name").val(response["task_name"]);
        $("#empty-task-form-date").val(response["due_date"]);
        $("#empty-task-form-description").val(response["description"]);

        $("#empty-task-form-submit-add-button").html('Modifier');
        $("#empty-task-form-submit-action").attr("action", "/updatetask/" + response["task_id"]);
        $("#empty-task-form-submit-add-button").css('background-color', response['category_color']);
        $(".category-buttons").css('color', response['category_color']);
        $(".category-buttons").css('transition', '0.3s');
        $(".category-buttons").children().css('color', 'inherit');

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

          $("#" + task_id).hide(600);
          $(".new-task-button").trigger('click');

        },
        error: function(rs, e) {
          console.log(e);
        }
      });
    });


  $(".new-list-form").click(function(){

    $("#BaseListForm").css("display", "block");
    $(".category_name").html("Nouvelle catégorie");
    $("#list_name").val("");
    $(".category_header").css("background-color", "#21756b");
    $(".pcr-button").css("color", "#21756b");
    $(".submit-list-form").css("background-color", "#21756b");

    update_form_when_color_saved();

  });

    $("#edit-list-form-button").click(function(){

      $("#BaseListForm").css("display", "block");

      var category_name = $('#tasklists').children("option:selected").text();
      var category_id = $('#tasklists').children("option:selected").val();
      var category_color = $("[href='/show_tasklist/" + category_id + "']").css("background-color");

      $(".category_header").css("background-color", category_color);
      $(".category_name").text("Modifier");
      $("#list_name").val(category_name);
      $("#category_form_action").attr("action", "/editcategory");
      $(".submit-list-form").text("Modifier");
      $(".submit-list-form").css("background-color", category_color);
      $(".pcr-button").css("color", category_color);
      $(".list_color").val("category_color");
      $(".list_id").val(category_id);

      update_form_when_color_saved();

    });

    $("#delete-list-form-button").click(function(){

      $("#DeleteListForm").css("display", "block");

      var category_name = $('#tasklists').children("option:selected").text();
      var category_id = $('#tasklists').children("option:selected").val();
      var category_color = $("[href='/show_tasklist/" + category_id + "']").css("background-color");

      var start_msg = "Êtes-vous sûr de vouloir supprimer la catégorie "
      var end_msg =  " et toutes les tâches qu'elle contient ?";

      $("#delete_header").css("background-color", category_color);
      $("#delete_list_title").text(category_name);
      $("#delete_message").text(start_msg + category_name + end_msg);
      $("#delete_list_id").val(category_id);
      $(".submit-list-form").css("background-color", category_color);
    });

});
