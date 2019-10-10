#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# load tempfile for temporary dir creation
import sys, os, tempfile

import json

# load libraries for NLP pipeline
import spacy

# load misc utils
import uuid
from werkzeug.utils import secure_filename
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# load libraries for string proccessing
import re, string

# load libraries for API proccessing
from flask import Flask, jsonify, flash, request, Response, redirect, url_for, abort, render_template

# A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
from flask_cors import CORS

# python-docx
# https://python-docx.readthedocs.io/en/latest/index.html
from docx import Document

# load libraries for XML proccessing
import xml.etree.ElementTree as ET

ALLOWED_EXTENSIONS = set(['docx']) 

# Load globally spaCy model via package name
# NLP_EN = spacy.load('en_core_web_sm')
NLP_EN_VECTORES = spacy.load('en_core_web_lg')

class JSONResponse(Response):
    default_mimetype = 'application/json'

app = Flask(__name__)
CORS(app)
app.response_class = JSONResponse

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

# Ridge DOCX-templated CV processing into JSON-----------------------------------------------------------
def get_data_from_ridge_docx_into_json(docx_path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    cv_data = {}
    personal_name_cv = {}
    paragraphs_temp = []
    document = Document(docx_path)

    # Personal name extraction
    personal_name_cv['First name'] = document.core_properties.subject.split(' ', 1)[0]
    personal_name_cv['Last name'] = document.core_properties.subject.split(personal_name_cv['First name'] + ' ', 1)[1]
    cv_data['Personal name'] = personal_name_cv

    # First table extraction BIO
    table = document.tables[0]
    bio_data = []
    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)
        # Construct a tuple for this row
        # if contain letters and numbers
        row_data = tuple(x for x in text if re.search(r'[A-Za-z0-9]+', x))
        bio_data.append(row_data)

    # remove an empty tuple(s) from a list of tuples
    bio_data = [t for t in bio_data if t]

    logging.debug(bio_data)

    cv_data['Bio'] = bio_data

    # Key Skills extraction
    paragraphs_temp.append(''.join(document.core_properties.subject))
    for para in document.paragraphs:
        if re.search(r'[A-Za-z0-9]+', para.text):
            text = para.text
            paragraphs_temp.append(''.join(text))
    if 'Work Experience' in paragraphs_temp:
        paragraphs_temp = paragraphs_temp[paragraphs_temp.index('Key Skills')+1:paragraphs_temp.index('Work Experience')]
    if 'Qualifications' in paragraphs_temp:
        paragraphs_temp = paragraphs_temp[paragraphs_temp.index('Key Skills')+1:paragraphs_temp.index('Qualifications')]
    cv_data['Key Skills'] = paragraphs_temp
    json_cv_data = json.dumps(cv_data)

    # return '\n'.join(paragraphs_temp)
    return json_cv_data

# --------------------------------------------------------------------------------------------------------

