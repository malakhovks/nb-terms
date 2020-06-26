import subprocess
# load libraries for string proccessing
import re, string

args = ["./mtag.py", "text.txt"]
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
    found = '' # apply your error handling