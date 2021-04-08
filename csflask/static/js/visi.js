function togglepass() {
	var pass = document.getElementById('password');

	if (pass.type == 'text')
		pass.type = 'password';
	else
		pass.type = 'text'

}

function ttogglepass() {
	var pass = document.getElementById('confirm_password');

	if (pass.type == 'text')
		pass.type = 'password';
	else
		pass.type = 'text'

}

function stogglepass() {
	var pass = document.getElementById('sitepassword');

	if (pass.type == 'text')
		pass.type = 'password';
	else
		pass.type = 'text'

}

// function forceLower(strInput) 
// {
// strInput.value=strInput.value.toLowerCase();
// }​
