from nltk.tokenize.punkt import PunktSentenceTokenizer
import re, string, json

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


# result = convert('giancoli_textbook.pdf')
#
# with open('giancoli.txt', 'w') as text_file:
#     text_file.write(result)
#     text_file.close()

with open('giancoli.txt', 'r') as text_file:
    phys = text_file.read()
    text_file.close()
phys = phys.decode('utf-8')
sentence_tokenizer = PunktSentenceTokenizer()
sentences = sentence_tokenizer.tokenize(phys)
bad_indices = []
size = len(sentences)
for i in xrange(size):
    sentence = (sentences[i].encode('ascii','ignore'))
    sentence = sentence.replace('\n', ' ')
    sentence = re.sub(' +',' ',sentence)
    sentence = re.sub(r'\d+', '', sentence)
    sentence = sentence.replace("-"," ")
    exclude = string.punctuation
    sentence = ''.join(ch for ch in sentence if ch not in exclude)
    sentence = re.sub(' +',' ',sentence)
    sentences[i] = sentence
count = 0
for sentence in sentences:
    if sentence == ' ' or sentence == '':
        sentences.pop(count)
    count +=1

with open('physics_textbook_1.json', 'w') as outfile:
    json.dump(sentences, outfile)
