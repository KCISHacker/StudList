function randomIntFromInterval(min, max) { // min and max included 
  return Math.floor(Math.random() * (max - min + 1) + min);
}

async function load(){
	await loadData();
	loadLastUpdate();
	var table = document.getElementById("query-table");
	var stud = studs[randomIntFromInterval(0, count-1)];
	console.log("Selected Studs:");
	console.log(stud);
	table.innerHTML += info_to_li(stud);
}
window.onload = load;