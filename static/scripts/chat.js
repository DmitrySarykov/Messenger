// import dateFormat from 'dateformat';

var ws;

// WebSocket
(function() {
  const sendBtn = document.querySelector('#btn');
  const chat = document.querySelector('#chat');

  function showMessage(json) {
    var username = fetch(`http://127.0.0.1:8000/api/user/${json.from_user}`).then(response => response.json())
    console.log(username.json) 
    let item = document.createElement('div');
    let date = dateformat(json.date);
    item.className = "message";
    item.append(`${date} ${json.from_user}: ${json.message}`);
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
        ws.send(json);
        showMessage(json);
        document.getElementById('message').value = "";
    })
    
  }
  init();
})();

function dateformat(value){
    let date = new Date(value);
    let h = date.getHours();
    let i = date.getMinutes();
    date = h + ":" + i;
    return date
}