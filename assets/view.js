function getQueryString(name) {
	var query_string = window.location.search;
	if (!query_string) return '';
	var re = /[?&]?([^=]+)=([^&]*)/g;
	var tokens;
	while (tokens = re.exec(query_string))
		if (decodeURIComponent(tokens[1]) === name)
			return decodeURIComponent(tokens[2]);
	return '';
}
async function load(){
	await loadData();
	loadLastUpdate();
	var search_text = getQueryString("search");
	var grade_option = getQueryString("grade");
	var category_option = getQueryString("category");
	category_option = (category_option == '' ? 'a' : category_option);
	var search_all = category_option == 'a';
	var re = new RegExp(search_text);
	var matched_count = 0;
	var table = document.getElementById("query-table");
	var html = table.innerHTML;
	const categories = {
		'i': 'id',
		'n': 'name',
		'p': 'pinyin',
		'b': 'birthday',
		'h': 'homeroom',
		'c': 'card_id'
	}
	grade_option = (grade_option == '' ? 'a' : grade_option);
	if (search_text == '')
		document.title = 'KCIS Stud. List - Friendly View';
	else
		document.title = `KCIS Stud. List - ${search_text} - Friendly View`;
	console.log("Search: " + search_text);
	for (let i in studs){
		var stud = studs[i];
		if (stud.grade == grade_option || grade_option == 'a'){
			var flag = false;
				for (let search_for in categories){
					var condition = categories[search_for];
					var test = re.test(stud[condition]);
					if (test){
						if (search_all){
							flag = true;
							break;
						}
						else {
							if (category_option == search_for){
								flag = true;
								break;
							}
						}
					}
				}
			if (flag){
				html += info_to_li(stud);
				matched_count++;
			}
		}
	}
	table.innerHTML = html;
	document.getElementById('data-count').innerText = matched_count;
	document.getElementById('data-tip').innerText = matched_count == 1 ? 'um' : 'a';
	console.log('Matched Data count: ' + matched_count);
	loadForm(grade_option, category_option, search_text);
}
function loadForm(arg_grade, arg_category, arg_search){
	grade.value = arg_grade;
	category.value = arg_category;
	search.value = arg_search;
}
function submit_search(){
	var search_arg = encodeURIComponent(search.value);
	var category_arg = encodeURIComponent(category.value);
	var grade_arg = encodeURIComponent(grade.value);
	var arg = `?grade=${grade_arg}&category=${category_arg}&search=${search_arg}`;
	window.location.href = window.location.pathname + arg;
	return false;
}
window.onload = load;