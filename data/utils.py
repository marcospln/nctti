import re

# Read data from NCTTI
######################
def read_nct(nct):
    nctti = dict()
    nct_comp = nct['compound']
    nct_class = nct['CompScale']
    nct_type = nct['CompType']
    nct_mean1 = nct['MeanS1']
    nct_mean2 = nct['MeanS2']
    nct_mean3 = nct['MeanS3']
    nct_syn = nct['Synonyms']
    nct_syn1 = nct['SynonymsS1']
    nct_syn2 = nct['SynonymsS2']
    nct_syn3 = nct['SynonymsS3']

    for p,c in enumerate(nct_comp):
        if c not in nctti:
            nctti[c] = dict()

        nctti[c]['class'] = nct_class[p]
        nctti[c]['type'] = nct_type[p]
        nctti[c]['mean1'] = nct_mean1[p]
        nctti[c]['mean2'] = nct_mean2[p]
        nctti[c]['mean3'] = nct_mean3[p]
        nctti[c]['syn'] = nct_syn[p]
        nctti[c]['syn1'] = nct_syn1[p]
        nctti[c]['syn2'] = nct_syn2[p]
        nctti[c]['syn3'] = nct_syn3[p]

    return(nctti)


# Read data from csv
####################
def read_data(nc_ids, lang):
    ncs = nc_ids['compound']
    ids1 = nc_ids['sentence1']
    ids2 = nc_ids['sentence2']
    ids3 = nc_ids['sentence3']

    target_ids = dict()
    compounds = dict()

    for p,n in enumerate(ncs):
        n = n.lower()
        if n not in compounds:
            compounds[n] = dict()

        # Sentence 1
        if re.search('^sent[123]:', ids1[p]):
            if lang == 'en':
                docid, numsent = ids1[p].split('"\', ')
                numsent = re.sub('\)$', '', numsent)
                docid = re.sub('^sent.: \(\'"', '', docid)
            elif lang == 'pt':
                docid, numsent = ids1[p].split('"\'], ')
                numsent = re.sub('\)$', '', numsent)
                docid = re.sub('^sent.: \(\[\'# MWETOOLKIT: meta.doc.id="([^\"]+)"\',.+$', r'# MWETOOLKIT: meta.doc.id="\1"', docid)

            if docid not in target_ids:
                target_ids[docid] = (n, numsent, 'sent1')
            else:
                tup1 = target_ids[docid]
                tup2 = (n, numsent, 'sent1')
                target_ids[docid] = [tup1, tup2]
        else:
            compounds[n]['sent1'] = ids1[p]

        # Sentence 2
        if re.search('^sent[123]:', ids2[p]):
            if lang == 'en':
                docid, numsent = ids2[p].split('"\', ')
                numsent = re.sub('\)$', '', numsent)
                docid = re.sub('^sent.: \(\'"', '', docid)
            elif lang == 'pt':
                docid, numsent = ids2[p].split('"\'], ')
                numsent = re.sub('\)$', '', numsent)
                docid = re.sub('^sent.: \(\[\'# MWETOOLKIT: meta.doc.id="([^\"]+)"\',.+$', r'# MWETOOLKIT: meta.doc.id="\1"', docid)

            if docid not in target_ids:
                target_ids[docid] = (n, numsent, 'sent2')
            else:
                tup1 = target_ids[docid]
                tup2 = (n, numsent, 'sent2')
                target_ids[docid] = [tup1, tup2]
        else:
            compounds[n]['sent2'] = ids2[p]

        # Sentence 3
        if re.search('^sent[123]:', ids3[p]):
            if lang == 'en':
                docid, numsent = ids3[p].split('"\', ')
                numsent = re.sub('\)$', '', numsent)
                docid = re.sub('^sent.: \(\'"', '', docid)
            elif lang == 'pt':
                docid, numsent = ids3[p].split('"\'], ')
                numsent = re.sub('\)$', '', numsent)
                docid = re.sub('^sent.: \(\[\'# MWETOOLKIT: meta.doc.id="([^\"]+)"\',.+$', r'# MWETOOLKIT: meta.doc.id="\1"', docid)

            if docid not in target_ids:
                target_ids[docid] = (n, numsent, 'sent3')
            else:
                tup1 = target_ids[docid]
                tup2 = (n, numsent, 'sent3')
                target_ids[docid] = [tup1, tup2]
        else:
            compounds[n]['sent3'] = ids3[p]

    return(target_ids, compounds)


# Read Portuguese data from .conll file
#######################################
def read_pt_corpus(target_ids, compounds, corpf):
    with open(corpf, 'r') as f:
        search = 0
        sent=''
        pos = 0
        for l in f:
            l = l.rstrip()
            if l in target_ids:
                target = l
                sents = dict()
                search = 1
            if search == 1:
                if re.search('^[0-9]', l):
                    if re.search('^1\t', l):
                        pos+=1
                        if len(sent)>0:
                            sents[pos] = sent
                        sent = l.split('\t')[1].replace('=', ' ')
                    else:
                        sent = sent + ' ' + l.split('\t')[1].replace('=', ' ')
                if l.startswith('# MWETOOLKIT: meta.doc.id') and l not in target_ids:
                    if len(target_ids[target]) == 3:
                        compounds[target_ids[target][0]][target_ids[target][2]] = sents[int(target_ids[target][1])]
                    elif len(target_ids[target]) == 2:
                        compounds[target_ids[target][0][0]][target_ids[target][0][2]] = sents[int(target_ids[target][0][1])]
                        compounds[target_ids[target][1][0]][target_ids[target][1][2]] = sents[int(target_ids[target][1][1])]
                    search = 0
                    pos = 0

    return(compounds)


# Read English data from .xml file
##################################
def read_en_corpus(target_ids, compounds, corpf):
    with open(corpf, 'r', errors='ignore') as f:
        search = 0
        sent=''
        sents = dict()
        pos = 0
        for l in f:
            l = l.rstrip()
            if l.startswith('<text id='):
                pos = 0
                url = l.replace('<text id="', '').replace('">', '')
                if url in target_ids:
                    target = url
                    search = 1
            if search == 1:
                if l.startswith('<s>'):
                    pos+=1
                elif l.startswith('</s>'):
                    sents[pos] = sent
                    sent = ''
                elif not l.startswith('<'):
                    sent = sent + ' ' + l.split('\t')[0].lower()
            if l.startswith('<text id=') and len(sents)>0:
                if len(target_ids[target]) == 3:
                    compounds[target_ids[target][0]][target_ids[target][2]] = sents[int(target_ids[target][1])]
                elif len(target_ids[target]) == 2:
                    compounds[target_ids[target][0][0]][target_ids[target][0][2]] = sents[int(target_ids[target][0][1])]
                    compounds[target_ids[target][1][0]][target_ids[target][1][2]] = sents[int(target_ids[target][1][1])]
                search = 0
                sents = dict()

    return(compounds)
