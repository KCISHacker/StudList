async function load(){
    await loadData();
    loadLastUpdate();
    document.getElementById('data-count').innerText = count
}
window.onload = load;