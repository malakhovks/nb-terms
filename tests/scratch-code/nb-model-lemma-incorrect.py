import spacy

nlp = spacy.load("nb_core_news_sm")
doc = nlp("Formuesskatten er en skatt som utlignes på grunnlag av nettoformuen din.")
doc1 = nlp("Formuess")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

for token in doc1:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)