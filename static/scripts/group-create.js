group_create.addEventListener("click", (e)=>{
    const srftoken = document.getElementById("csrf_token").value;
    const group_name = document.getElementById("group-name").value;
    const group_admin = document.getElementById("group-admin").value;
    const users = document.querySelectorAll(".users_input");
    const group_users = []
    var j = 0; 
    for (let i = 0; i < users.length; i++) {
        if (users[i].checked == true){
            group_users[j] = users[i].value;
            j++;
        }
    } 
    const options = {
         method: 'POST',
         body: JSON.stringify({
            admin: group_admin,
            name: group_name,
            users: group_users,
         }),
         headers: {
             "X-CSRFToken": srftoken,
             "Content-type": "application/json; charset=UTF-8"
         }
    }
    fetch("http://127.0.0.1:8000/api/group/create/",options)
    .then(response => response.json())
    .then(json => console.log(json)).then(groupRedirect());
    let form = document.getElementById("group-create-form");
    form.reset();
});

function groupRedirect(){
    window.location.replace('http://127.0.0.1:8000/messages/');
}


