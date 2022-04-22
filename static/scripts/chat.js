// import dateFormat from 'dateformat';

var ws;

// WebSocket
(function() {
  const sendBtn = document.querySelector('#btn');
  const chat = document.querySelector('#chat');
  
  function showMessage(json, pos = false) { 
    let item = document.createElement('div');
    if (pos == true){
      item.className = "message message-user";
    } else{
      item.className = "message";
    }
    let date = dateformat(json.date);
    item.append(`${json.message} ${date}`);
    chat.insertAdjacentElement("afterend",item);
  }
  function init() {
    if (ws) {
      ws.onerror = ws.onopen = ws.onclose = null;
      ws.close();
    }

    ws = new WebSocket('ws://127.0.0.1:6969');
    ws.onopen = () => {
      console.log('Соединение установлено!');
    }
    // Для получателя
    ws.onmessage = ({ data }) => {
      data = JSON.parse(data) // Преобразуем данные из Json
      pos = false;
      showMessage(data, pos);
    };
    ws.onclose = function() {
      ws = null;
    }
  }

  sendBtn.onclick = function() {
    if (!ws) {
      console.log("Соединение разорвано :(");
      return ;
    }
    // Отправка сообщения json через API
    const message = document.getElementById('message').value;
    const srftoken = document.getElementById("csrf_token").value
    const user_to = document.getElementById("user-to").value;
    const user_from = document.getElementById("user-from").value;
    const options = {
         method: 'POST',
         body: JSON.stringify({
            to_user: user_to,
            from_user: user_from,
            message: message
         }),
         headers: {
             "X-CSRFToken": srftoken,
             "Content-type": "application/json; charset=UTF-8"
         }
    }
    fetch('http://127.0.0.1:8000/api/message/create/',options)
    .then(response => response.json())
    .then(json => {
        right = true; // Если отправитель текущий пользователь, т.е на его стороне произошла отправка
        ws.send(JSON.stringify(json)); // Посылаем данные получателю
        showMessage(json, right); // Отображение у отправителя
        document.getElementById('message').value = "";
    }).catch(console.log("Ошибка"))
    
  }
  init();
})();

function dateformat(value){
    let date = new Date(value);
    let h = date.getHours();
    let i = date.getMinutes();
    let s = date.getSeconds();
    date = h + ":" + i + ":" + s;
    return date
}