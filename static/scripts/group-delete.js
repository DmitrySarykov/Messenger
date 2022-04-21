delete_group.addEventListener("click", (e)=>{
    const srftoken = document.getElementById("csrf_token").value;
    const group_pk = document.getElementById("group").value;
    let url = `http://127.0.0.1:8000/api/group/delete/${group_pk}`
    const options = {
         method: 'DELETE',
         body: JSON.stringify({
            id: group_pk,
         }),
         headers: {
             "X-CSRFToken": srftoken,
             "Content-type": "application/json; charset=UTF-8"
         }
    }
    fetch(url,options)
    .then(response => response.json())
    .then(json => console.log(json)).then(groupRedirect())
});

function groupRedirect(){
    window.location.replace('http://127.0.0.1:8000/messages/');
}