#!/usr/bin/python3

# Obtains sentences with copyright from the ukWac and brWaC corpus to build the NCTTI datasets

import sys
import re
import os.path
from argparse import ArgumentParser
import pandas as pd

from data.utils import read_nct, read_data, read_en_corpus, read_pt_corpus

arg_parser = ArgumentParser(
    description='This script constructs the English and/or Portuguese versions of the NCTTI dataset. It requires the ukWaC and/or brWaC corpora to get the sentences with copyright from them.'
)

arg_parser.add_argument(
    '--lang',
    '-l',
    type=str,
    choices=['en', 'pt'],
    help='Language of the dataset: English (en) or Portuguese (pt)',
    required=True,
    default=None
)

arg_parser.add_argument(
    '--corpus',
    '-c',
    type=str,
    required=True,
    help='ukWaC/brWaC corpus. brWaC should be in .conll format. UKWAC as a single file concatenating all the XML files.',
    default=None
)

args = arg_parser.parse_args()
lang = args.lang
corpf = args.corpus

# Input file (sentences and IDs)
if lang == 'en':
    inpf = './data/sentids_en.csv'
    inpd = './data/data_en.tsv'
elif lang == 'pt':
    inpf = './data/sentids_pt.csv'
    inpd = './data/data_pt.tsv'

# Read nctti data
nct = pd.read_csv(inpd, sep='\t', keep_default_na=False)
nctti = read_nct(nct)

# Read sentence ids
nc_ids = pd.read_csv(inpf)

# Get target ids and compounds
target_ids, compounds = read_data(nc_ids, lang)

# Reads corpus
if lang == 'en':
    compounds = read_en_corpus(target_ids, compounds, corpf)
elif lang == 'pt':
    compounds = read_pt_corpus(target_ids, compounds, corpf)

# Print head
if lang == 'pt':
    outf = 'NCTTI_pt.tsv'
elif lang == 'en':
    outf = 'NCTTI_en.tsv'

if os.path.exists(outf):
    ans = 'y'
    ans = input('File %s will be overwritten. Proceed? (y/n) [DEFAULT: y]' %outf)
    if ans == 'n' and ans == 'no':
        exit(0)
        
out = open(outf, 'w+')

# Print
out.write('compound\tcomposit_class\tcomposit_type\tcomposit_meanS1\tcomposit_meanS2\tcomposit_meanS\tsentence1\tsentence2\tsentence3\tsynonyms_type\tsynonymsS1\tsynonymsS2\tsynonymsS3\n')
for c in compounds:
    out.write('{}\t{}\t{}\t{}\t{}\t{}\t'.format(c, nctti[c]['class'], nctti[c]['type'],
                                                nctti[c]['mean1'], nctti[c]['mean2'], nctti[c]['mean3']))
    if 'sent1' in compounds[c]:
        out.write('{}\t'.format(compounds[c]['sent1']))
    else:
        out.write('\t')
    if 'sent2' in compounds[c]:
        out.write('{}\t'.format(compounds[c]['sent2']))
    else:
        out.write('\t')
    if 'sent3' in compounds[c]:
        out.write('{}\t'.format(compounds[c]['sent3']))
    else:
        out.write('\t')
    out.write('{}\t{}\t{}\t{}\n'.format(nctti[c]['syn'],
                                        nctti[c]['syn1'], nctti[c]['syn2'], nctti[c]['syn3']))
out.close()
print('Dataset %s created' %outf)
