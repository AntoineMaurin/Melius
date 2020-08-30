function toggleMyTasks() {

  var my_tasks = document.getElementById("my-tasks");
  var button = document.getElementsByClassName('see-my-tasks-button');

  if (my_tasks.style.display === "none") {
    my_tasks.style.display = "block";
    button[0].classList.remove("turn-around");
  } else {
    my_tasks.style.display = "none";
    button[0].classList.add("turn-around");
  }
}
