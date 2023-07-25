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


function enableEditUser(user_id) {
  const inputs = document.querySelectorAll(`#name_${user_id}, #lastname_${user_id},
   #mail_${user_id}, #type_${user_id}, #created_${user_id}, #address_${user_id},
   #phone_${user_id}`);
  const saveButton = document.querySelector(`#save_${user_id}`);

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
}

const searchIcon = document.querySelector('.search i');
const searchForm = document.getElementById('search-form');

searchIcon.addEventListener('click', () => {
  searchForm.classList.toggle('show-search');
});

