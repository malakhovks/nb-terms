/* document.addEventListener("DOMContentLoaded", function () {
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
}); */

var $textArea1 = $('#text-area-1'),
    $textArea2 = $("#text-area-2"),
    $buttonFindSimilarity = $("#button-find-similarity"),
    $labelCosineSimilarity = $("#label-cosine-similarity");

$(document).ready(function () {
    $textArea1.val("Company representative, manned underwater operations, HSE advisor; Research: chaired research into noise in diving for NOROG; Human factors/ergonomics (incl: control room design, noise, light, DSE, manual handling, etc.) Conference paper referee for Ergonomics Society HSEQ management; Life support supervision, saturation diving; Offshore occupational health & safety; General and offshore nursing; Lecturer, producer of training material, written and film; Expert witness in court; Technical author and proof-reader.");
    $textArea2.val("Geophysicist with 28 years of experience within seismic interpretation, depth conversion, well planning including use of 3D visualization tools, seismic 4D monitoring. Application support: Petrel, GeoFrameCharisma, Irap, RMS, SviPro.");
});
$buttonFindSimilarity.click(function () {
    findSimilarity();
});

function findSimilarity() {
    if (self.fetch) {
        fetch('/wv/api/en/similarity', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text1: $textArea1.val(), text2: $textArea2.val() })
        }).then(res => res.json())
            .then(response => { console.log('Success:', JSON.stringify(response)); $labelCosineSimilarity.text(response.similarity) })
            .catch(error => console.error('Error:', error));
    } else {
        alert('Error: Fetch API not supported');
    }
}