#requires Python >= 3.5
import xml.etree.ElementTree
import glob
import os
import re
import string
import sys

prefix = '{http://www.tei-c.org/ns/1.0}'
sentences = ".//{0}s".format(prefix)
segments = ".//{0}seg".format(prefix)

gender_tags = {'m1', 'm2', 'm3', 'f', 'n'}
number_tags = {'pl', 'sg'}
case_tags = {'nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc'}

def remove_nonalpha(string):
    pattern = re.compile('[\W_]+', re.UNICODE)
    return pattern.sub('', string)

def contract_whitespace(string):
    pattern = re.compile('\s+')
    return pattern.sub(' ', string)

def is_num(string):
    roman = ['ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
    return string in roman or any(char.isdigit() for char in string)

def is_valid(line):
    return len(line) > 4 and line.count('num') < 3

def extract_orthographic(segment):
    tag = ".//{0}f[@name='orth']/{0}string".format(prefix)
    orthographic = segment.find(tag).text.lower()
    return remove_nonalpha(orthographic) 

def extract_interpretation(segment):
    interpretation = ".//{0}f[@name='interpretation']/{0}string".format(prefix)
    return segment.find(interpretation).text.lower()
    
def extract_gnc(interpretation):
    gender = next((token for token in interpretation if token in gender_tags), None)
    number = next((token for token in interpretation if token in number_tags), None)
    case = next((token for token in interpretation if token in case_tags), None)
    return ''.join(list(filter(None, [gender, number, case])))

def split_interpretation(interpretation):
    interpretation = interpretation.split(':')
    base = interpretation[0]
    pos = interpretation[1]
    if len(interpretation) < 3:
        gnc = pos
    else:
        gnc = extract_gnc(interpretation)
        if gnc:
            gnc = "{0}:{1}".format(pos, gnc)
        else:
            gnc = pos
    return base, pos, gnc

def append_orth(parsed, interpretation): 
    base, pos, gnc = split_interpretation(interpretation)
    if pos == 'aglt':
        parsed[-1] += orth
    elif pos not in ['brev', 'ign', 'interp', 'xxx']:
        parsed.append(orth)

def get_base(interpretation): 
    base, pos, gnc = split_interpretation(interpretation)
    if pos not in ['brev', 'ign', 'interp', 'xxx', 'aglt']:
        return base

def get_pos(interpretation): 
    base, pos, gnc = split_interpretation(interpretation)
    if pos not in ['brev', 'ign', 'interp', 'xxx']:
        return pos

def get_pos_gnc(interpretation): 
    base, pos, gnc = split_interpretation(interpretation)
    if pos not in ['brev', 'ign', 'interp', 'xxx']:
        return gnc 
    else:
        return ''

def parse_sentence(sentence):
    parsed = []
    for segment in sentence.findall(segments):
        orth = extract_orthographic(segment)
        interpretation =  extract_interpretation(segment)
        if is_num(orth):
            parsed.append('num')
        else:
            parsed.append(get_pos_gnc(interpretation))
    return parsed

def parse(xmlpath, out):
    with open(out, 'a') as out:
        root = xml.etree.ElementTree.parse(filename).getroot()
        for sentence in root.findall(sentences):
            parsed = parse_sentence(sentence)
            if is_valid(parsed):
                parsed = contract_whitespace(' '.join(parsed))
                print(parsed, file=out)

if __name__ == '__main__':
    path = sys.argv[1]
    out= os.path.basename(os.path.normpath(path))
    open(out, 'w').close()
    xmlpath = os.path.join(path, '**/ann_morphosyntax.xml') 
    for filename in glob.iglob(xmlpath, recursive=True):
        try:
            parse(xmlpath, out)
        except Exception as err:
            print(err)
            continue
