var ws;
// WebSocket
(function() {
  const sendBtn = document.querySelector('#btn');
  const chat = document.querySelector('#chat');

  function showMessage(data) {
    let item = document.createElement('p');
    item.append(data);
    chat.insertAdjacentElement("afterend",item);
  }
  function init() {
    if (ws) {
      ws.onerror = ws.onopen = ws.onclose = null;
      ws.close();
    }

    ws = new WebSocket('ws://localhost:6969');
    ws.onopen = () => {
      console.log('Соединение установлено!');
    }
    ws.onmessage = ({ data }) => {
      showMessage(data);
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
    const user_to = document.getElementById("user_to").value;
    const user_from = document.getElementById("user_from").value;
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
    fetch('http://127.0.0.1:8000/api/message_create/',options)
    .then(response => response.json())
    .then(json => {
        ws.send(`${json.date} ${user_from}: ${message}`);
        showMessage(`${json.date} ${user_from}: ${message}`);
    })
    
  }
  init();
})();

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