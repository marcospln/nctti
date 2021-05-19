Noun Compound Type and Token Idiomaticity Dataset
-------------------------------------------------

This repository includes information about how to generate the Noun Compound Type and Token Idiomaticity (NCTTI) dataset, which contains noun compounds (NCs) in English and Portuguese with the following information (provided by annotators):

  * Type-level compositionality scores (from Cordeiro _et al._, 2019 and Reddy _et al.,_ 2011).
  * Token-level compositionality scores in three sentences.
  * Suggestions of paraphrases classified at type-level (for the three sentences) or token-level (for each sentence).

The NCTTI dataset has data for 280 and 180 noun compounds in English and Portuguese, respectively, with different degrees of idiomaticity. For each compound, it contains 3 naturalistic sentences obtained from corpora. Due to copyright restrictions we do not release all the original sentences. Instead, we include a script to obtain them from the ukWaC (Baroni _et al._, 2009) and brWaC (Wagner Filho _et al._, 2018) corpora (see below).

## Obtaining the sentences

### Requirements
 * Python 3
 * Pandas
 * [ukWaC](https://wacky.sslmit.unibo.it/doku.php?id=download) corpus in XML format (tagged). The 25 files (UKWAC-1.xml to UKWAC-25.xml) should be concatenated into a single one (e.g., `cat UKWAC*xml > UKWAC_full.xml`).
 * [brWaC](https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC) corpus in .conll format (single file `brwac.conll`)

### Building the corpus
Use the script `build_dataset.py` to create the English and Portuguese datasets:

`python3 build_dataset.py --lang en --corpus UKWAC_full.xml`

`python3 build_dataset.py --lang pt --corpus brwac.conll`

This should create the `NCTTI_en.tsv` and `NCTTI_pt.tsv` files, respectively.

## NCTTI dataset
The dataset is splitted in two TSV (tab-separated values) files, one per language, with the following information:

  * Compound: the noun compound.
  * Compositionality Class: its compositionality class (Compositional, Non-Compositional, or Partly Compositional)
  * Compositionality Type: compositionality score at type level (from Cordeiro _et al._, 2019 and Reddy _et al.,_ 2011).
  * Compositionality S1: mean compositionality score in sentence 1.
  * Compositionality S2: mean compositionality score in sentence 2.
  * Compositionality S3: mean compositionality score in sentence 3.
  * Sentence 1: sentence 1.
  * Sentence 2: sentence 2.
  * Sentence 3: sentence 3.
  * Synonyms Type: suggestions of paraphrases at type-level (provided for the three sentences).
  * Synonyms S1: suggestions of paraphrases for the first sentence.
  * Synonyms S2: suggestions of paraphrases for the second sentence.
  * Synonyms S3: suggestions of paraphrases for the third sentence.

## Citation
If you use this resource, please cite the following paper:

  * Garcia, Marcos, Tiago Kramer Vieira, Carolina Scarton, Marco Idiart and Aline Villavicencio. 2021. Assessing the Representations of Idiomaticity in Vector Models with a Noun Compound Dataset Labeled at Type and Token Levels. In _Proceedings of the Joint Conference of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (ACL-IJCNLP 2021)_ (forthcoming).

## References
Baroni, Marco, Silvia Bernardini, Adriano Ferraresi and Eros Zanchetta. 2009. The WaCky wide web: a collection of very large linguistically processed web-crawled corpora. _Language resources and evaluation_, 43(3), 209-226.

Cordeiro, Silvio, Aline Villavicencio, Marco Idiart and Carlos Ramisch. 2019. Unsupervised compositionality prediction of nominal compounds. _Computational Linguistics_, 45(1):1–57.

Reddy, Siva, Diana McCarthy and Suresh Manandhar. 2011. An empirical study on compositionality in compound nouns. In _Fifth International Joint Conference on Natural Language Processing_, IJCNLP 2011, Chiang Mai, Thailand, November 8-13, 2011, pages 210–218. The Association for Computer Linguistics.

Wagner Filho, Jorge Alberto, Rodrigo Wilkens, Marco Idiart and Aline Villavicencio. 2019. The brWaC Corpus: A New Open Resource for Brazilian Portuguese. In _Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)_. ELRA.
