#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# load tempfile for temporary dir creation
import sys, os, tempfile, subprocess

# load libraries for NLP pipeline
import spacy

# load misc utils
import json
# import uuid
from werkzeug.utils import secure_filename
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# load libraries for string proccessing
import re, string

# load libraries for pdf processing pdfminer
from io import StringIO, BytesIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# load libraries for docx processing
import zipfile
WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
# load libraries for XML proccessing
import xml.etree.ElementTree as ET

# load libraries for API proccessing
from flask import Flask, jsonify, flash, request, Response, redirect, url_for, abort, render_template

# A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
from flask_cors import CORS

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx'])
VOWELS = set(['a', 'e', 'i', 'o', 'u', 'y', 'æ', 'ø', 'å'])

# Load globally spaCy model via package name
NLP_NB = spacy.load('nb_core_news_sm')
# Load lemmas only
NLP_NB_LEMMA = spacy.load('nb_core_news_sm', disable=["parser", "tagger"])

# Stanza – A Python NLP Package for Many Human Languages
# import stanza
# from spacy_stanza import StanzaLanguage
# try:
#     snlp = stanza.Pipeline(lang="nb", processors='tokenize,mwt,pos,lemma', dir='./deploy/stanza_resources')
#     stanza_nlp = StanzaLanguage(snlp)
# except:
#     logging.debug('Installing Stance pretrained NLP model for Norwegian Bokmaal.')
#     stanza.download('nb', dir='./deploy/stanza_resources')
#     logging.debug('Stance pretrained NLP model for Norwegian Bokmaal is ready to use.')
#     snlp = stanza.Pipeline(lang="nb", processors='tokenize,mwt,pos,lemma', dir='./deploy/stanza_resources')
#     stanza_nlp = StanzaLanguage(snlp)

# load SnowballStemmer stemmer from nltk
from nltk.stem.snowball import SnowballStemmer
# Load globally english SnowballStemmer
NORWEGIAN_STEMMER = SnowballStemmer("norwegian")

# for hunspell https://github.com/blatinier/pyhunspell
import hunspell
nb_spell = hunspell.HunSpell('./deploy/dictionary/nb.dic', './deploy/dictionary/nb.aff')

# load mtag
import mtag

__author__ = "Kyrylo Malakhov <malakhovks@nas.gov.ua> and Vitalii Velychko <aduisukr@gmail.com>"
__copyright__ = "Copyright (C) 2020 Kyrylo Malakhov <malakhovks@nas.gov.ua> and Vitalii Velychko <aduisukr@gmail.com>"

app = Flask(__name__)
CORS(app)

"""
Limited the maximum allowed payload to 16 megabytes.
If a larger file is transmitted, Flask will raise an RequestEntityTooLarge exception.
"""
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

"""
Set the secret key to some random bytes. Keep this really secret!
How to generate good secret keys.
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for Flask.secret_key (or SECRET_KEY):
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
"""
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = os.urandom(42)

"""
# ------------------------------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------------------------------
# """
# function that check if an extension is valid
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# default sentence normalization
def sentence_normalization_default(raw_sentence):
    # remove tabs and insert spaces
    raw_sentence = re.sub('[\t]', ' ', raw_sentence)
    # remove multiple spaces
    raw_sentence = re.sub('\s\s+', ' ', raw_sentence)
    # remove all numbers
    # line = re.sub(r'\d+','',line)
    # remove leading and ending spaces
    raw_sentence = raw_sentence.strip()
    normalized_sentence = raw_sentence
    return normalized_sentence

