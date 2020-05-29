# nb-terms API

### API endpoints

|        |                   Service                    | API endpoint                                                 | HTTP method |
| :----: | :------------------------------------------: | :----------------------------------------------------------- | :---------: |
| **E1** | Get **allterms** for **message** in **JSON** | `host[:port]/api/bot/nb/message/json/allterms`<br>`http://194.44.28.250:45102/api/bot/nb/message/json/allterms` |    POST     |
| **E2** |   Get **parce** for **message** in **XML**   | `host[:port]/api/bot/nb/message/xml/parce`<br/>`http://194.44.28.250:45102/api/bot/nb/message/xml/parce` |    POST     |
| **E3** |  Get **parce** for **document** in **XML**   | `host[:port]/api/bot/nb/document/xml/parce`<br/>`http://194.44.28.250:45102/api/bot/nb/document/xml/parce` |    POST <br> multipart/form-data   |

##### E1 - Input data

```JSON
{
	"message": "I de fleste tilfeller får du beskjeden når du forsøker å handle et verdipapir som ikke er skattemessig hjemmehørende innenfor EØS, til tross for at det muligens handles på Oslo Børs. Eksempelvis er en god del oljeselskap på Oslo Børs skattemessig hjemmehørende utenfor EØS hvilket gjør at selskapet dermed faller utenfor investeringsuniverset på Aksjesparekonto. Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar. San Francisco vurderer å forby robotbud på fortauene. Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar. For å flytte aksjer fra en annen bank eller megler til Nordnet, må du sende oss signert overføringsfullmakt. Eksempelvis er en god del oljeselskap på Oslo Børs skattemessig hjemmehørende utenfor EØS hvilket gjør at selskapet dermed faller utenfor investeringsuniverset på Aksjesparekonto. Om du ikke har anledning til å signere med BankID, kan følgende overføringsfullmakt sendes via meldingstjenesten når du er logget inn eller i posten."
}
```
##### E1 - Output data

