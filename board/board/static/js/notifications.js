const notificationShower = document.querySelector("#notification-show"); 

const notificationSocket = new WebSocket(
    'ws://'
    + window.location.host 
    + '/ws/notifications/'
)

notificationSocket.onmessage = (e) => {
    const data = JSON.parse(e.data); 
    if (data.project_id){
        const dateOptions = {
            hour: 'numeric', 
            minute: 'numeric', 
            hour12: true, 
            day: 'numeric', 
            month: 'long', 
            year: 'numeric'
        };
        const date = new Date(data.date).toLocaleString('en', dateOptions); 
        notificationShower.innerHTML += `
            <li class="border-bottom">
                <a class="dropdown-item" href="http://${window.location.host}/projects/${data.project_id}/">
                    <p>${data.message}</p>
                    <p class="text-muted">${date}</p>
                </a>
            </li>
        `;
    } else {
        const dateOptions = {
            hour: 'numeric', 
            minute: 'numeric', 
            hour12: true, 
            day: 'numeric', 
            month: 'long', 
            year: 'numeric'
        };
        const date = new Date(data.date).toLocaleString('en', dateOptions); 
        notificationShower.innerHTML += `
            <li class="border-bottom bg-light opacity-50">
                <a class="dropdown-item" href="#">
                    <p>${data.message}</p>
                    <p class="text-muted">${date}</p>
                </a>
            </li>
        `;
    }

}

