user_update.addEventListener("click", (e)=>{
    const srftoken = document.getElementById("csrf_token").value;
    const username = document.getElementById("user-name").value;
    const user = document.getElementById("user").value;
    let url = `http://127.0.0.1:8000/api/user/update/${user}`
    const options = {
         method: 'PATCH',
         body: JSON.stringify({
            username: username,
         }),
         headers: {
             "X-CSRFToken": srftoken,
             "Content-type": "application/json; charset=UTF-8"
         }
    }
    fetch(url,options)
    .then(response => response.json())
    .then(json => changeUser(json))
});

function changeUser(json){
    let user = document.getElementById("user-now");
    user.innerHTML = json.username;
}