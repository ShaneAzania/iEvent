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
