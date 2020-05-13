# nb-terms
### nb-terms is an NLU-powered network toolkit (Web service with API) for the contextual and semantic analysis of the natural language text messages (Norwegian Bokmål).

**nb-terms** is an NLU-powered network toolkit (Web service with API) for the contextual and semantic analysis of the natural language text messages (Norwegian Bokmål).

**Allterms API** – is a service features the generation an XML-structure representation (XML-structure and allterms.xml document) of the text message (using [spaCy](https://spacy.io/) with available pretrained statistical model [nb_core_news_sm](https://spacy.io/models/nb#nb_core_news_sm) for Norwegian Bokmål and [NLTK](https://www.nltk.org/) libraries for Norwegian Bokmål) which includes:

- an accurate syntactic dependency parsing;
- part-of-speech POS tagging;
- stemming and lemmatization of words;
- sentence boundary detection;
- split text message into sentences/words;
- iterating over base noun phrases (also known as "noun chunks" – flat phrases that have a noun as their head);

**Input data:**

JSON data which contains text message in Norwegian Bokmål via HTTP POST request method to the corresponding endpoint of API:

```JSON
{
    "message": "Selvkjørende biler flytter forsikringsansvaret over på produsentene."
}
```

Key "message" contains next message which will be processed.

**Output data:**

XML representation (XML-structure and allterms.xml document) of the text message corresponds to the following XML scheme:
The `<exporterms>` element contains a sequence of `<term>` elements that represents the terms (base noun phrases) with their syntactic and semantic specifications from the processed text message.

The syntactic and semantic specifications of the terms are described by the following elements:

-	`<ttype>` element – contains Part of speech POS tag according to the [Universal Dependencies scheme](https://spacy.io/api/annotation);
-	`<tname>` element – contains lemma for the term (the base form of the word or noun phrase);
-	`<wcount>` element – contains number of word per term in the noun phrase;
-	`<osn>` element – contains stems for all words per term in the noun phrase;
-	`<sentpos>` element – contains the position of the term in the text message and represented as a string of the "2/10" format (in this case, it means that the term is in the 2nd sentence by 10 positions)
-	`<relup>` and `<reldown>` elements – reflects relations to other terms according to the [Universal Dependencies scheme](https://spacy.io/api/annotation);
-	`<sentences>` element – contains an array of `<sent>` elements containing sentences from text message. The order of sentences in the `<sentences>` element corresponds to the order of sentences in the input text message.

```xml
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="termsintext">
    <xs:complexType>
      <xs:sequence>
        <xs:element type="xs:string" name="filepath"/>
        <xs:element name="exporterms">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="term" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element type="xs:string" name="ttype"/>
                    <xs:element type="xs:string" name="tname"/>
                    <xs:element type="xs:byte" name="wcount"/>
                    <xs:element type="xs:string" name="osn" maxOccurs="unbounded" minOccurs="0"/>
                    <xs:element type="xs:string" name="sentpos" maxOccurs="unbounded" minOccurs="0"/>
                    <xs:element type="xs:short" name="relup" maxOccurs="unbounded" minOccurs="0"/>
                    <xs:element type="xs:short" name="reldown" maxOccurs="unbounded" minOccurs="0"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="sentences">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="sent" maxOccurs="unbounded" minOccurs="0"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```
**Parse API** – is a service features the generation an XML-like representation (XML-structure and parse.xml document) of the text message (using [spaCy](https://spacy.io/) with available pretrained statistical model [nb_core_news_sm](https://spacy.io/models/nb#nb_core_news_sm) for Norwegian Bokmål and [NLTK](https://www.nltk.org/) libraries for Norwegian Bokmål) which includes:

-	an accurate syntactic dependency parsing;
-	Named entity recognition tagging;
-	part of speech POS tagging;
-	stemming and lemmatization of words;
-	sentence boundary detection;
-	splitting a text meesage into meaningful segments, called tokens;

**Input data:**

JSON data which contains text message in Norwegian Bokmål via HTTP POST request method to the corresponding endpoint of API:
```JSON
{
"message": "Selvkjørende biler flytter forsikringsansvaret over på produsentene."
}
```

Key "message" contains next message which will be processed.

**Output data:**

XML representation (XML-structure and parse.xml document) of the text message corresponds to the following XML scheme:
The `<text>` element contains a sequence of `<sentence>` elements that represents sentences and their specifications according to the NLP results of the text message, in particular, syntactic analysis, grammatical analysis and morphological analysis of the sentences.
The specifications of the sentences are described by the following elements:

-	`<sentnumber>` element – contains the position of a sentence in the text message and represened as a string of the "1" format (in this case, it means that the sentence is at 1 position in the text message);
-	`<sent>` element – contains a sentence from the text message;
-	`<ner>` element – contains a sequence of `<entity>` elements that represents named entities (the default nb_core_news_sm model identifies a variety of named and numeric entities, including companies, locations, organizations and products.):
  - `<entitytext>` element – contains lemma for the named entity;
  - `<label>` element – contains the type of the named entity according to the [spaCy annotations](https://spacy.io/api/annotation#named-entities);
  - `<startentityposcharacter>` element – contains the position of the first character of the named entity (tokenization at the character level), and represented as a string of the format "51" (in this case, it means that the first character of the named entity is at 51 positions in the sentence);
  - `<endentityposcharacter>` element – contains the position of the last character of the named entity (tokenization at the character level), and represented as a string of the format "81" (in this case, it means that the last character of the named entity is at 81 positions in the sentence);
  - `<startentitypostoken>` element – contains the position of the first token (first word) of the named entity (tokenization at the word level) and represented as a string of format "11" (in this case, it means that the position of the first token (first word) of the named entity in the sentence is 15);
  - `<endentitypostoken>` element – contains the position of the last token (last word) of the named entity (tokenization at the word level) and represented as a string of format "11" (in this case, it means that the position of the last token (last word) of the named entity in the sentence is 15);
-	`<item>` element – contains a set of elements that represents the linguistic parameters of words in the sentence:
  - `<word>` element – contains a word in original form;
  - `<lemma>` element – contains lemma for the word (the base form of the word)
  - `<number>` element – contains the position of the word (tokenization at the level of words) and represented as a string of format “1” (in this case, it means that the position of the word in the sentence is 1);
  - `<speech>` element – contains Part of speech POS tag according to the [Universal Dependencies scheme](https://spacy.io/api/annotation);
  - `<pos>` element – the position of the first character of the word (tokenization at the character level), and represented as a string of format “7” (in this case, means that the first character of the word is at 7 positions in the sentence);
  - `<rel_type>` element – contains syntactic dependency according to the [spaCy dependency parsing](https://spacy.io/api/annotation#dependency-parsing);
  - `<relate>` element – contains the position of the word (tokenization at the word level) to which there is a syntactic dependence, and represented as a string of format "9" (in this case, it means that the position of the word in the sentence to which is the syntax dependence is 1).

```XML
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="text">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="sentence" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="item" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element type="xs:string" name="word"/>
                    <xs:element type="xs:string" name="osnova"/>
                    <xs:element type="xs:string" name="lemma"/>
                    <xs:element type="xs:string" name="kflex"/>
                    <xs:element type="xs:string" name="flex"/>
                    <xs:element type="xs:byte" name="number"/>
                    <xs:element type="xs:short" name="pos"/>
                    <xs:element type="xs:byte" name="group_n"/>
                    <xs:element type="xs:string" name="speech"/>
                    <xs:element type="xs:byte" name="relate"/>
                    <xs:element type="xs:string" name="rel_type"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
              <xs:element type="xs:byte" name="sentnumber"/>
              <xs:element type="xs:string" name="sent"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```