# Stanza – A Python NLP Package for Many Human Languages
import stanza

# try:
#     nlp_stanza_en = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
# except:
#     # logging.error(e, exc_info=True)
#     stanza.download('en')
#     nlp_stanza_en = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')

nlp_stanza = stanza.Pipeline(lang='nb', processors='tokenize,mwt,pos,lemma')
# doc_stanza = nlp_stanza('av henger')
# doc_stanza = nlp_stanza('til hører')
doc_stanza = nlp_stanza('formues skatten')
# doc_stanza = nlp_stanza('oppstart firma')
# doc_stanza = nlp_stanza('sparekontoer')
# doc_stanza = nlp_stanza('formuesskatten')
# doc_stanza = nlp_stanza('Formuesskatten er en skatt som utlignes på grunnlag av nettoformuen din.')
# doc_stanza = nlp_stanza('Kurtasjen du betaler avhenger av hvor store beløp du handler for, hvor ofte du handler og hvilken kurtasjeklasse kontoen tilhører.')
# print(*[f'word: {word.text+" "}\tlemma: {word.lemma}' for sent in doc_stanza.sentences for word in sent.words], sep='\n')
print([word.lemma for sent in doc_stanza.sentences for word in sent.words])