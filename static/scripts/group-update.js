edit_group.addEventListener("click", ()=>{
    let form_edit = document.querySelector(".group-edit-form");
    if (form_edit.style.display == "none"){
        form_edit.style.display = "block";
    } else{
        form_edit.style.display = "none";
    }
});

group_update.addEventListener("click", (e)=>{
    const srftoken = document.getElementById("csrf_token").value
    const groupname = document.getElementById("group-name").value;
    const group = document.getElementById("group").value;
    let url = `http://127.0.0.1:8000/api/group/update/${group}`
    const options = {
         method: 'PATCH',
         body: JSON.stringify({
            name: groupname,
         }),
         headers: {
             "X-CSRFToken": srftoken,
             "Content-type": "application/json; charset=UTF-8"
         }
    }
    fetch(url,options)
    .then(response => response.json())
    .then(json => changeGroup(json))
    document.querySelector(".group-edit-form").style.display = "none";
});

function changeGroup(json){
    let group = document.getElementById("group-now");
    group.innerHTML = json.name;
}


