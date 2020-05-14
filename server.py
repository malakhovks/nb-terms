#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# load tempfile for temporary dir creation
import sys, os, tempfile

# load libraries for NLP pipeline
import spacy
# load Visualizers 
from spacy import displacy

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

# load libraries for XML proccessing
import xml.etree.ElementTree as ET

# load libraries for API proccessing
from flask import Flask, jsonify, flash, request, Response, redirect, url_for, abort, render_template

# A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
from flask_cors import CORS

# Load globally spaCy model via package name
NLP_NB = spacy.load('nb_core_news_sm')
# NLP_NB_VECTORES = spacy.load('./tmp/nb_nowac_vectores')
# NLP_EN_VECTORES = spacy.load('en_core_web_lg')

# load SnowballStemmer stemmer from nltk
from nltk.stem.snowball import SnowballStemmer
# Load globally english SnowballStemmer
NORWEGIAN_STEMMER = SnowballStemmer("norwegian")

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

"""
# ------------------------------------------------------------------------------------------------------
# """

""" @app.route('/')
def index():
    return Response(render_template('index.html'), mimetype='text/html')

@app.route('/ner')
def ner():
    return Response(render_template('ner.html'), mimetype='text/html')

@app.route('/cvparsing')
def cvparsing():
    return Response(render_template('cvparsing.html'), mimetype='text/html')

@app.route('/cvwe')
def cvwe():
    return Response(render_template('cvwe.html'), mimetype='text/html') """

