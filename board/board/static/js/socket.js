const roomName = JSON.parse(document.getElementById("project-id").textContent); 
const requestUser = JSON.parse(document.getElementById("request-user").textContent)

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data); 
    const chat = document.querySelector("#chat-log"); 

    const dateOptions = {hour: 'numeric', minute: 'numeric', hour12: true}
    const date = new Date(data.date).toLocaleString('en', dateOptions); 
    const isMe = data.user == requestUser; 
    const source = isMe ? "me" : "other"; 
    const name = isMe? "Me": data.user; 

    chat.innerHTML += '<div class="message ' + source + '">' + '<strong>' + name + '</strong> ' +
                  '<span class="date">' + date + '</span><br>' +
                  data.message + '</div>';

    chat.scrollTop = chat.scrollHeight; 
}; 

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};