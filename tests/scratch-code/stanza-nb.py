# Stanza – A Python NLP Package for Many Human Languages
import stanza

nlp_stanza = stanza.Pipeline(lang='nb', processors='tokenize,mwt,pos,lemma')
doc_stanza = nlp_stanza('formues')
# doc_stanza = nlp_stanza('sparekontoer')
# print(*[f'word: {word.text+" "}\tlemma: {word.lemma}' for sent in doc_stanza.sentences for word in sent.words], sep='\n')
print([word.lemma for sent in doc_stanza.sentences for word in sent.words])


doc = nlp_stanza('formuesskatten.')
for token in doc.sentences[0].tokens:
    print(f'token: {token.text}\twords: {", ".join([word.text for word in token.words])}')