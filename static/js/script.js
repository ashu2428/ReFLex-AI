// to set time for flashed messages in 'layout.html'
var flash_div = document.getElementById("flash_div");
if (flash_div) {
	setTimeout(function () {
		flash_div.style.display = "none";
	}, 10000); // Hide the div after 10 seconds
}

// for 'text_editor.html'
function toggleFormatting(command, value = null) {
	document.execCommand(command, false, value);
	var button = document.getElementById(command + 'Btn');
	button.classList.toggle('active-button', document.queryCommandState(command));
}
function addLink() {
	const url = prompt('Insert url: ');
	toggleFormatting('createLink', url);
}
function save_diary() {
	// Get the content of the diary-content div
	var diaryContent = document.getElementById('diary-content').innerHTML;
	// Set the content as the value of the hidden input field
	document.getElementById('hidden-diary-content').value = diaryContent;
}

// start and end dates for 'plot.html'
const startDateInput = document.getElementById('start_date');
const endDateInput = document.getElementById('end_date');

const today = new Date();
const todayLocalISO = today.toISOString().split('T')[0];
startDateInput.max = todayLocalISO;

startDateInput.addEventListener('change', function () {
    const selectedStartDate = new Date(this.value);
    // Enable end date input and set the minimum and maximum values
    endDateInput.disabled = false;
    endDateInput.min = this.value;
    endDateInput.max = todayLocalISO;
});

// for filter dropdowns in 'index.html'
function toggleFilterOptions() {
	var filterType = document.getElementById("filterType").value;
	var tagFilter = document.getElementById("tagFilter");
	var emotionFilter = document.getElementById("emotionFilter");

	if (filterType === "tag") {
		tagFilter.style.display = "block";
		emotionFilter.style.display = "none";
	} else if (filterType === "emotion") {
		tagFilter.style.display = "none";
		emotionFilter.style.display = "block";
	} else {
		tagFilter.style.display = "none";
		emotionFilter.style.display = "none";
	}
}

function submitForm() {
	document.getElementById("filterForm").submit();
}

// // JavaScript to limit the number of checked checkboxes
// const form = document.getElementById('profileForm');
// const checkboxes = form.getElementsByClassName('interest-checkbox');

// form.addEventListener('submit', function (event) {
// 	const checkedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
// 	if (checkedCheckboxes.length > 5) {
// 		alert('Please select a maximum of 5 interests.');
// 		event.preventDefault();
// 	}
// });