"""
# API ---------------------------------------------------------------------------------------------------
# """
# --------------------------------------------------------------------------------------------------------
@app.route('/api/bot/nb/alltermsxml', methods=['POST'])
def get_allterms():
    req_data = request.get_json()
    try:
        # spaCy doc init + default sentence normalization
        doc = NLP_NB(req_data['message'])

        # create the <allterms.xml> file structure
        # create root element <termsintext>
        root_termsintext_element = ET.Element("termsintext")
        # create element <sentences>
        sentences_element = ET.Element("sentences")
        # create element <filepath>
        # filepath_element = ET.Element("filepath")
        # filepath_element.text = file.filename
        # create element <exporterms>
        exporterms_element = ET.Element("exporterms")

        # Helper list for one-word terms
        one_word_terms_help_list = []
        # Helper list for two-word terms
        two_word_terms_help_list = []
        # Helper list for multiple-word terms (from 4-word terms)
        multiple_word_terms_help_list = []

        noun_chunks = []

        # Main text parsing cycle for sentences
        for sentence_index, sentence in enumerate(doc.sents):
            # default sentence normalization
            sentence_clean = sentence.text
            # create and append <sent>
            new_sent_element = ET.Element('sent')
            new_sent_element.text = sentence_clean #.encode('ascii', 'ignore') errors='replace'
            sentences_element.append(new_sent_element)
            # for processing specific sentence
            doc_for_chunks = NLP_NB(sentence_clean)
            # sentence NP shallow parsing cycle
            for chunk in doc_for_chunks.noun_chunks:
                doc_for_tokens = NLP_NB(chunk.text)
                '''
                # EXTRACT ONE-WORD TERMS ----------------------------------------------------------------------
                '''
                if len(doc_for_tokens) == 1:

                    if doc_for_tokens[0].pos_ in ['NOUN', 'PROPN']:

                        if doc_for_tokens[0].lemma_ in one_word_terms_help_list:
                            for term in exporterms_element.findall('term'):
                                if term.find('tname').text == doc_for_tokens[0].lemma_:
                                    new_sentpos_element = ET.Element('sentpos')
                                    new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                                    term.append(new_sentpos_element)

                        if doc_for_tokens[0].lemma_ not in one_word_terms_help_list:

                            one_word_terms_help_list.append(doc_for_tokens[0].lemma_)
                            # create and append <wcount>
                            new_wcount_element = ET.Element('wcount')
                            new_wcount_element.text = '1'
                            # create and append <ttype>
                            new_ttype_element = ET.Element('ttype')
                            new_ttype_element.text = doc_for_tokens[0].pos_
                            # create <term>
                            new_term_element = ET.Element('term')
                            # create and append <tname>
                            new_tname_element = ET.Element('tname')
                            new_tname_element.text = doc_for_tokens[0].lemma_
                            # create and append <osn>
                            new_osn_element = ET.Element('osn')
                            new_osn_element.text = NORWEGIAN_STEMMER.stem(doc_for_tokens[0].text)

                            # create and append <sentpos>
                            new_sentpos_element = ET.Element('sentpos')
                            new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                            new_term_element.append(new_sentpos_element)

                            # append to <term>
                            new_term_element.append(new_ttype_element)
                            new_term_element.append(new_tname_element)
                            new_term_element.append(new_osn_element)
                            new_term_element.append(new_wcount_element)

                            # append to <exporterms>
                            exporterms_element.append(new_term_element)

                if len(doc_for_tokens) == 2:

                    '''
                    # Extract one-word terms from 2-words statements (excluding articles DET)
                    '''
                    if doc_for_tokens[0].pos_ in ['DET', 'PUNCT']:

                        if doc_for_tokens[1].lemma_ in one_word_terms_help_list:
                            for term in exporterms_element.findall('term'):
                                if term.find('tname').text == doc_for_tokens[1].lemma_:
                                    new_sentpos_element = ET.Element('sentpos')
                                    new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+2)
                                    term.append(new_sentpos_element)

                        if doc_for_tokens[1].lemma_ not in one_word_terms_help_list:

                            one_word_terms_help_list.append(doc_for_tokens[1].lemma_)
                            # create and append <wcount>
                            new_wcount_element = ET.Element('wcount')
                            new_wcount_element.text = '1'
                            # create and append <ttype>
                            new_ttype_element = ET.Element('ttype')
                            new_ttype_element.text = doc_for_tokens[1].pos_
                            # create <term>
                            new_term_element = ET.Element('term')
                            # create and append <tname>
                            new_tname_element = ET.Element('tname')
                            new_tname_element.text = doc_for_tokens[1].lemma_
                            # create and append <osn>
                            new_osn_element = ET.Element('osn')
                            new_osn_element.text = NORWEGIAN_STEMMER.stem(doc_for_tokens[1].text)

                            # create and append <sentpos>
                            new_sentpos_element = ET.Element('sentpos')
                            new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+2)
                            new_term_element.append(new_sentpos_element)

                            # append to <term>
                            new_term_element.append(new_ttype_element)
                            new_term_element.append(new_tname_element)
                            new_term_element.append(new_osn_element)
                            new_term_element.append(new_wcount_element)

                            # append to <exporterms>
                            exporterms_element.append(new_term_element)

                    '''
                    # EXTRACT TWO-WORD TERMS ---------------------------------------------------------------
                    '''
                    if doc_for_tokens[0].pos_ not in ['DET', 'PUNCT']:

                        # print('two-word term lemma ---> ' + chunk.lemma_ +' POS[0]:'+ doc_for_tokens[0].pos_ + ' POS[0]:'+ doc_for_tokens[0].tag_ + ' HEAD[0]:' + doc_for_tokens[0].head.lower_ +' POS[1]:' + doc_for_tokens[1].pos_ + ' POS[1]:'+ doc_for_tokens[1].tag_ + ' HEAD[1]:' + doc_for_tokens[1].head.lower_)

                        # print('--------------------')

                        # If two-word term already exists in two_word_terms_help_list
                        # if chunk.lower_ in two_word_terms_help_list:
                        if chunk.lemma_ in two_word_terms_help_list:

                            # add new <sentpos> for existing two-word term
                            for term in exporterms_element.findall('term'):
                                # if term.find('tname').text == chunk.lower_:
                                if term.find('tname').text == chunk.lemma_:
                                    new_sentpos_element = ET.Element('sentpos')
                                    new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                                    term.append(new_sentpos_element)

                            # Check If root (root of Noun chunks always is a NOUN) of the two-word term
                            # already exists in one_word_terms_help_list
                            if chunk.root.lemma_ in one_word_terms_help_list:

                                sent_pos_helper = []

                                for relup_index, one_term in enumerate(exporterms_element.findall('term')):

                                    if one_term.find('tname').text == chunk.root.lemma_:

                                        for sent_pos in one_term.findall('sentpos'):
                                            sent_pos_helper.append(sent_pos.text)

                                        # create and append new <sentpos>
                                        # check if new <sentpos> already exist, if no then add new <sentpos>
                                        if chunk.root.lower_ == doc_for_tokens[0].lower_:
                                            if (str(sentence_index) + '/' + str(chunk.start+1)) not in sent_pos_helper:
                                                new_sentpos_element = ET.Element('sentpos')
                                                new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                                                one_term.append(new_sentpos_element)
                                        else:
                                            if (str(sentence_index) + '/' + str(chunk.start+2)) not in sent_pos_helper:
                                                new_sentpos_element = ET.Element('sentpos')
                                                new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+2)
                                                one_term.append(new_sentpos_element)

                            # Check If child of the root (Child not always be a NOUN, so not always be a term) of the two-word term
                            # already exists in one_word_terms_help_list
                            for t in doc_for_tokens:
                                    if t.lemma_ != chunk.root.lemma_:
                                        # if child of the root is NOUN, so it is a term
                                        if t.pos_ in ['NOUN']:
                                            if t.lemma_ in one_word_terms_help_list:

                                                sent_pos_helper = []
                                                if t.i == 0:
                                                    index_helper = chunk.start+1
                                                else:
                                                    index_helper = chunk.start+2

                                                for relup_index, one_term in enumerate(exporterms_element.findall('term')):

                                                    if one_term.find('tname').text == t.lemma_:

                                                        for sent_pos in one_term.findall('sentpos'):
                                                            sent_pos_helper.append(sent_pos.text)

                                                        if (str(sentence_index) + '/' + str(index_helper)) not in sent_pos_helper:
                                                                new_sentpos_element = ET.Element('sentpos')
                                                                new_sentpos_element.text = str(sentence_index) + '/' + str(index_helper)
                                                                one_term.append(new_sentpos_element)


                        # If two-word term not exists in two_word_terms_help_list
                        if chunk.lemma_ not in two_word_terms_help_list:

                            # update two_word_terms_help_list with the new two-word term
                            # two_word_terms_help_list.append(chunk.lower_)
                            two_word_terms_help_list.append(chunk.lemma_)

                            # create and append <wcount>
                            new_wcount_element = ET.Element('wcount')
                            new_wcount_element.text = '2'
                            # create and append <ttype>
                            new_ttype_element = ET.Element('ttype')
                            new_ttype_element.text = doc_for_tokens[0].pos_ + '_' + doc_for_tokens[1].pos_
                            # create <term>
                            new_term_element = ET.Element('term')
                            # create and append <tname>
                            new_tname_element = ET.Element('tname')
                            # new_tname_element.text = chunk.lower_
                            new_tname_element.text = chunk.lemma_
                            # create and append <osn>
                            new_osn_element = ET.Element('osn')
                            new_osn_element.text = NORWEGIAN_STEMMER.stem(doc_for_tokens[0].text)
                            new_term_element.append(new_osn_element)
                            new_osn_element = ET.Element('osn')
                            new_osn_element.text = NORWEGIAN_STEMMER.stem(doc_for_tokens[1].text)
                            new_term_element.append(new_osn_element)
                            # create and append <sentpos>
                            new_sentpos_element = ET.Element('sentpos')
                            new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                            new_term_element.append(new_sentpos_element)

                            # append to <term>
                            new_term_element.append(new_ttype_element)
                            new_term_element.append(new_tname_element)
                            new_term_element.append(new_wcount_element)

                            # append to <exporterms>
                            exporterms_element.append(new_term_element)

                            # Check If root (root of Noun chunks always is a NOUN) of the two-word term
                            # already exists in one_word_terms_help_list
                            # add relup/reldown
                            if chunk.root.lemma_ in one_word_terms_help_list:

                                sent_pos_helper = []

                                for relup_index, one_term in enumerate(exporterms_element.findall('term')):

                                    if one_term.find('tname').text == chunk.root.lemma_:

                                        for sent_pos in one_term.findall('sentpos'):
                                            sent_pos_helper.append(sent_pos.text)

                                        if chunk.root.lower_ == doc_for_tokens[0].lower_:
                                            if (str(sentence_index) + '/' + str(chunk.start+1)) not in sent_pos_helper:
                                                new_sentpos_element = ET.Element('sentpos')
                                                new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                                                one_term.append(new_sentpos_element)
                                        else:
                                            if (str(sentence_index) + '/' + str(chunk.start+2)) not in sent_pos_helper:
                                                new_sentpos_element = ET.Element('sentpos')
                                                new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+2)
                                                one_term.append(new_sentpos_element)

                                        for reldown_index, two_term in enumerate(exporterms_element.findall('term')):

                                            # if two_term.find('tname').text == chunk.lower_:
                                            if two_term.find('tname').text == chunk.lemma_:
                                                new_relup_element = ET.Element('relup')
                                                new_relup_element.text = str(relup_index)
                                                two_term.append(new_relup_element)
                                                new_reldown_element = ET.Element('reldown')
                                                new_reldown_element.text = str(reldown_index)
                                                one_term.append(new_reldown_element)

                            # Check If root NOUN not exists in one_word_terms_help_list
                            # add root NOUN to one_word_terms_help_list
                            # add relup/reldown
                            if chunk.root.lemma_ not in one_word_terms_help_list:

                                # print('root NOUN not exists in one_word_terms_help_list --->> ' + chunk.root.lemma_)
                                # print('--------------------')

                                one_word_terms_help_list.append(chunk.root.lemma_)

                                # create and append <wcount>
                                new_wcount_element = ET.Element('wcount')
                                new_wcount_element.text = '1'
                                # create and append <ttype>
                                new_ttype_element = ET.Element('ttype')
                                new_ttype_element.text = 'NOUN'
                                # create <term>
                                new_term_element = ET.Element('term')
                                # create and append <tname>
                                new_tname_element = ET.Element('tname')
                                new_tname_element.text = chunk.root.lemma_
                                # create and append <osn>
                                new_osn_element = ET.Element('osn')
                                new_osn_element.text = NORWEGIAN_STEMMER.stem(chunk.root.lower_)
                                # create and append <sentpos>
                                new_sentpos_element = ET.Element('sentpos')
                                if chunk.root.lower_ == doc_for_tokens[0].lower_:
                                    new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                                else:
                                    new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+2)
                                new_term_element.append(new_sentpos_element)
                                # append to <term>
                                new_term_element.append(new_ttype_element)
                                new_term_element.append(new_tname_element)
                                new_term_element.append(new_wcount_element)

                                # append to <exporterms>
                                exporterms_element.append(new_term_element)

                                for relup_index, one_term in enumerate(exporterms_element.findall('term')):

                                    if one_term.find('tname').text == chunk.root.lemma_:
                                        for reldown_index, two_term in enumerate(exporterms_element.findall('term')):

                                            # if two_term.find('tname').text == chunk.lower_:
                                            if two_term.find('tname').text == chunk.lemma_:
                                                new_relup_element = ET.Element('relup')
                                                new_relup_element.text = str(relup_index)
                                                two_term.append(new_relup_element)
                                                new_reldown_element = ET.Element('reldown')
                                                new_reldown_element.text = str(reldown_index)
                                                one_term.append(new_reldown_element)

                            for t in doc_for_tokens:
                                    if t.lemma_ != chunk.root.lemma_:
                                        if t.pos_ in ['NOUN']:

                                            # print('-------->>>>>>' + t.lemma_)

                                            if t.lemma_ in one_word_terms_help_list:

                                                sent_pos_helper = []
                                                if t.i == 0:
                                                    index_helper = chunk.start+1
                                                else:
                                                    index_helper = chunk.start+2


                                                for relup_index, one_term in enumerate(exporterms_element.findall('term')):

                                                    if one_term.find('tname').text == t.lemma_:
                                                        for reldown_index, two_term in enumerate(exporterms_element.findall('term')):

                                                            # if two_term.find('tname').text == chunk.lower_:
                                                            if two_term.find('tname').text == chunk.lemma_:

                                                                for sent_pos in one_term.findall('sentpos'):
                                                                    sent_pos_helper.append(sent_pos.text)

                                                                if (str(sentence_index) + '/' + str(index_helper)) not in sent_pos_helper:
                                                                    new_sentpos_element = ET.Element('sentpos')
                                                                    new_sentpos_element.text = str(sentence_index) + '/' + str(index_helper)
                                                                    one_term.append(new_sentpos_element)

                                                                new_relup_element = ET.Element('relup')
                                                                new_relup_element.text = str(relup_index)
                                                                two_term.append(new_relup_element)
                                                                new_reldown_element = ET.Element('reldown')
                                                                new_reldown_element.text = str(reldown_index)
                                                                one_term.append(new_reldown_element)

                                            if t.lemma_ not in one_word_terms_help_list:

                                                # print('if t.lemma_ not in one_word_terms_help_list ----->>>>>>' + t.lemma_)

                                                sent_pos_helper = []

                                                if t.i == 0:
                                                    index_helper = chunk.start+1
                                                else:
                                                    index_helper = chunk.start+2

                                                one_word_terms_help_list.append(t.lemma_)

                                                # create and append <wcount>
                                                new_wcount_element = ET.Element('wcount')
                                                new_wcount_element.text = '1'
                                                # create and append <ttype>
                                                new_ttype_element = ET.Element('ttype')
                                                new_ttype_element.text = 'NOUN'
                                                # create <term>
                                                new_term_element = ET.Element('term')
                                                # create and append <tname>
                                                new_tname_element = ET.Element('tname')
                                                new_tname_element.text = t.lemma_
                                                # create and append <osn>
                                                new_osn_element = ET.Element('osn')
                                                new_osn_element.text = NORWEGIAN_STEMMER.stem(t.lower_)
                                                # create and append <sentpos>
                                                new_sentpos_element = ET.Element('sentpos')
                                                new_sentpos_element.text = str(sentence_index) + '/' + str(index_helper)
                                                # append to <term>
                                                new_term_element.append(new_sentpos_element)
                                                new_term_element.append(new_ttype_element)
                                                new_term_element.append(new_tname_element)
                                                new_term_element.append(new_wcount_element)

                                                # append to <exporterms>
                                                exporterms_element.append(new_term_element)

                                                for relup_index, one_term in enumerate(exporterms_element.findall('term')):

                                                    if one_term.find('tname').text == t.lemma_:
                                                        for reldown_index, two_term in enumerate(exporterms_element.findall('term')):

                                                            # if two_term.find('tname').text == chunk.lower_:
                                                            if two_term.find('tname').text == chunk.lemma_:

                                                                for sent_pos in one_term.findall('sentpos'):
                                                                    sent_pos_helper.append(sent_pos.text)

                                                                if (str(sentence_index) + '/' + str(index_helper)) not in sent_pos_helper:
                                                                    new_sentpos_element = ET.Element('sentpos')
                                                                    new_sentpos_element.text = str(sentence_index) + '/' + str(index_helper)
                                                                    one_term.append(new_sentpos_element)

                                                                new_relup_element = ET.Element('relup')
                                                                new_relup_element.text = str(relup_index)
                                                                two_term.append(new_relup_element)
                                                                new_reldown_element = ET.Element('reldown')
                                                                new_reldown_element.text = str(reldown_index)
                                                                one_term.append(new_reldown_element)

                '''
                # EXTRACT THREE-WORD TERMS
                '''
                if len(doc_for_tokens) == 3:

                    logging.debug('three-word term lemma ---> ' + chunk.lemma_ +' POS[0]:'+ doc_for_tokens[0].pos_ + ' POS[1]:' + doc_for_tokens[1].pos_ + ' POS[2]:' + doc_for_tokens[2].pos_)
                    logging.debug('--------------------')

                if len(doc_for_tokens) > 3:

                    logging.debug('multi-word term lemma ---> ' + chunk.lemma_)
                    logging.debug('--------------------')

                    if doc_for_tokens[0].pos_ not in ['DET', 'PUNCT']:

                        # If multiple-word term already exists in multiple_word_terms_help_list
                        if chunk.lemma_ in multiple_word_terms_help_list:

                            # add new <sentpos> for existing two-word term
                            for term in exporterms_element.findall('term'):
                                if term.find('tname').text == chunk.lemma_:
                                    new_sentpos_element = ET.Element('sentpos')
                                    new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                                    term.append(new_sentpos_element)
                        
                        # If multiple-word term not exists in multiple_word_terms_help_list
                        if chunk.lemma_ not in multiple_word_terms_help_list:
                            # update  multiple_word_terms_help_list with the new multiple-word term
                            multiple_word_terms_help_list.append(chunk.lemma_)

                            # create and append <wcount>
                            new_wcount_element = ET.Element('wcount')
                            new_wcount_element.text = str(len(chunk))
                            # create and append <ttype>
                            multiple_pos_helper = []
                            for multiple_pos in doc_for_tokens:
                                multiple_pos_helper.append(multiple_pos.pos_)
                            new_ttype_element = ET.Element('ttype')
                            new_ttype_element.text = '_'.join(multiple_pos_helper)
                            # create <term>
                            new_term_element = ET.Element('term')
                            # create and append <tname>
                            new_tname_element = ET.Element('tname')
                            # new_tname_element.text = chunk.lower_
                            new_tname_element.text = chunk.lemma_
                            # create and append <osn>
                            multiple_osn_helper = []
                            for multiple_osn in doc_for_tokens:
                                new_osn_element = ET.Element('osn')
                                new_osn_element.text = NORWEGIAN_STEMMER.stem(multiple_osn.text)
                                new_term_element.append(new_osn_element)
                            # create and append <sentpos>
                            new_sentpos_element = ET.Element('sentpos')
                            new_sentpos_element.text = str(sentence_index) + '/' + str(chunk.start+1)
                            new_term_element.append(new_sentpos_element)

                            # append to <term>
                            new_term_element.append(new_ttype_element)
                            new_term_element.append(new_tname_element)
                            new_term_element.append(new_wcount_element)

                            # append to <exporterms>
                            exporterms_element.append(new_term_element)

        # create full <allterms.xml> file structure
        # root_termsintext_element.append(filepath_element)
        root_termsintext_element.append(exporterms_element)
        root_termsintext_element.append(sentences_element)

        return Response(ET.tostring(root_termsintext_element, encoding='utf8', method='xml'), mimetype='text/xml')

    except Exception as e:
        logging.error(e, exc_info=True)
        return abort(500)

