allterms_native = {
    "termsintext": {
        "filepath": "/home/recapService/consoles/console_1543823713324/fileForAnalysisDocXCP1251.txt",
        "exporterms": {
            "term": [
                {
                    "ttype": "Noun",
                    "tname": "sdaf",
                    "wcount": "1",
                    "osn": "dsfa",
                    "sentpos": [
                        "0/1",
                        "2/1",
                        "3/1",
                        "5/1",
                        "8/6",
                        "11/13",
                        "12/9",
                        "13/2",
                        "13/51",
                        "14/12",
                        "15/1",
                        "16/13",
                        "17/1",
                        "18/3",
                        "19/1"
                    ]
                }
            ]
        },
        "sentences": {
            "sent": [
                "sdmfasdf sadfasd asdfasdfasdf",
                "sdfa dsfasdf sdf frefg 454  d sf a dfa sdfas"
            ]
        }
    }
}
print(allterms_native['termsintext']['filepath'])
print(allterms_native['termsintext']['exporterms']['term'][0]['tname'])
print(allterms_native)

allterms_new = {
    "termsintext": {
        "exporterms": {
            "term": []
        },
        "sentences": {
            "sent": []
        }
    }
}

term = {
    "ttype": "",
    "tname": "",
    "wcount": "",
    "osn": "",
    "sentpos": [],
    "relup":[],
    "reldown":[]
}

allterms_new['termsintext']['exporterms']['term'].append('1')
allterms_new['termsintext']['exporterms']['term'].append('2')
allterms_new['termsintext']['exporterms']['term'].append('3')

exporterms = allterms_new['termsintext']['exporterms']['term']
exporterms.append('4')
print(exporterms)
print(allterms_new)

term_name = {}
term_properties_1 = {}
term_properties_2 = {}
term_properties_1['prop_1'] = '1'
term_properties_1['prop_2'] = '2'
term_properties_2['prop_1'] = '12'
term_properties_2['prop_2'] = '22'
term_name['name_1'] = term_properties_1
term_name['name_2'] = term_properties_2

if 'name_1' in term_name:
    print(term_name['name_2'])

