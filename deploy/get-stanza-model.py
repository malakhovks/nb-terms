import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
import stanza
logging.debug('Installing Stance pretrained NLP model for Norwegian Bokmaal.')
stanza.download('nb', dir='./deploy/stanza_resources')
logging.debug('Stance pretrained NLP model for Norwegian Bokmaal is ready to use.')
