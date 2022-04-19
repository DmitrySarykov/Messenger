const chat = document.querySelector(".chat")
console.log()
btn.addEventListener('click', (e)=>{
    const srftoken = document.getElementById("csrf_token").value
    const user_to = document.getElementById("user_to").value;
    const user_from = document.getElementById("user_from").value;
    const text = document.getElementById("message").value;
    e.preventDefault();
    const options = {
        method: 'POST',
        body: JSON.stringify({
            to_user: user_to,
            from_user: user_from,
            message: text
        }),
        headers: {
            "X-CSRFToken": srftoken,
            "Content-type": "application/json; charset=UTF-8"
        }
    }
    fetch('http://127.0.0.1:8000/api/message_create/',options).then(response => response.json()).then(json => screenChat(json))
    document.getElementById("form_chat").reset()
});
function screenChat(json){
    let item = document.createElement('p');
    let date = new Date(json.date);
    let d = date.getDate()
    let m = date.getMonth()+1
    let y = date.getFullYear()
    let h = date.getHours()
    let i = date.getMinutes()
    let s = date.getSeconds()
    date = d + "." + m + "." + y + " " + h + ":" + i + ":" + s
    item.append(`${date} ${json.from_user}: ${json.message}`);
    chat.insertAdjacentElement("afterend",item);
}