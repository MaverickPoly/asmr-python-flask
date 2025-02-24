const field = document.querySelector(".field");

function addChar(char) {
	field.value += char;
}
function clearField() {
	field.value = "";
}

function deleteField() {
	field.value = field.value.substring(0, field.value.length - 1);
}

function percent() {
	calculateField();
	field.value = parseFloat(field.value) / 100;
}

function calculateField() {
	try {
		const result = eval(field.value);
		field.value = result;
	} catch (e) {
		field.value = `Error: ${e.message}`;
	}
}
