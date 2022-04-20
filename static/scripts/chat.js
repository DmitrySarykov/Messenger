const chat = document.querySelector(".chat");
const btnopen = document.getElementById("socket-open");
const btnclose = document.getElementById("socket-close");
var websocket
// WebSocket
btnopen.addEventListener('click', (e)=>{
    websocket = new WebSocket("ws://127.0.0.1:8010");
    websocket.onopen = function(e){
        console.log("Соединение установлено");
    }
    websocket.onoclose = function(e){
        console.log("Соединение закрыто");
    }
    websocket.onmessage = function(e){
        console.log("Отправка сообщения", e.message);
    }
    websocket.onerror = function(e){
        console.log("Ошибка соединения");
    }
});
btnclose.addEventListener('click', (e)=>{
    websocket.close();
    websocket = null;
});

// Отправка сообщения
btn.addEventListener('submit', (e)=>{
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
// Вывод на экран
function screenChat(json){
    let item = document.createElement('p');
    let date = dateformat(json.date);
    websocket.send(`${date} ${json.from_user}: ${json.message}`)
    item.append(`${date} ${json.from_user}: ${json.message}`);
    chat.insertAdjacentElement("afterend",item);
}

function dateformat(value){
    let date = new Date(value);
    let d = date.getDate();
    let m = date.getMonth()+1
    let y = date.getFullYear();
    let h = date.getHours();
    let i = date.getMinutes();
    let s = date.getSeconds();
    date = d + "." + m + "." + y + " " + h + ":" + i + ":" + s;
    return date
}