# Ridge-templated CV (DOCX) processing into XML-------------------------------------------------------------------
def docx_ridge_to_xml(docx_path, flg):
    # Init docx document
    document = Document(docx_path)
    paragraphs_temp = []

    # create root element <Graph>
    root_element_Graph = ET.Element("Graph")
    root_element_Graph.set("nodesize", "10")
    root_element_Graph.set("vspacing", "3")
    root_element_Graph.set("hspacing", "20")
    root_element_Graph.set("padding", "4")
    root_element_Graph.set("guid", "")
    root_element_Graph.set("searchurl", "https://www.google.com.ua/#output=search%26q=###SEARCH###")

    # create <Linkgroups> element
    element_Linkgroups = ET.Element("Linkgroups")
    ET.SubElement(element_Linkgroups, "Group", {"name" : "Default", "color" : "10066329"})

    # create <datagroups> element
    element_datagroups = ET.Element("datagroups")
    # create <datagroup> element as subelements of <datagroups> element
    ET.SubElement(element_datagroups, "datagroup").text = "First Name"
    ET.SubElement(element_datagroups, "datagroup").text = "Last Name"
    ET.SubElement(element_datagroups, "datagroup").text = "Birthday"
    ET.SubElement(element_datagroups, "datagroup").text = "Job Title"
    ET.SubElement(element_datagroups, "datagroup").text = "Location"
    ET.SubElement(element_datagroups, "datagroup").text = "Languages"
    ET.SubElement(element_datagroups, "datagroup").text = "Language"
    ET.SubElement(element_datagroups, "datagroup").text = "Nationality"
    ET.SubElement(element_datagroups, "datagroup").text = "Speak Norwegian"
    ET.SubElement(element_datagroups, "datagroup").text = "Skills"
    ET.SubElement(element_datagroups, "datagroup").text = "Skill"
    ET.SubElement(element_datagroups, "datagroup").text = "Consultancy Firm"

    # create <Edges> element
    element_Edges = ET.Element("Edges")

    # add default edge
    ET.SubElement(element_Edges, "Edge", {"guid" : str(uuid.uuid4()).rpartition('-')[-1], "edgeName" : "", "node1" : document.core_properties.subject, "node2" : "Stuff", "group" : "Default", "istwoway" : "false"})

    # create <Nodes> element
    element_Nodes = ET.Element("Nodes")

    # add default node
    ET.SubElement(element_Nodes, "Node", {"guid" : str(uuid.uuid4()).rpartition('-')[-1], "nodeName" : "Stuff", "nclass" : "", "shape" : "circle", "color" : "13421772", "xPos" : "", "yPos" : "", "font" : "Verdana", "fontsize" : "14"})

    element_Node = ET.Element("Node")
    element_Node.set("guid", str(uuid.uuid4()).rpartition('-')[-1])
    element_Node.set("nodeName", document.core_properties.subject)
    element_Node.set("nclass", "")
    element_Node.set("shape", "square")
    element_Node.set("color", "13421772")
    element_Node.set("xPos", "")
    element_Node.set("yPos", "")
    element_Node.set("Font", "Verdana")
    element_Node.set("fontsize", "14")

    element_Data_Skills = ET.Element("data")
    element_Data_Skills.set("tclass", "Skills")
    element_Data_Skills.set("type", "text")
    element_Data_Skills.set("link", "")

    element_Data_Languages = ET.Element("data")
    element_Data_Languages.set("tclass", "Languages")
    element_Data_Languages.set("type", "text")
    element_Data_Languages.set("link", "")

    # add default node with Ridge value
    ET.SubElement(element_Node, "data", {"tclass": "Consultancy Firm", "type" : "text", "link" : ""}).text = "Ridge"

    # add node with vacancy value
    ET.SubElement(element_Node, "data", {"tclass": "First Name", "type" : "text", "link" : ""}).text = document.core_properties.subject.split(' ', 1)[0]

    ET.SubElement(element_Node, "data", {"tclass": "Last Name", "type" : "text", "link" : ""}).text = document.core_properties.subject.split(document.core_properties.subject.split(' ', 1)[0] + ' ', 1)[1]

    # First table extraction BIO
    table = document.tables[0]
    bio_data = []
    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)
        # Construct a tuple for this row
        # if contain letters and numbers
        row_data = tuple(x for x in text if re.search(r'[A-Za-z0-9]+', x))
        bio_data.append(row_data)
    # remove an empty tuple(s) from a list of tuples
    bio_data = [t for t in bio_data if t]

    for i in bio_data:
        if "Title" in i[0]:
            ET.SubElement(element_Node, "data", {"tclass": "Job Title", "type" : "text", "link" : ""}).text =i[1].strip()
            ET.SubElement(element_Nodes, "Node", {"guid" : str(uuid.uuid4()).rpartition('-')[-1], "nodeName" : i[1], "nclass" : "", "shape" : "circle", "color" : "13421772", "xPos" : "", "yPos" : "", "font" : "Verdana", "fontsize" : "14"})
            ET.SubElement(element_Edges, "Edge", {"guid" : str(uuid.uuid4()).rpartition('-')[-1], "edgeName" : "", "node1" : document.core_properties.subject, "node2" : i[1], "group" : "Default", "istwoway" : "false"})
        if i[0] == "Nationality:":
            ET.SubElement(element_Node, "data", {"tclass": "Nationality", "type" : "text", "link" : ""}).text = i[1]
        if i[0] == "Languages:":
            # ET.SubElement(element_Node, "data", {"tclass": "Languages", "type" : "text", "link" : ""}).text = i[1]
            element_Data_Languages.text = i[1]
            for lang in i[1].split(','):
                ET.SubElement(element_Data_Languages, "data", {"tclass": "Language", "type" : "text", "link" : ""}).text = lang.strip()
            element_Node.append(element_Data_Languages)
        if i[0] == "Date of Birth:":
            ET.SubElement(element_Node, "data", {"tclass": "Birthday", "type" : "text", "link" : ""}).text = i[1]
        if i[0] == "Location:":
            ET.SubElement(element_Node, "data", {"tclass": "Location", "type" : "text", "link" : ""}).text = i[1]
        if '\n' in i[0]:
            list_bio_temp_left = i[0].split("\n", 1)
            list_bio_temp_right = i[1].split("\n", 1)
            for j in list_bio_temp_left:
                if 'Date of Birth' in j:
                    ET.SubElement(element_Node, "data", {"tclass": "Birthday", "type" : "text", "link" : ""}).text = list_bio_temp_right[list_bio_temp_left.index(j)]
                if 'Year of Birth' in j:
                    ET.SubElement(element_Node, "data", {"tclass": "Birthday", "type" : "text", "link" : ""}).text = list_bio_temp_right[list_bio_temp_left.index(j)]
                if 'Location' in j:
                    ET.SubElement(element_Node, "data", {"tclass": "Location", "type" : "text", "link" : ""}).text = list_bio_temp_right[list_bio_temp_left.index(j)]
                if 'Nationality' in j:
                    ET.SubElement(element_Node, "data", {"tclass": "Nationality", "type" : "text", "link" : ""}).text = list_bio_temp_right[list_bio_temp_left.index(j)]
                if 'Languages' in j:
                    # ET.SubElement(element_Node, "data", {"tclass": "Languages", "type" : "text", "link" : ""}).text = list_bio_temp_right[list_bio_temp_left.index(j)]
                    element_Data_Languages.text = list_bio_temp_right[list_bio_temp_left.index(j)]
                    for lang in list_bio_temp_right[list_bio_temp_left.index(j)].split(','):
                        ET.SubElement(element_Data_Languages, "data", {"tclass": "Language", "type" : "text", "link" : ""}).text = lang.strip()
                    element_Node.append(element_Data_Languages)

    # Key Skills extraction
    for para in document.paragraphs:
        if re.search(r'[A-Za-z0-9]+', para.text):
            text = para.text
            paragraphs_temp.append(''.join(text))
    if 'Work Experience' in paragraphs_temp:
        if 'Key Strengths' in paragraphs_temp:
            paragraphs_temp = paragraphs_temp[paragraphs_temp.index('Key Strengths')+1 : paragraphs_temp.index('Work Experience')]
            # ET.SubElement(element_Node, "data", {"tclass": "Skills", "type" : "text", "link" : ""}).text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            element_Data_Skills.text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            for temp in paragraphs_temp:
                ET.SubElement(element_Data_Skills, "data", {"tclass": "Skill", "type" : "text", "link" : ""}).text = temp
            element_Node.append(element_Data_Skills)
        if 'Key Skills' in paragraphs_temp:
            paragraphs_temp = paragraphs_temp[paragraphs_temp.index('Key Skills')+1 : paragraphs_temp.index('Work Experience')]
            # ET.SubElement(element_Node, "data", {"tclass": "Skills", "type" : "text", "link" : ""}).text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            element_Data_Skills.text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            for temp in paragraphs_temp:
                ET.SubElement(element_Data_Skills, "data", {"tclass": "Skill", "type" : "text", "link" : ""}).text = temp
            element_Node.append(element_Data_Skills)
    if 'Qualifications' in paragraphs_temp:
        if 'Key Strengths' in paragraphs_temp:
            paragraphs_temp = paragraphs_temp[paragraphs_temp.index('Key Strengths')+1 : paragraphs_temp.index('Qualifications')]
            # ET.SubElement(element_Node, "data", {"tclass": "Skills", "type" : "text", "link" : ""}).text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            element_Data_Skills.text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            for temp in paragraphs_temp:
                ET.SubElement(element_Data_Skills, "data", {"tclass": "Skill", "type" : "text", "link" : ""}).text = temp
            element_Node.append(element_Data_Skills)
        if 'Key Skills' in paragraphs_temp:
            paragraphs_temp = paragraphs_temp[paragraphs_temp.index('Key Skills')+1 : paragraphs_temp.index('Qualifications')]
            # ET.SubElement(element_Node, "data", {"tclass": "Skills", "type" : "text", "link" : ""}).text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            element_Data_Skills.text = re.sub('\s\s+', ' ', ' '.join(paragraphs_temp))
            for temp in paragraphs_temp:
                ET.SubElement(element_Data_Skills, "data", {"tclass": "Skill", "type" : "text", "link" : ""}).text = temp
            element_Node.append(element_Data_Skills)

    element_Nodes.append(element_Node)
    root_element_Graph.append(element_Nodes)
    root_element_Graph.append(element_Edges)
    root_element_Graph.append(element_Linkgroups)
    root_element_Graph.append(element_datagroups)

    if flg:
        return ET.tostring(root_element_Graph, encoding='utf8', method='xml')
    else:
        return root_element_Graph