# default text normalization
def text_normalization_default(raw_text):
    raw_text_list = []
    for line in raw_text.splitlines(True):
        # if line contains letters
        if re.search(r'[a-z]+', line):
            """
            remove \n \r \r\n new lines and insert spaces
            \r = CR (Carriage Return) → Used as a new line character in Mac OS before X
            \n = LF (Line Feed) → Used as a new line character in Unix/Mac OS X
            \r\n = CR + LF → Used as a new line character in Windows
            """
            """
            \W pattern: When the LOCALE and UNICODE flags are not specified, matches any non-alphanumeric character;
            this is equivalent to the set [^a-zA-Z0-9_]. With LOCALE, it will match any character not in the set [0-9_], and not defined as alphanumeric for the current locale.
            If UNICODE is set, this will match anything other than [0-9_] plus characters classified as not alphanumeric in the Unicode character properties database.
            To remove all the non-word characters, the \W pattern can be used as follows:
            """
            # line = re.sub(r'\W', ' ', line, flags=re.I)
            # remove all non-words except punctuation
            # line = re.sub('[^\w.,;!?-]', ' ', line)
            # remove all words which contains number
            line = re.sub(r'\w*\d\w*', ' ', line)
            # remove % symbol
            line = re.sub('%', ' ', line)
            # remove ° symbol
            line = re.sub('[°]', ' ', line)
            line = re.sub('[\n]', ' ', line)
            line = re.sub('[\r\n]', ' ', line)
            line = re.sub('[\r]', ' ', line)
            # remove tabs and insert spaces
            line = re.sub('[\t]', ' ', line)
            # Replace multiple dots with space
            line = re.sub('\.\.+', ' ', line)
            # remove multiple spaces
            line = re.sub('\s\s+', ' ', line)
            # remove all numbers
            # line = re.sub(r'\d+','',line)
            # remove leading and ending spaces
            line = line.strip()
            raw_text_list.append(line)
    yet_raw_text = ' '.join(raw_text_list)
    return yet_raw_text

