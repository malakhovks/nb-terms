import spacy
# from spacy.symbols import *
from spacy.matcher import Matcher
import textacy
import textacy.ke

nlp = spacy.load("nb_core_news_sm")
doc = nlp("San Francisco vurderer å forby robotbud på fortauene.")
# doc = nlp("Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar.")

# default spaCy
print('spaCy default -------------------------------------------------------------------------------------')
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)
print('-------------------------------------------------------------------------------------')
# default spaCy

# TEXTACY--------------------------------------------
print('textacy -------------------------------------------------------------------------------------')
sentence = 'I de fleste tilfeller får du beskjeden når du forsøker å handle et verdipapir som ikke er skattemessig hjemmehørende innenfor EØS, til tross for at det muligens handles på Oslo Børs. Eksempelvis er en god del oljeselskap på Oslo Børs skattemessig hjemmehørende utenfor EØS hvilket gjør at selskapet dermed faller utenfor investeringsuniverset på Aksjesparekonto. Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar. San Francisco vurderer å forby robotbud på fortauene. Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar. For å flytte aksjer fra en annen bank eller megler til Nordnet, må du sende oss signert overføringsfullmakt.'
# pattern = r'<DET>?(<NOUN>+<ADP|CONJ>)*<NOUN>+'
# # pattern = r'<PREP><DET>?(<NOUN>+<ADP>)*<NOUN>+'
doc = textacy.make_spacy_doc(sentence, lang='nb_core_news_sm')
# lists = textacy.extract.pos_regex_matches(doc, pattern)
# for lst in lists:
#     print(lst.text)

# ts = textacy.TextStats(doc)
# print(ts.basic_counts)
# print(list(textacy.extract.ngrams(doc, 1, filter_stops=True, filter_punct=True, filter_nums=False)))

print(textacy.ke.textrank(doc, normalize="lemma", topn=10))

print('-------------------------------------------------------------------------------------')
# TEXTACY --------------------------------------------

print('spaCy matcher -------------------------------------------------------------------------------------')
examples = [
    "Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar.",
    "San Francisco vurderer å forby robotbud på fortauene.",
    "For overføringer til aksje- og fondskonto, kan følgende overføringsfullmakt benyttes.",
    "Selvkjørende biler flytter forsikringsansvaret over på produsentene."
    ]
patterns = [
    [{'POS': 'PROPN'}],
    [{'POS': 'NOUN'}],
    [{'POS': {'IN':['NOUN', 'ADJ','PROPN']}}, {'POS': {'IN':['NOUN', 'ADJ','PROPN']}}]
    # [{'ENT_TYPE': 'GPE_LOC'}]
    ]
matcher = Matcher(nlp.vocab)
# matcher.add("PROPN", None, patterns[0])
# matcher.add("NOUN", None, patterns[1])
matcher.add("NOUN/ADJ/PROPN+NOUN/ADJ/PROPN", None, patterns[2])
# matcher.add("GPE", None, patterns[3])
for text in examples:
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        print(string_id, span.start_char, span.end_char, span.text, span.root.pos_, span.root.text)
        if len(span) == 2:
            if [tkn.text for tkn in span].index(span.root.text) == 0:
                print('child: ' + span[1].text)
            else:
                print('child: ' + span[0].text)

