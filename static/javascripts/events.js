document.addEventListener("DOMContentLoaded", function () {
    let textArea = document.getElementsByClassName('text-input')[0],
        langField = document.getElementsByClassName('lang-name')[0];

    textArea.addEventListener("keyup", function () {
        if (this.value !== '') {
            getLanguage(this.value);
        } else {
            langField.classList.remove('visible');
        }
    });
    function getLanguage(ofText) {
		let text = 'https://translate.yandex.net/api/v1.5/tr.json/detect?hint=ru,en&key=trnsl.1.1.20160517T143002Z.e9fc37c7a484c5f4.8cba036cc3eb084c401f3766ed5b2b389b6dc9fc&text=' + ofText;
		if (self.fetch) {
			fetch(text, {
				method: 'post'
			})
				.then(function (response) {
					return response.json().then(function (result) {
						langField.innerHTML = result.lang;
						langField.classList.add('visible');
					})
				})
				.catch(function (error) {
					alert('Виникла помилка на стороні серевера.' + '\n' + 'Помилка: ' + error + '\n' + ' Cпробуйте ще раз.');
				});
		} else {
			alert('Ваш браузер застарів. Встановіть актуальну версію Google Chrome');
		}
	}
});