import spacy
# load SnowballStemmer stemmer from nltk
from nltk.stem.snowball import SnowballStemmer
# Load globally english SnowballStemmer
NORWEGIAN_STEMMER = SnowballStemmer("norwegian")

nlp = spacy.load("nb_core_news_sm")
doc = nlp("Formuesskatten er en skatt som utlignes på grunnlag av nettoformuen din.")
# doc1 = nlp("sparekontoer")
doc1 = nlp("til hører")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

for token in doc1:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

print(NORWEGIAN_STEMMER.stem('formues'))