```JSON
{
  "termsintext": {
    "exporterms": {
      "term": {
        "fler tilfelle": {
          "wcount": "2",
          "ttype": "ADJ_NOUN",
          "tname": "fler tilfelle",
          "osn": [
            "flest",
            "tilfell"
          ],
          "sentpos": [
            "0/3"
          ],
          "relup": [
            2
          ]
        },
        "tilfelle": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "tilfelle",
          "osn": "tilfell",
          "sentpos": [
            "0/4"
          ],
          "reldown": [
            1
          ]
        },
        "verdipapir": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "verdipapir",
          "osn": "verdipapir",
          "sentpos": [
            "0/14"
          ]
        },
        "skattemessig hjemmehørende": {
          "wcount": "2",
          "ttype": "ADJ_ADJ",
          "tname": "skattemessig hjemmehørende",
          "osn": [
            "skattemess",
            "hjemmehør"
          ],
          "sentpos": [
            "0/18",
            "1/10",
            "6/10"
          ]
        },
        "hjemmehørende innenfor EØS": {
          "wcount": "3",
          "ttype": "ADJ_ADP_PROPN",
          "tname": "hjemmehørende innenfor EØS",
          "osn": [
            "hjemmehør",
            "innenfor",
            "eøs"
          ],
          "sentpos": [
            "0/19"
          ]
        },
        "EØS": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "EØS",
          "osn": "eøs",
          "sentpos": [
            "0/21",
            "1/13",
            "6/13"
          ]
        },
        "Oslo": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "Oslo",
          "osn": "oslo",
          "sentpos": [
            "0/31",
            "1/8",
            "6/8"
          ],
          "reldown": [
            8
          ]
        },
        "Oslo Børs": {
          "wcount": "2",
          "ttype": "PROPN_PROPN",
          "tname": "Oslo Børs",
          "osn": [
            "oslo",
            "bør"
          ],
          "sentpos": [
            "0/31",
            "1/8",
            "6/8"
          ],
          "relup": [
            7
          ]
        },
        "Børs": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "Børs",
          "osn": "bør",
          "sentpos": [
            "0/32",
            "1/9",
            "6/9"
          ],
          "reldown": [
            8
          ]
        },
        "god del": {
          "wcount": "2",
          "ttype": "ADJ_NOUN",
          "tname": "god del",
          "osn": [
            "god",
            "del"
          ],
          "sentpos": [
            "1/4",
            "6/4"
          ],
          "relup": [
            11
          ]
        },
        "del": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "del",
          "osn": "del",
          "sentpos": [
            "1/5",
            "6/5"
          ],
          "reldown": [
            10,
            13
          ]
        },
        "god del oljeselskap": {
          "wcount": "3",
          "ttype": "ADJ_NOUN_NOUN",
          "tname": "god del oljeselskap",
          "osn": [
            "god",
            "del",
            "oljeselskap"
          ],
          "sentpos": [
            "1/4",
            "6/4"
          ]
        },
        "del oljeselskap": {
          "wcount": "2",
          "ttype": "NOUN_NOUN",
          "tname": "del oljeselskap",
          "osn": [
            "del",
            "oljeselskap"
          ],
          "sentpos": [
            "1/5",
            "6/5"
          ],
          "relup": [
            14
          ]
        },
        "oljeselskap": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "oljeselskap",
          "osn": "oljeselskap",
          "sentpos": [
            "1/6",
            "6/6"
          ],
          "reldown": [
            13
          ]
        },
        "oljeselskap på Oslo": {
          "wcount": "3",
          "ttype": "NOUN_ADP_PROPN",
          "tname": "oljeselskap på Oslo",
          "osn": [
            "oljeselskap",
            "på",
            "oslo"
          ],
          "sentpos": [
            "1/6",
            "6/6"
          ]
        },
        "Oslo Børs skattemessig": {
          "wcount": "3",
          "ttype": "PROPN_PROPN_ADJ",
          "tname": "Oslo Børs skattemessig",
          "osn": [
            "oslo",
            "bør",
            "skattemess"
          ],
          "sentpos": [
            "1/8",
            "6/8"
          ]
        },
        "Børs skattemessig": {
          "wcount": "2",
          "ttype": "PROPN_ADJ",
          "tname": "Børs skattemessig",
          "osn": [
            "bør",
            "skattemess"
          ],
          "sentpos": [
            "1/9",
            "6/9"
          ]
        },
        "Børs skattemessig hjemmehørende": {
          "wcount": "3",
          "ttype": "PROPN_ADJ_ADJ",
          "tname": "Børs skattemessig hjemmehørende",
          "osn": [
            "bør",
            "skattemess",
            "hjemmehør"
          ],
          "sentpos": [
            "1/9",
            "6/9"
          ]
        },
        "hjemmehørende utenfor EØS": {
          "wcount": "3",
          "ttype": "ADJ_ADP_PROPN",
          "tname": "hjemmehørende utenfor EØS",
          "osn": [
            "hjemmehør",
            "utenfor",
            "eøs"
          ],
          "sentpos": [
            "1/11",
            "6/11"
          ]
        },
        "selskap": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "selskap",
          "osn": "selskap",
          "sentpos": [
            "1/17",
            "6/17"
          ]
        },
        "investeringsunivers": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "investeringsunivers",
          "osn": "investeringsunivers",
          "sentpos": [
            "1/21",
            "6/21"
          ]
        },
        "investeringsunivers på Aksjesparekonto": {
          "wcount": "3",
          "ttype": "NOUN_ADP_PROPN",
          "tname": "investeringsunivers på Aksjesparekonto",
          "osn": [
            "investeringsunivers",
            "på",
            "aksjesparekonto"
          ],
          "sentpos": [
            "1/21",
            "6/21"
          ]
        },
        "Aksjesparekonto": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "Aksjesparekonto",
          "osn": "aksjesparekonto",
          "sentpos": [
            "1/23",
            "6/23"
          ]
        },
        "Apple": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "Apple",
          "osn": "appl",
          "sentpos": [
            "2/1",
            "4/1"
          ]
        },
        "britisk oppstartfirme": {
          "wcount": "2",
          "ttype": "ADJ_NOUN",
          "tname": "britisk oppstartfirme",
          "osn": [
            "britisk",
            "oppstartfirm"
          ],
          "sentpos": [
            "2/5",
            "4/5"
          ],
          "relup": [
            26
          ]
        },
        "oppstartfirme": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "oppstartfirme",
          "osn": "oppstartfirm",
          "sentpos": [
            "2/6",
            "4/6"
          ],
          "reldown": [
            25
          ]
        },
        "milliard": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "milliard",
          "osn": "milliard",
          "sentpos": [
            "2/9",
            "4/9"
          ],
          "reldown": [
            28
          ]
        },
        "milliard dollar": {
          "wcount": "2",
          "ttype": "NOUN_NOUN",
          "tname": "milliard dollar",
          "osn": [
            "milliard",
            "doll"
          ],
          "sentpos": [
            "2/9",
            "4/9"
          ],
          "relup": [
            29
          ]
        },
        "dollar": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "dollar",
          "osn": "doll",
          "sentpos": [
            "2/10",
            "4/10"
          ],
          "reldown": [
            28
          ]
        },
        "San": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "San",
          "osn": "san",
          "sentpos": [
            "3/1"
          ],
          "reldown": [
            31
          ]
        },
        "San Francisco": {
          "wcount": "2",
          "ttype": "PROPN_PROPN",
          "tname": "San Francisco",
          "osn": [
            "san",
            "francisco"
          ],
          "sentpos": [
            "3/1"
          ],
          "relup": [
            30
          ]
        },
        "Francisco": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "Francisco",
          "osn": "francisco",
          "sentpos": [
            "3/2"
          ],
          "reldown": [
            31
          ]
        },
        "robotbud": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "robotbud",
          "osn": "robotbud",
          "sentpos": [
            "3/6"
          ]
        },
        "robotbud på fortau": {
          "wcount": "3",
          "ttype": "NOUN_ADP_NOUN",
          "tname": "robotbud på fortau",
          "osn": [
            "robotbud",
            "på",
            "fortau"
          ],
          "sentpos": [
            "3/6"
          ]
        },
        "fortau": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "fortau",
          "osn": "fortau",
          "sentpos": [
            "3/8"
          ]
        },
        "aksje": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "aksje",
          "osn": "aksj",
          "sentpos": [
            "5/4"
          ]
        },
        "bank": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "bank",
          "osn": "bank",
          "sentpos": [
            "5/8"
          ]
        },
        "megler": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "megler",
          "osn": "megl",
          "sentpos": [
            "5/10"
          ]
        },
        "megler til Nordnet": {
          "wcount": "3",
          "ttype": "NOUN_ADP_PROPN",
          "tname": "megler til Nordnet",
          "osn": [
            "megl",
            "til",
            "nordn"
          ],
          "sentpos": [
            "5/10"
          ]
        },
        "Nordnet": {
          "wcount": "1",
          "ttype": "PROPN",
          "tname": "Nordnet",
          "osn": "nordn",
          "sentpos": [
            "5/12"
          ]
        },
        "anledning": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "anledning",
          "osn": "anledning",
          "sentpos": [
            "7/5"
          ]
        },
        "BankID": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "BankID",
          "osn": "bankid",
          "sentpos": [
            "7/10"
          ]
        },
        "meldingstjeneste": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "meldingstjeneste",
          "osn": "meldingstjenest",
          "sentpos": [
            "7/17"
          ]
        },
        "post": {
          "wcount": "1",
          "ttype": "NOUN",
          "tname": "post",
          "osn": "post",
          "sentpos": [
            "7/25"
          ]
        }
      }
    },
    "sentences": {
      "sent": [
        "I de fleste tilfeller får du beskjeden når du forsøker å handle et verdipapir som ikke er skattemessig hjemmehørende innenfor EØS, til tross for at det muligens handles på Oslo Børs.",
        "Eksempelvis er en god del oljeselskap på Oslo Børs skattemessig hjemmehørende utenfor EØS hvilket gjør at selskapet dermed faller utenfor investeringsuniverset på Aksjesparekonto.",
        "Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar.",
        "San Francisco vurderer å forby robotbud på fortauene.",
        "Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar.",
        "For å flytte aksjer fra en annen bank eller megler til Nordnet, må du sende oss signert overføringsfullmakt.",
        "Eksempelvis er en god del oljeselskap på Oslo Børs skattemessig hjemmehørende utenfor EØS hvilket gjør at selskapet dermed faller utenfor investeringsuniverset på Aksjesparekonto.",
        "Om du ikke har anledning til å signere med BankID, kan følgende overføringsfullmakt sendes via meldingstjenesten når du er logget inn eller i posten."
      ]
    }
  }
}
```