# Extracting all the text from DOCX
def get_unicode_from_docx(docx_path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(docx_path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = ET.XML(xml_content)
    paragraphs = []
    for paragraph in tree.iter(PARA):
        texts = [node.text
                 for node in paragraph.iter(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))
    return '\n\n'.join(paragraphs)
# Extracting all the text from PDF with PDFMiner.six
def get_unicode_from_pdf(pdf_path):
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()
    # save document layout including spaces that are only visual not a character
    """
    Some pdfs mark the entire text as figure and by default PDFMiner doesn't try to perform layout analysis for figure text. To override this behavior the all_texts parameter needs to be set to True
    """
    laparams = LAParams()
    setattr(laparams, 'all_texts', True)
    # save document layout including spaces that are only visual not a character
    with StringIO() as retstr:
        with TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams) as device:
            with open(pdf_path, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()
                for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
                    interpreter.process_page(page)
        return retstr.getvalue()
"""
# ------------------------------------------------------------------------------------------------------
# """

@app.route('/help')
def index():
    return Response(render_template('help.html'), mimetype='text/html')

"""
# API ---------------------------------------------------------------------------------------------------
# """
# --------------------------------------------------------------------------------------------------------
# Text messages
@app.route('/api/bot/nb/message/xml/parce', methods=['POST'])
def get_quick_parcexml():
    # POS UD
    # https://universaldependencies.org/u/pos/
    if request.args.get('pos', None) == 'udkonspekt':
        speech_dict_POS_tags = {'NOUN':'S1', 'ADJ':'S2', 'VERB': 'S4', 'INTJ':'S21', 'PUNCT':'98', 'SYM':'98', 'CONJ':'U', 'NUM':'S7', 'X':'99', 'PRON':'S11', 'ADP':'P', 'PROPN':'S22', 'ADV':'S16', 'AUX':'99', 'CCONJ':'U', 'DET':'99', 'PART':'99', 'SCONJ':'U', 'SPACE':'98'}
    # TODO Correctly relate the parts of speech with spaCy
    # tag_map.py in https://github.com/explosion/spaCy/tree/master/spacy/lang
    # POS spaCy
    if request.args.get('pos', None) == 'spacykonspekt':
        speech_dict_POS_tags = {'NOUN':'S1', 'ADJ':'S2', 'VERB': 'S4', 'INTJ':'S21', 'PUNCT':'98', 'SYM':'98', 'CONJ':'U', 'NUM':'S7', 'X':'S29', 'PRON':'S10', 'ADP':'P', 'PROPN':'S22', 'ADV':'S16', 'AUX':'AUX', 'CCONJ':'CCONJ', 'DET':'DET', 'PART':'PART', 'SCONJ':'SCONJ', 'SPACE':'SPACE'}

    req_data = request.get_json()

    try:
        doc = NLP_NB(req_data['message'])
        """
        # create the <parce.xml> file structure
        """
        # create root element <text>
        root_element = ET.Element("text")

        for sentence_index, sentence in enumerate(doc.sents):
            # XML structure creation
            new_sentence_element = ET.Element('sentence')
            # create and append <sentnumber>
            new_sentnumber_element = ET.Element('sentnumber')
            new_sentnumber_element.text = str(sentence_index+1)
            new_sentence_element.append(new_sentnumber_element)
            # create and append <sent>
            new_sent_element = ET.Element('sent')
            new_sent_element.text = sentence.text
            new_sentence_element.append(new_sent_element)

            doc_for_lemmas = NLP_NB(sentence.text)

            logging.debug('Sentence: ' + sentence.text)

            # create amd append <ner>, <entity>
            # NER labels description https://spacy.io/api/annotation#named-entities
            if len(doc_for_lemmas.ents) != 0:
                # create <ner>
                ner_element = ET.Element('ner')
                for ent in doc_for_lemmas.ents:
                    # create <entity>
                    new_entity_element = ET.Element('entity')
                    # create and append <entitytext>
                    new_entity_text_element = ET.Element('entitytext')
                    new_entity_text_element.text = ent.text
                    new_entity_element.append(new_entity_text_element)
                    # create and append <label>
                    new_entity_label_element = ET.Element('label')
                    new_entity_label_element.text = ent.label_
                    new_entity_element.append(new_entity_label_element)
                    # create and append <startentitypos>
                    new_start_entity_pos_character_element = ET.Element('startentityposcharacter')
                    new_start_entity_pos_token_element = ET.Element('startentitypostoken')
                    new_start_entity_pos_character_element.text = str(ent.start_char + 1)
                    new_start_entity_pos_token_element.text = str(ent.start + 1)
                    new_entity_element.append(new_start_entity_pos_character_element)
                    new_entity_element.append(new_start_entity_pos_token_element)
                    # create and append <endentitypos>
                    new_end_entity_pos_character_element = ET.Element('endentityposcharacter')
                    new_end_entity_pos_token_element = ET.Element('endentitypostoken')
                    new_end_entity_pos_character_element.text = str(ent.end_char)
                    new_end_entity_pos_token_element.text = str(ent.end)
                    new_entity_element.append(new_end_entity_pos_character_element)
                    new_entity_element.append(new_end_entity_pos_token_element)
                    # append <entity> to <ner>
                    ner_element.append(new_entity_element)
                # append <ner> to <sentence>
                new_sentence_element.append(ner_element)
            # create and append <item>, <word>, <lemma>, <number>, <pos>, <speech>
            for lemma in doc_for_lemmas:
                # create and append <item>
                new_item_element = ET.Element('item')
                # create and append <word>
                new_word_element = ET.Element('word')
                new_word_element.text = lemma.text
                new_item_element.append(new_word_element)
                # create and append <spell>
                if 'spell' in req_data:
                    if req_data['spell'] == True:
                        new_spell_element = ET.Element('spell')
                        new_correctness_element = ET.Element('correctness')
                        if nb_spell.spell(lemma.text):
                            new_correctness_element.text = str(nb_spell.spell(lemma.text))
                            new_spell_element.append(new_correctness_element)
                            new_item_element.append(new_spell_element)
                        else:
                            new_correctness_element.text = str(nb_spell.spell(lemma.text))
                            new_spell_element.append(new_correctness_element)
                            new_suggest_element = ET.Element('suggest')
                            for sggst in nb_spell.suggest(lemma.text):
                                new_sug_element = ET.Element('sug')
                                new_sug_element.text = sggst
                                new_spell_element.append(new_sug_element)
                            new_item_element.append(new_spell_element)
                # create and append <lemma>
                new_lemma_element = ET.Element('lemma')
                # -PRON- detection
                if lemma.lemma_ not in ['-PRON-']:
                    new_lemma_element.text = lemma.lemma_ #.encode('ascii', 'ignore')
                else:
                    new_lemma_element.text = lemma.text
                new_item_element.append(new_lemma_element)
                # create and append <number>
                new_number_element = ET.Element('number')
                new_number_element.text = str(lemma.i+1)
                new_item_element.append(new_number_element)
                # create and append <speech>
                new_speech_element = ET.Element('speech')
                # compound words split
                if 'compound' in req_data:
                    if req_data['compound']:
                        if lemma.pos_ in ["NOUN"]:
                            if len(lemma.text) > 7:
                                logging.debug('---------------------------------------------------------------------------------------------------')

                                temp_file = secure_filename('dbskv.txt')
                                destination = "/".join([tempfile.mkdtemp(),temp_file])
                                try:
                                    with open(destination, 'w') as f:
                                        f.write(lemma.lemma_ + ' . ' + lemma.text.lower())
                                except IOError as e:
                                    logging.error(e, exc_info=True)
                                    return abort(500)

                                try:
                                    result_list = mtag.anal(destination)
                                except Exception as e:
                                    logging.error(e, exc_info=True)
                                    return abort(500)


                                logging.debug('mtag processing result: ' + '\n' + ''.join(result_list))

                                if result_list == '':
                                    logging.debug('Error while processing Word <' + lemma.text + '>. Maybe spell error.')
                                else:
                                    result_string = ''.join(result_list)
                                    out = re.sub('[\t]', '', result_string)
                                    out_1 = out.split('\n')[1]
                                    out_n = out.split('\n')[out.split('\n').index('"." symb') + 2]
                                    logging.debug('out_n: ' + out_n)

                                    try:
                                        mtag_compound_lemma = re.search(r'\"(.*)\"', out_n).group(1)

                                        # Check for lemma correctness
                                        # if correct
                                        if lemma.lemma_ == mtag_compound_lemma:
                                            logging.debug('Compound word lemma correctness (lemmas IS EQUAL) spaCy | mtag:: '  + lemma.lemma_ + ' | ' + mtag_compound_lemma)

                                            second_word = re.search(r'\<\+(.*)\>', out_1).group(1)
                                            out_compound_word = out.split('\n')[out.split('\n').index('"." symb') + 1]
                                            out_compound_word = re.search(r'\<(.*)\>', out_compound_word).group(1)
                                            first_word = re.search(r'(.*)' + second_word, out_compound_word).group(1)

                                            # Check if first_word ending with <e> or <s>
                                            if re.search(r'[es]$', first_word):
                                                # Check if first_word ending with <e>
                                                if re.search(r'[e]$', first_word):
                                                    vowel_counts = dict((c, first_word.count(c)) for c in VOWELS)
                                                    counts = vowel_counts.values()
                                                    # Check if first_word includes 2 vowels
                                                    if sum(counts) == 2:
                                                        first_word = first_word[:-1]
                                                # Check if first_word ending with <s>
                                                if re.search(r'[s]$', first_word):
                                                    first_word = first_word[:-1]
                                                    # Check if first_word includes 1 vowel
                                                    # vowel_counts = dict((c, first_word.count(c)) for c in VOWELS)
                                                    # counts = vowel_counts.values()
                                                    # if sum(counts) == 1:
                                                    #     first_word = first_word[:-1]

                                            # get lemmas with spaCy
                                            spacy_doc_lemmas = NLP_NB_LEMMA(first_word + ' ' + second_word)
                                            spacy_compound_words_lemmas_arr = [token.lemma_ for token in spacy_doc_lemmas]
                                            logging.debug('Compound word <first_lemma> with spaCy: ' + spacy_compound_words_lemmas_arr[0])
                                            logging.debug('Compound word <second_lemma> with spaCy: ' + spacy_compound_words_lemmas_arr[1])

                                            # create <compound>
                                            new_compound_element = ET.Element('compound')
                                            first_word_element = ET.Element('first_lemma')
                                            first_word_element.text = spacy_compound_words_lemmas_arr[0]
                                            new_compound_element.append(first_word_element)
                                            second_word_element = ET.Element('second_lemma')
                                            second_word_element.text = spacy_compound_words_lemmas_arr[1]
                                            new_compound_element.append(second_word_element)
                                            new_item_element.append(new_compound_element)
                                        # Check for lemma correctness
                                        # if not correct
                                        else:
                                            logging.debug('Compound word lemma correctness (lemmas IS NOT EQUAL) spaCy | mtag: ' + lemma.lemma_ + ' | ' + mtag_compound_lemma)

                                            # Changing for correct lemma
                                            correct_lemma_element = new_item_element.find('lemma')
                                            correct_lemma_element.text = mtag_compound_lemma

                                            second_word = re.search(r'\<\+(.*)\>', out_n).group(1)
                                            out_compound_word = out.split('\n')[out.split('\n').index('"." symb') + 1]
                                            out_compound_word = re.search(r'\<(.*)\>', out_compound_word).group(1)
                                            first_word = re.search(r'(.*)' + second_word, out_compound_word).group(1)
                                            # Check if first_word ending with <e> or <s>
                                            if re.search(r'[es]$', first_word):
                                                # Check if first_word ending with <e>
                                                if re.search(r'[e]$', first_word):
                                                    vowel_counts = dict((c, first_word.count(c)) for c in VOWELS)
                                                    counts = vowel_counts.values()
                                                    # Check if first_word includes 2 vowels
                                                    if sum(counts) == 2:
                                                        first_word = first_word[:-1]
                                                # Check if first_word ending with <s>
                                                if re.search(r'[s]$', first_word):
                                                    first_word = first_word[:-1]
                                            # get lemmas with spaCy
                                            spacy_doc_lemmas = NLP_NB_LEMMA(first_word + ' ' + second_word)
                                            spacy_compound_words_lemmas_arr = [token.lemma_ for token in spacy_doc_lemmas]
                                            logging.debug('Compound word <first_lemma> with spaCy: ' + spacy_compound_words_lemmas_arr[0])
                                            logging.debug('Compound word <second_lemma> with spaCy: ' + spacy_compound_words_lemmas_arr[1])

                                            # create <compound>
                                            new_compound_element = ET.Element('compound')
                                            first_word_element = ET.Element('first_lemma')
                                            # first_word_element.text = mtag_first_word_lemma
                                            first_word_element.text = spacy_compound_words_lemmas_arr[0]
                                            new_compound_element.append(first_word_element)
                                            second_word_element = ET.Element('second_lemma')
                                            # second_word_element.text = spacy_second_word_lemma_arr[0]
                                            second_word_element.text = spacy_compound_words_lemmas_arr[1]
                                            new_compound_element.append(second_word_element)
                                            new_item_element.append(new_compound_element)
                                    except AttributeError:
                                        logging.debug('Error while processing Word <' + lemma.text + '>. Maybe not compound word.')
                if 'pos' in req_data:
                    if req_data['pos'] == 'ud':
                        new_speech_element.text = lemma.pos_
                    elif req_data['pos'] == 'udkonspekt':
                        # relate the universal dependencies parts of speech with konspekt tags
                        new_speech_element.text = speech_dict_POS_tags[lemma.pos_]
                    elif req_data['pos'] == 'spacykonspekt':
                        # relate the spaCy parts of speech with konspekt tags
                        new_speech_element.text = speech_dict_POS_tags[lemma.tag_]
                    elif req_data['pos'] == 'spacy':
                        # spaCy Fine-grained part-of-speech.
                        # tag_map.py in https://github.com/explosion/spaCy/tree/master/spacy/lang
                        new_speech_element.text = lemma.tag_
                if 'pos' not in req_data:
                    # Coarse-grained part-of-speech from the Universal POS tag set.
                    # https://spacy.io/api/annotation#pos-tagging
                    new_speech_element.text = lemma.pos_
                new_item_element.append(new_speech_element)
                # create and append <pos>
                new_pos_element = ET.Element('pos')
                new_pos_element.text = str(lemma.idx+1)
                new_item_element.append(new_pos_element)

                # create and append <relate> and <rel_type>
                new_rel_type_element = ET.Element('rel_type')
                new_relate_element = ET.Element('relate')
                if lemma.dep_ == 'punct':
                    new_rel_type_element.text = 'K0'
                    new_relate_element.text = '0'
                    new_item_element.append(new_rel_type_element)
                    new_item_element.append(new_relate_element)
                else:
                    new_rel_type_element.text = lemma.dep_
                    new_item_element.append(new_rel_type_element)
                    new_relate_element.text = str(lemma.head.i+1)
                    new_item_element.append(new_relate_element)

                # create and append <group_n>
                new_group_n_element = ET.Element('group_n')
                new_group_n_element.text = '1'
                new_item_element.append(new_group_n_element)

                new_sentence_element.append(new_item_element)
            # create full <parce.xml> file structure
            root_element.append(new_sentence_element)
        return Response(ET.tostring(root_element, encoding='utf8', method='xml'), mimetype='text/xml')
    except Exception as e:
        logging.error(e, exc_info=True)
        return abort(500)
# --------------------------------------------------------------------------------------------------------
# Text documents
@app.route('/api/bot/nb/document/xml/parce', methods=['POST'])
def get_parcexml_from_documents():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return abort(400)

    file = request.files['file']

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return abort(400)

    if file and allowed_file(file.filename):
        # pdf processing
        if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
            pdf_file = secure_filename(file.filename)
            destination = "/".join([tempfile.mkdtemp(),pdf_file])
            file.save(destination)
            file.close()
            if os.path.isfile(destination):
                raw_text = get_unicode_from_pdf(destination)
        # docx processing
        if file.filename.rsplit('.', 1)[1].lower() == 'docx':
            docx_file = secure_filename(file.filename)
            destination = "/".join([tempfile.mkdtemp(),docx_file])
            file.save(destination)
            file.close()
            if os.path.isfile(destination):
                raw_text = get_unicode_from_docx(destination)
        # txt processing
        if file.filename.rsplit('.', 1)[1].lower() == 'txt':
            txt_file = secure_filename(file.filename)
            destination = "/".join([tempfile.mkdtemp(),txt_file])
            file.save(destination)
            file.close()
            with open(destination) as t_f:
                raw_text = t_f.read()
    # POS UD
    # https://universaldependencies.org/u/pos/
    if request.args.get('pos', None) == 'udkonspekt':
        speech_dict_POS_tags = {'NOUN':'S1', 'ADJ':'S2', 'VERB': 'S4', 'INTJ':'S21', 'PUNCT':'98', 'SYM':'98', 'CONJ':'U', 'NUM':'S7', 'X':'99', 'PRON':'S11', 'ADP':'P', 'PROPN':'S22', 'ADV':'S16', 'AUX':'99', 'CCONJ':'U', 'DET':'99', 'PART':'99', 'SCONJ':'U', 'SPACE':'98'}
    # TODO Correctly relate the parts of speech with spaCy
    # POS spaCy
    if request.args.get('pos', None) == 'spacykonspekt':
        speech_dict_POS_tags = {'NOUN':'S1', 'ADJ':'S2', 'VERB': 'S4', 'INTJ':'S21', 'PUNCT':'98', 'SYM':'98', 'CONJ':'U', 'NUM':'S7', 'X':'S29', 'PRON':'S10', 'ADP':'P', 'PROPN':'S22', 'ADV':'S16', 'AUX':'AUX', 'CCONJ':'CCONJ', 'DET':'DET', 'PART':'PART', 'SCONJ':'SCONJ', 'SPACE':'SPACE'}

    try:

        text_normalized = text_normalization_default(raw_text)

        doc = NLP_NB(text_normalized)

        """
        # create the <parce.xml> file structure
        """
        # create root element <text>
        root_element = ET.Element("text")

        for sentence_index, sentence in enumerate(doc.sents):
            # default sentence normalization
            sentence_clean = sentence_normalization_default(sentence.text)
            # XML structure creation
            new_sentence_element = ET.Element('sentence')
            # create and append <sentnumber>
            new_sentnumber_element = ET.Element('sentnumber')
            new_sentnumber_element.text = str(sentence_index+1)
            new_sentence_element.append(new_sentnumber_element)
            # create and append <sent>
            new_sent_element = ET.Element('sent')
            new_sent_element.text = sentence_clean
            new_sentence_element.append(new_sent_element)

            doc_for_lemmas = NLP_NB(sentence_clean)
            # create amd append <ner>, <entity>
            # NER labels description https://spacy.io/api/annotation#named-entities
            if len(doc_for_lemmas.ents) != 0:
                # create <ner>
                ner_element = ET.Element('ner')
                for ent in doc_for_lemmas.ents:
                    # create <entity>
                    new_entity_element = ET.Element('entity')
                    # create and append <entitytext>
                    new_entity_text_element = ET.Element('entitytext')
                    new_entity_text_element.text = ent.text
                    new_entity_element.append(new_entity_text_element)
                    # create and append <label>
                    new_entity_label_element = ET.Element('label')
                    new_entity_label_element.text = ent.label_
                    new_entity_element.append(new_entity_label_element)
                    # create and append <startentitypos>
                    new_start_entity_pos_character_element = ET.Element('startentityposcharacter')
                    new_start_entity_pos_token_element = ET.Element('startentitypostoken')
                    new_start_entity_pos_character_element.text = str(ent.start_char + 1)
                    new_start_entity_pos_token_element.text = str(ent.start + 1)
                    new_entity_element.append(new_start_entity_pos_character_element)
                    new_entity_element.append(new_start_entity_pos_token_element)
                    # create and append <endentitypos>
                    new_end_entity_pos_character_element = ET.Element('endentityposcharacter')
                    new_end_entity_pos_token_element = ET.Element('endentitypostoken')
                    new_end_entity_pos_character_element.text = str(ent.end_char)
                    new_end_entity_pos_token_element.text = str(ent.end)
                    new_entity_element.append(new_end_entity_pos_character_element)
                    new_entity_element.append(new_end_entity_pos_token_element)
                    # append <entity> to <ner>
                    ner_element.append(new_entity_element)
                # append <ner> to <sentence>
                new_sentence_element.append(ner_element)
            # create and append <item>, <word>, <lemma>, <number>, <pos>, <speech>
            for lemma in doc_for_lemmas:
                # create and append <item>
                new_item_element = ET.Element('item')
                # create and append <word>
                new_word_element = ET.Element('word')
                new_word_element.text = lemma.text
                new_item_element.append(new_word_element)
                # create and append <spell>
                if request.args.get('spell', None) == 'yes':
                    new_spell_element = ET.Element('spell')
                    new_correctness_element = ET.Element('correctness')
                    if nb_spell.spell(lemma.text):
                        new_correctness_element.text = str(nb_spell.spell(lemma.text))
                        new_spell_element.append(new_correctness_element)
                        new_item_element.append(new_spell_element)
                    else:
                        new_correctness_element.text = str(nb_spell.spell(lemma.text))
                        new_spell_element.append(new_correctness_element)
                        new_suggest_element = ET.Element('suggest')
                        for sggst in nb_spell.suggest(lemma.text):
                            new_sug_element = ET.Element('sug')
                            new_sug_element.text = sggst
                            new_spell_element.append(new_sug_element)
                        new_item_element.append(new_spell_element)
                # create and append <lemma>
                new_lemma_element = ET.Element('lemma')
                # -PRON- detection
                if lemma.lemma_ not in ['-PRON-']:
                    new_lemma_element.text = lemma.lemma_ #.encode('ascii', 'ignore')
                else:
                    new_lemma_element.text = lemma.text
                new_item_element.append(new_lemma_element)
                # create and append <number>
                new_number_element = ET.Element('number')
                new_number_element.text = str(lemma.i+1)
                new_item_element.append(new_number_element)
                # create and append <speech>
                new_speech_element = ET.Element('speech')
                # relate the universal dependencies parts of speech with konspekt tags
                if request.args.get('pos', None) == 'udkonspekt':
                    new_speech_element.text = speech_dict_POS_tags[lemma.pos_]
                # relate the spaCy parts of speech with konspekt tags
                if request.args.get('pos', None) == 'spacykonspekt':
                    new_speech_element.text = speech_dict_POS_tags[lemma.tag_]
                # spaCy Fine-grained part-of-speech.
                # tag_map.py in https://github.com/explosion/spaCy/tree/master/spacy/lang
                if request.args.get('pos', None) == 'spacy':
                    new_speech_element.text = lemma.tag_
                # Coarse-grained part-of-speech from the Universal POS tag set.
                # https://spacy.io/api/annotation#pos-tagging
                if request.args.get('pos', None) == 'ud':
                    new_speech_element.text = lemma.pos_
                # default Coarse-grained part-of-speech from the Universal POS tag set.
                if request.args.get('pos', None) == None:
                    new_speech_element.text = lemma.pos_
                new_item_element.append(new_speech_element)
                # create and append <pos>
                new_pos_element = ET.Element('pos')
                new_pos_element.text = str(lemma.idx+1)
                new_item_element.append(new_pos_element)

                # create and append <relate> and <rel_type>
                new_rel_type_element = ET.Element('rel_type')
                new_relate_element = ET.Element('relate')
                if lemma.dep_ == 'punct':
                    new_rel_type_element.text = 'K0'
                    new_relate_element.text = '0'
                    new_item_element.append(new_rel_type_element)
                    new_item_element.append(new_relate_element)
                else:
                    new_rel_type_element.text = lemma.dep_
                    new_item_element.append(new_rel_type_element)
                    new_relate_element.text = str(lemma.head.i+1)
                    new_item_element.append(new_relate_element)

                # create and append <group_n>
                new_group_n_element = ET.Element('group_n')
                new_group_n_element.text = '1'
                new_item_element.append(new_group_n_element)

                new_sentence_element.append(new_item_element)
            # create full <parce.xml> file structure
            root_element.append(new_sentence_element)
        return Response(ET.tostring(root_element, encoding='utf8', method='xml'), mimetype='text/xml')
    except Exception as e:
        logging.error(e, exc_info=True)
        return abort(500)
# --------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # default port = 5000
    app.run(host = '0.0.0.0')
