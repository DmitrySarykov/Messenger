const delete_group = document.querySelectorAll(".delete_group");
delete_group.forEach(element => {
    element.addEventListener("click", deleteGroup);
});

function deleteGroup(e){
    const srftoken = document.getElementById("csrf_token").value;
    const group_pk = e.target.previousElementSibling.value;
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
    clearGroupInList(group_pk)
}
function clearGroupInList(group){
    let item= document.getElementById(`group-${group}`);
    message_list.removeChild(item);
}