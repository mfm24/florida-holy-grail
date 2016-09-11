# make tf_idf.
# Trains a TfidfVectorizer on the brown corpus.
# also adds the set of words from Monty Python's
# holy grail so we have an occurrence for every word there.
# we also save a pickled monty_python ntlk.Text so we don't
# have to import nltk.books each time...

import nltk.book
import re
from sklearn.feature_extraction.text import TfidfVectorizer

holy_grail_tokens = nltk.book.text6


def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    # MFM modify to replace "' s " with "'s "
    # so that eg that ' s goes to that's
    step7 = step6.replace("' s ", "'s ")
    return step7.strip()

t = TfidfVectorizer(stop_words='english', sublinear_tf=True)
t.fit([untokenize(s) for s in  nltk.corpus.brown.sents()] + list(set(holy_grail_tokens)))

import pickle
pickle.dump(t, open('holy_grail_tfidf.pkl', 'wb'))
pickle.dump(holy_grail_tokens, open('holy_grail_tokens.pkl', 'wb'))