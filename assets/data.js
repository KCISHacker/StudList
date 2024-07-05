// Fetch Json
var studs, count, last_update;
async function loadData(){
    await fetch("./data.json")
    .then((response) => response.json())
    .then((data) => {
        studs = data.data;
        count = data.count;
        last_update = new Date(data.last_update);
    })
    .catch((error) => {
        studs = undefined;
        count = undefined;
        last_update = undefined;
        alert('Cannot access data file: data.json. Error ' + error.message);
    })
}

// Load Last Update labels
function loadLastUpdate(){
    var last_update_str = last_update.toDateString().substring(4);
    var last_update_label = document.getElementsByClassName('last-update-label');
    for (let i in last_update_label)
        last_update_label[i].innerHTML = "Last Update: " + last_update_str;
}