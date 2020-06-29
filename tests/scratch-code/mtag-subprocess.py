import subprocess
# load libraries for string proccessing
import re, string
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

""" args = ["./mtag.py", "text.txt"]
process = subprocess.Popen(args, stdout=subprocess.PIPE)

data = process.communicate()
out = re.sub('[\t]', '', data[0])
out = out.split('\n')[1]

try:
    lemma = re.search(r'\"(.*)\"', out).group(1)
    second_part = re.search(r'\<\+(.*)\>', out).group(1)
    first_part = re.search(r'(.*)' + second_part, lemma).group(1)
    print(lemma)
    print(first_part)
    print(second_part)
except AttributeError:
    # AAA, ZZZ not found in the original string
    found = '' # apply your error handling """

""" args = ["./mtag.py", "-wxml", "input.txt", "-o", "output.txt"]
try:
    code = subprocess.call(args, stdout=subprocess.DEVNULL)
    if code == 0:
        print("subprocess.call Success!")
    else:
        print("subprocess.call Error!")
except OSError as e:
    print(e) """

destination_input_text_for_mtag = './input.txt'
destination_output_text_for_mtag = './output.txt'
try:
    with open(destination_input_text_for_mtag, 'w') as f:
        f.write('formuesskatten' + ' . ' + 'formuesskatt')
except IOError as e:
    logging.error(e, exc_info=True)

# args = ["./mtag.py", "-wxml", destination_input_text_for_mtag, "-o", destination_output_text_for_mtag]
args = ["./mtag.py", destination_input_text_for_mtag, "-o", destination_output_text_for_mtag]

try:
    code = subprocess.call(args, stdout=subprocess.DEVNULL)
    if code == 0:
        logging.debug("subprocess.call Success!")
    else:
        logging.error("subprocess.call Error!")
except OSError as e:
    logging.error(e, exc_info=True)

try:
    with open(destination_output_text_for_mtag) as f:
        # out = f.read().splitlines(True)
        data = f.read()
except IOError as e:
    logging.error(e, exc_info=True)

logging.debug(data)

if data == '':
    logging.debug('Error while processing Word <' + 'lemma.text' + '>. Maybe spell error.')
else:
    out = re.sub('[\t]', '', data)
    out_1 = out.split('\n')[1]
    out_n = out.split('\n')[out.split('\n').index('"." symb') + 2]
    logging.debug('out_n: ' + out_n)