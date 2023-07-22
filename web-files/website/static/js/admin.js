window.onload = function(){
    const sidebar = document.querySelector(".sidebar");
    const closeBtn = document.querySelector("#btn");
    const searchBtn = document.querySelector(".bx-search")

    closeBtn.addEventListener("click",function(){
        sidebar.classList.toggle("open")
        menuBtnChange()
    })

    searchBtn.addEventListener("click",function(){
        sidebar.classList.toggle("open")
        menuBtnChange()
    })

    function menuBtnChange(){
        if(sidebar.classList.contains("open")){
            closeBtn.classList.replace("bx-menu","bx-menu-alt-right")
        }else{
            closeBtn.classList.replace("bx-menu-alt-right","bx-menu")
        }
    }
}


//owner actions


function enableEditOwner(owner_id) {
  const inputs = document.querySelectorAll(`#name_${owner_id}, #created_${owner_id}, #address_${owner_id}, #phone_${owner_id}`);
  const saveButton = document.querySelector(`#save_${owner_id}`);

  let isEditable = false;

  for (const input of inputs) {
    if (input.disabled) {
      input.disabled = false;
      isEditable = true;
    } else {
      input.disabled = true;
    }
  }

  if (saveButton) {
    if (isEditable) {
      saveButton.style = 'display: inline-block';
    } else {
      saveButton.style = 'display: none';
    }
  }

  // Prevent form submission when the "Save" button is clicked
  return false;
}



