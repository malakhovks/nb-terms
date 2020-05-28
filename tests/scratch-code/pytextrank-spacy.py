import spacy
import pytextrank

nlp = spacy.load('nb_core_news_sm')

tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)

# text = 'Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar.'
# text = 'Selvkjørende biler flytter forsikringsansvaret over på produsentene.'
text = 'Apple vurderer å kjøpe britisk oppstartfirma for en milliard dollar. San Francisco vurderer å forby robotbud på fortauene. For å flytte aksjer fra en annen bank eller megler til Nordnet, må du sende oss signert overføringsfullmakt.'
doc = nlp(text)

# examine the top-ranked phrases in the document
for p in doc._.phrases:
    print('{:.4f} {:5d}  {}'.format(p.rank, p.count, p.text))
    print(p.chunks)