# --------------------------------------------------------------------------------------------------------

@app.route('/api/bot/nb/parcexml', methods=['POST'])
def get_parcexml():
    # POS UD
    # https://universaldependencies.org/u/pos/
    if (request.args.get('pos', None) == 'ud') or (request.args.get('pos', None) == None):
        speech_dict_POS_tags = {'NOUN':'S1', 'ADJ':'S2', 'VERB': 'S4', 'INTJ':'S21', 'PUNCT':'98', 'SYM':'98', 'CONJ':'U', 'NUM':'S7', 'X':'99', 'PRON':'S11', 'ADP':'P', 'PROPN':'S22', 'ADV':'S16', 'AUX':'99', 'CCONJ':'U', 'DET':'99', 'PART':'99', 'SCONJ':'U', 'SPACE':'98'}
    # TODO Correctly relate the parts of speech with spaCy
    # POS spaCy
    if request.args.get('pos', None) == 'spacy':
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
                # create and append <lemma>
                new_lemma_element = ET.Element('lemma')
                new_lemma_element.text = lemma.lemma_ #.encode('ascii', 'ignore')
                new_item_element.append(new_lemma_element)
                # create and append <number>
                new_number_element = ET.Element('number')
                new_number_element.text = str(lemma.i+1)
                new_item_element.append(new_number_element)
                # create and append <speech>
                new_speech_element = ET.Element('speech')
                # relate the universal dependencies parts of speech with konspekt tags
                if (request.args.get('pos', None) == 'ud') or (request.args.get('pos', None) == None):
                    # new_speech_element.text = speech_dict_POS_tags[lemma.pos_]
                    new_speech_element.text = lemma.pos_
                # relate the spaCy parts of speech with konspekt tags
                if request.args.get('pos', None) == 'spacy':
                    # new_speech_element.text = speech_dict_POS_tags[lemma.tag_]
                    new_speech_element.text = lemma.tag_
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