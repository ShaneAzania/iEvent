// search feature front end changes when 'date' filter is selected
if (document.querySelector("#filter")) {
	const formFilter = document.querySelector("#filter"),
		formFilterOptions = document.querySelector("#filter").children,
		searchField = document.querySelector("#search");
	formFilter.addEventListener("click", (e) => {
		// check if filter from form = 'date'
		if (e.target.value == "time") {
			searchField.setAttribute("type", "date");
		} else {
			searchField.setAttribute("type", "search");
		}
	});
	searchField.addEventListener("click", (e) => {
		// check if filter from form = 'date'
		for (let index = 0; index < formFilterOptions.length; index++) {
			var option = formFilterOptions[index];
			if (option.selected == true && option.value == "time") {
				e.target.type = "date";
			} else if (option.selected == true && option.value != "time") {
				e.target.type = "search";
			}
		}
	});
}

if (document.querySelector("#back_btn")) {
	// Go back to last page
	const back_btn = document.querySelector("#back_btn");
	back_btn.addEventListener("click", (e) => {
		history.back();
		console.log("function reached");
	});
}
