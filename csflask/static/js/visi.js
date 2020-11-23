// const togglePassword = document.querySelector('#togglePassword');
// const password = document.querySelector('#password');

// togglePassword.addEventListener('click', function (e) {

// 	const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
// 	password.setAttribute('type', type);

// 	this.classList.toggle('fa-eye-slash');

// });


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