# --------------------------------------------------------------------------------------------------------

# Free-templated CV (DOCX) processing --------------------------------------------------------------------
def get_data_from_free_docx(docx_path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    paragraphs = []
    document = Document(docx_path)
    logging.debug(document.core_properties.subject)

    paragraphs.append(''.join(document.core_properties.subject))
    for para in document.paragraphs:
        text = para.text
        paragraphs.append(''.join(text))
    return '\n\n'.join(paragraphs)

"""
# ------------------------------------------------------------------------------------------------------
# """

@app.route('/')
def index():
    return Response(render_template('index.html'), mimetype='text/html')

@app.route('/cvparsing')
def cvparsing():
    return Response(render_template('cvparsing.html'), mimetype='text/html')

@app.route('/cvwe')
def cvwe():
    return Response(render_template('cvwe.html'), mimetype='text/html')

"""
# API ---------------------------------------------------------------------------------------------------
# """

@app.route('/api/cv/ridge/docx/extract/json', methods=['POST'])
def get_data_from_cv_json():
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
        # docx processing
        if file.filename.rsplit('.', 1)[1].lower() == 'docx':
            try:
                docx_file = secure_filename(file.filename)
                destination = "/".join([tempfile.mkdtemp(),docx_file])
                file.save(destination)
                file.close()
                if os.path.isfile(destination):
                    return get_data_from_ridge_docx_into_json(destination)
            except Exception as e:
                logging.error(e, exc_info=True)
            return abort(500)

# --------------------------------------------------------------------------------------------------------

@app.route('/api/cv/ridge/docx/extract/xml', methods=['POST'])
def get_data_from_cv_xml():
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
        try:
            docx_file = secure_filename(file.filename)
            destination = "/".join([tempfile.mkdtemp(),docx_file])
            file.save(destination)
            file.close()
            if os.path.isfile(destination):
                return docx_ridge_to_xml(destination, True)
        except Exception as e:
            logging.error(e, exc_info=True)
        return abort(500)

# --------------------------------------------------------------------------------------------------------

@app.route('/api/cv/multiple/ridge/docx/extract/xml', methods=['POST'])
def get_data_from_cvs_xml():
    uploaded_files = request.files.getlist("file")
    list_xml = []
    xml_final_tree = None

    logging.debug(uploaded_files)

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            # docx processing
            docx_file = secure_filename(file.filename)
            destination = "/".join([tempfile.mkdtemp(),docx_file])
            file.save(destination)
            file.close()
            if os.path.isfile(destination):
                # logging.debug(docx_ridge_to_xml(destination).getchildren())
                list_xml.append(ET.tostring(docx_ridge_to_xml(destination, False), encoding='unicode', method='xml'))
                if xml_final_tree is None:
                    xml_final_tree = docx_ridge_to_xml(destination, False)
                else:
                    for el_Node_old in xml_final_tree.iter('Node'):
                        list_xml.append(el_Node_old.get('nodeName'))
                    # ---------
                    for el_Node in docx_ridge_to_xml(destination, False).iter('Node'):
                        # xml_final_tree.find('Nodes').append(el_Node)
                        if el_Node.get('nodeName') not in list_xml:
                            xml_final_tree.find('Nodes').append(el_Node)
                    for el_Edge in docx_ridge_to_xml(destination, False).iter('Edge'):
                        xml_final_tree.find('Edges').append(el_Edge)
    return ET.tostring(xml_final_tree, encoding='unicode', method='xml')

@app.route('/wv/api/en/similarity', methods=['POST'])
def get_similarity():
    req_data = request.get_json()
    doc1 = NLP_EN_VECTORES(req_data['text1'])
    doc2 = NLP_EN_VECTORES(req_data['text2'])
    return jsonify(similarity = doc1.similarity(doc2))

if __name__ == '__main__':
    # default port = 5000
    app.run(host = '0.0.0.0')
    # app.run(host = '127.0.0.1', port = 8000)