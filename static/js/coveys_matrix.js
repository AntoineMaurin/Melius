function toggleMyTasks() {

  var my_tasks = document.getElementById("my-tasks");
  var matrix = document.getElementsByClassName('matrix-container col-8');

  var button = document.getElementsByClassName('see-my-tasks-button');

  if (my_tasks.style.display === "none") {
    my_tasks.style.display = "block";
    matrix[0].classList.remove("offset-2");
    matrix[0].classList.add("offset-3");
    button[0].classList.remove("turn-around");
  } else {
    my_tasks.style.display = "none";
    matrix[0].classList.remove("offset-3");
    matrix[0].classList.add("offset-2");
    button[0].classList.add("turn-around");
  }
}

function openChangeMatrixQuarter(e) {
  var box = document.getElementById("change-matrix-box")
  box.style.display = "block";
  var left  = e.clientX  + "px";
  var top  = e.clientY  + "px";
  console.log(left, top);

  box.style.left = left;
  box.style.top = top;
}

function closeChangeMatrixQuarter() {
  document.getElementById("change-matrix-box").style.display = "none";
}

$(document).ready(function() {

  $(".task-box").click(function(){

    var task_id = $(this).attr('id');
    $("#change-matrix-task-id").val(task_id);

    $("#matrix-quarter-1").click(function(){

      var destination = "top-left";

      $("#change-matrix-destination").val(destination);

    });

    $("#matrix-quarter-2").click(function(){

      var destination = "top-right";

      $("#change-matrix-destination").val(destination);

    });

    $("#matrix-quarter-3").click(function(){

      var destination = "bottom-left";

      $("#change-matrix-destination").val(destination);

    });

    $("#matrix-quarter-4").click(function(){

      var destination = "bottom-right";

      $("#change-matrix-destination").val(destination);

    });

  });

});