##### E2 - Input data

```JSON
{
	"spell": true, // Boolean true / false (or without this element, then default is false)
	"pos": "ud", // String "spacy" / "ud" / "udkonspekt" / "spacykonspekt" (or without this element, then default is "ud")
	"message": "Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar. For å flytte aksjer fra en annen bank eller megler til Nordnet, må du sende oss signert overføringsfullmakt." // String message.
}
```
##### E2 - Output data

With `"spell": true` (mistake in "briytisk" word)
```XML
<text>
  <sentence>
    <sentnumber>1</sentnumber>
    <sent>Apple vurderer å kjøpe briytisk oppstartfirma for en milliard dollar.</sent>
    <ner>
      <entity>
        <entitytext>Apple</entitytext>
        <label>ORG</label>
        <startentityposcharacter>1</startentityposcharacter>
        <startentitypostoken>1</startentitypostoken>
        <endentityposcharacter>5</endentityposcharacter>
        <endentitypostoken>1</endentitypostoken>
      </entity>
    </ner>
    <item>
      <word>Apple</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>Apple</lemma>
      <number>1</number>
      <speech>PROPN</speech>
      <pos>1</pos>
      <rel_type>nsubj</rel_type>
      <relate>2</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>vurderer</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>vurdere</lemma>
      <number>2</number>
      <speech>VERB</speech>
      <pos>7</pos>
      <rel_type>ROOT</rel_type>
      <relate>2</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>å</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>å</lemma>
      <number>3</number>
      <speech>PART</speech>
      <pos>16</pos>
      <rel_type>mark</rel_type>
      <relate>4</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>kjøpe</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>kjøpe</lemma>
      <number>4</number>
      <speech>VERB</speech>
      <pos>18</pos>
      <rel_type>xcomp</rel_type>
      <relate>2</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>briytisk</word>
      <spell>
        <correctness>False</correctness>
        <sug>britisk</sug>
      </spell>
      <lemma>briytisk</lemma>
      <number>5</number>
      <speech>ADJ</speech>
      <pos>24</pos>
      <rel_type>amod</rel_type>
      <relate>6</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>oppstartfirma</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>oppstartfirme</lemma>
      <number>6</number>
      <speech>NOUN</speech>
      <pos>33</pos>
      <rel_type>dobj</rel_type>
      <relate>4</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>for</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>for</lemma>
      <number>7</number>
      <speech>ADP</speech>
      <pos>47</pos>
      <rel_type>case</rel_type>
      <relate>9</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>en</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>en</lemma>
      <number>8</number>
      <speech>DET</speech>
      <pos>51</pos>
      <rel_type>det</rel_type>
      <relate>9</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>milliard</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>milliard</lemma>
      <number>9</number>
      <speech>NOUN</speech>
      <pos>54</pos>
      <rel_type>det</rel_type>
      <relate>10</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>dollar</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>dollar</lemma>
      <number>10</number>
      <speech>NOUN</speech>
      <pos>63</pos>
      <rel_type>dobj</rel_type>
      <relate>4</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>.</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>.</lemma>
      <number>11</number>
      <speech>PUNCT</speech>
      <pos>69</pos>
      <rel_type>K0</rel_type>
      <relate>0</relate>
      <group_n>1</group_n>
    </item>
  </sentence>
  <sentence>
    <sentnumber>2</sentnumber>
    <sent>For å flytte aksjer fra en annen bank eller megler til Nordnet, må du sende oss signert overføringsfullmakt.</sent>
    <ner>
      <entity>
        <entitytext>Nordnet</entitytext>
        <label>LOC</label>
        <startentityposcharacter>56</startentityposcharacter>
        <startentitypostoken>12</startentitypostoken>
        <endentityposcharacter>62</endentityposcharacter>
        <endentitypostoken>12</endentitypostoken>
      </entity>
    </ner>
    <item>
      <word>For</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>for</lemma>
      <number>1</number>
      <speech>ADP</speech>
      <pos>1</pos>
      <rel_type>case</rel_type>
      <relate>3</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>å</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>å</lemma>
      <number>2</number>
      <speech>PART</speech>
      <pos>5</pos>
      <rel_type>mark</rel_type>
      <relate>3</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>flytte</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>flytte</lemma>
      <number>3</number>
      <speech>VERB</speech>
      <pos>7</pos>
      <rel_type>advcl</rel_type>
      <relate>16</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>aksjer</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>aksje</lemma>
      <number>4</number>
      <speech>NOUN</speech>
      <pos>14</pos>
      <rel_type>dobj</rel_type>
      <relate>3</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>fra</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>fra</lemma>
      <number>5</number>
      <speech>ADP</speech>
      <pos>21</pos>
      <rel_type>case</rel_type>
      <relate>8</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>en</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>en</lemma>
      <number>6</number>
      <speech>DET</speech>
      <pos>25</pos>
      <rel_type>det</rel_type>
      <relate>8</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>annen</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>annen</lemma>
      <number>7</number>
      <speech>DET</speech>
      <pos>28</pos>
      <rel_type>det</rel_type>
      <relate>8</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>bank</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>bank</lemma>
      <number>8</number>
      <speech>NOUN</speech>
      <pos>34</pos>
      <rel_type>nmod</rel_type>
      <relate>3</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>eller</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>eller</lemma>
      <number>9</number>
      <speech>CONJ</speech>
      <pos>39</pos>
      <rel_type>cc</rel_type>
      <relate>8</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>megler</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>megler</lemma>
      <number>10</number>
      <speech>NOUN</speech>
      <pos>45</pos>
      <rel_type>conj</rel_type>
      <relate>8</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>til</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>til</lemma>
      <number>11</number>
      <speech>ADP</speech>
      <pos>52</pos>
      <rel_type>case</rel_type>
      <relate>12</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>Nordnet</word>
      <spell>
        <correctness>False</correctness>
        <sug>Ordnet</sug>
        <sug>Nordnes</sug>
        <sug>Tordnet</sug>
        <sug>Uordnet</sug>
        <sug>Anordnet</sug>
        <sug>Nordnett</sug>
        <sug>Nordnekt</sug>
        <sug>Nordetter</sug>
        <sug>Nordjordet</sug>
        <sug>Anordne</sug>
        <sug>Tordne</sug>
      </spell>
      <lemma>Nordnet</lemma>
      <number>12</number>
      <speech>PROPN</speech>
      <pos>56</pos>
      <rel_type>nmod</rel_type>
      <relate>10</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>,</word>
      <spell>
        <correctness>False</correctness>
        <sug>i</sug>
        <sug>å</sug>
      </spell>
      <lemma>,</lemma>
      <number>13</number>
      <speech>PUNCT</speech>
      <pos>63</pos>
      <rel_type>K0</rel_type>
      <relate>0</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>må</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>må</lemma>
      <number>14</number>
      <speech>AUX</speech>
      <pos>65</pos>
      <rel_type>aux</rel_type>
      <relate>16</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>du</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>-PRON-</lemma>
      <number>15</number>
      <speech>PRON</speech>
      <pos>68</pos>
      <rel_type>nsubj</rel_type>
      <relate>16</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>sende</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>sende</lemma>
      <number>16</number>
      <speech>VERB</speech>
      <pos>71</pos>
      <rel_type>ROOT</rel_type>
      <relate>16</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>oss</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>-PRON-</lemma>
      <number>17</number>
      <speech>PRON</speech>
      <pos>77</pos>
      <rel_type>dobj</rel_type>
      <relate>16</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>signert</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>signere</lemma>
      <number>18</number>
      <speech>VERB</speech>
      <pos>81</pos>
      <rel_type>amod</rel_type>
      <relate>19</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>overføringsfullmakt</word>
      <spell>
        <correctness>False</correctness>
        <sug>overføringfullmakt</sug>
        <sug>overføringfullsmakt</sug>
        <sug>overføringsvullmakt</sug>
        <sug>overføringsflyktning</sug>
        <sug>reguleringsfullmakt</sug>
        <sug>overføringsmuligheta</sug>
        <sug>overføringsmulighet</sug>
      </spell>
      <lemma>overføringsfullmakt</lemma>
      <number>19</number>
      <speech>VERB</speech>
      <pos>89</pos>
      <rel_type>dobj</rel_type>
      <relate>16</relate>
      <group_n>1</group_n>
    </item>
    <item>
      <word>.</word>
      <spell>
        <correctness>True</correctness>
      </spell>
      <lemma>.</lemma>
      <number>20</number>
      <speech>PUNCT</speech>
      <pos>108</pos>
      <rel_type>K0</rel_type>
      <relate>0</relate>
      <group_n>1</group_n>
    </item>
  </sentence>
</text>
```

##### E3 - Input data

**docx** or **pdf** files, multipart/form-data, part name **file**

```javascript
# Fetch API overview https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
# HTML <input type = "file" />, FormData() and fetch().
var formData = new FormData();
var fileField = document.querySelector('input[type="file"]');

# https://developer.mozilla.org/en-US/docs/Web/API/FormData/append
formData.append('file', fileField.files[0]);

fetch("file", 'http://194.44.28.250:45102/api/bot/nb/document/xml/parce', {
                method: 'post',
                body: formData
            })
.then(response => response.text())
.catch(error => console.error('Error:', error))
.then(response => console.log('Success:', response));
```

<u>URL params:</u>

**pos** = spacy / ud / udkonspekt / spacykonspekt (or without this param, then default is "ud")

**spell** = yes / no (or without this param). Default no (usage of **spell** param not recommended  for documents)