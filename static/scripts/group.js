var ws;
// WebSocket
(function() {
  const sendBtn = document.querySelector('#btn');
  const chat = document.querySelector('#chat');

  function showMessage(data) {
    let item = document.createElement('div');
    item.className = "message";
    item.append(data);
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
    const group = document.getElementById("group").value;
    const user_from = document.getElementById("user-from").value;
    const options = {
         method: 'POST',
         body: JSON.stringify({
            from_user: user_from,
            group: group,
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
        ws.send(`${json.date} ${user_from}: ${message}`);
        showMessage(`${json.date} ${user_from}: ${message}`);
        document.getElementById('message').value = "";
    }).catch(console.log("Ошибка"))
    
  }
  init();
})();

function dateformat(value){
    let date = new Date(value);
    let d = date.getDate();
    let m = date.getMonth()+1
    if (m < 9){
      m = "0" + m
    }
    let y = date.getFullYear();
    let h = date.getHours();
    let i = date.getMinutes();
    let s = date.getSeconds();
    date = d + "." + m + "." + y + " " + h + ":" + i + ":" + s;
    return date
}