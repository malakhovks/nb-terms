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
    $inputDocxFile = $('#input-docx-file'),
    $inputDocxFiles = $("#input-docx-files"),
    $buttonFindSimilarity = $("#button-find-similarity"),
    $buttonExtractCvData = $("#button-extract-cv-data"),
    $buttonExtractCvsData = $("#button-extract-cvs-data"),
    $labelCosineSimilarity = $("#label-cosine-similarity");

$(document).ready(function () {
    $textArea1.val("Company representative, manned underwater operations, HSE advisor; Research: chaired research into noise in diving for NOROG; Human factors/ergonomics (incl: control room design, noise, light, DSE, manual handling, etc.) Conference paper referee for Ergonomics Society HSEQ management; Life support supervision, saturation diving; Offshore occupational health & safety; General and offshore nursing; Lecturer, producer of training material, written and film; Expert witness in court; Technical author and proof-reader.");
    $textArea2.val("Geophysicist with 28 years of experience within seismic interpretation, depth conversion, well planning including use of 3D visualization tools, seismic 4D monitoring. Application support: Petrel, GeoFrameCharisma, Irap, RMS, SviPro.");
});

$buttonFindSimilarity.click(function () {
    findSimilarity();
});

$buttonExtractCvData.click(function (){
    extractCvData();
});

$buttonExtractCvsData.click(function (){
    extractCvsData();
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

function extractCvData() {
    const docxExtension = '.docx';
    var form = new FormData();

    var uploadFileName = $inputDocxFile.val().split('\\').pop()

    form.append("file", $inputDocxFile[0].files[0]);

    if (uploadFileName.indexOf(docxExtension) != -1) {
        if (self.fetch) {
            fetch('/api/cv/ridge/docx/extract/xml', {
                method: 'post',
                body: form
            })
            .then(response => {
                if (response.status == 503) {
                    alert('Сервіс зайнятий, спробуйте ще раз.');
                    return;
                }
                return response.text().then(result => {
                    document.getElementById('text-area-3').value = formatXml(result)
                    // document.getElementById('text-area-3').value = JSON.stringify(result, undefined, 4)
                    // console.log(JSON.stringify(result));
                })
            })
        } else {
            alert("Ваш браузер застарів, встановіть актуальну версію Google Chrome!");
        }
    }
}

function formatXml(xml) {
    var formatted = '';
    var reg = /(>)(<)(\/*)/g;
    xml = xml.replace(reg, '$1\r\n$2$3');
    var pad = 0;
    jQuery.each(xml.split('\r\n'), function(index, node) {
        var indent = 0;
        if (node.match( /.+<\/\w[^>]*>$/ )) {
            indent = 0;
        } else if (node.match( /^<\/\w/ )) {
            if (pad != 0) {
                pad -= 1;
            }
        } else if (node.match( /^<\w([^>]*[^\/])?>.*$/ )) {
            indent = 1;
        } else {
            indent = 0;
        }

        var padding = '';
        for (var i = 0; i < pad; i++) {
            padding += '  ';
        }

        formatted += padding + node + '\r\n';
        pad += indent;
    });

    return formatted;
}

function extractCvsData() {
    const docxExtension = '.docx';
    var form = new FormData();

    // const fileList = $inputDocxFiles.files;
    // const fileList = $inputDocxFiles[0].files

    for (const file of $inputDocxFiles[0].files) {
        form.append('file', file, file.name)
    }


    // form.append("file", $inputDocxFile[0].files[0]);


    if (self.fetch) {
        fetch('/api/cv/multiple/ridge/docx/extract/xml', {
            method: 'post',
            body: form
        })
            .then(response => {
                if (response.status == 503) {
                    alert('Сервіс зайнятий, спробуйте ще раз.');
                    return;
                }
                return response.text().then(result => {
                    document.getElementById('text-area-3').value = formatXml(result)
                    downloadLink = document.createElement("a");
                    // Make sure that the link is not displayed
                    downloadLink.style.display = "none";
                    // Add the link to your DOM
                    document.body.appendChild(downloadLink);
                    // let blob = new Blob([projectStructure], { type: "octet/stream" }),
                    let blob = new Blob([formatXml(result)], { type: "application/xml" }),
                        url = window.URL.createObjectURL(blob);
                    downloadLink.href = url;
                    downloadLink.download = 'cv.xml';
                    downloadLink.click();
                })
            })
    } else {
        alert("Ваш браузер застарів, встановіть актуальну версію Google Chrome!");
    }

}