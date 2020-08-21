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
