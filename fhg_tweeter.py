# fhg_tweeter.py
# needs a trained TfidfVectorizer saved in mp_tfidf.pkl
# loads holy grail text from a pickle so we don't have to
# import the full nltk.books each time!
import string
import nltk
#import nltk.book
import feedparser
import math
import re
import pickle

tfidf_vectorizer = pickle.load(open('holy_grail_tfidf.pkl', 'rb'))
print('Loaded Tfidf model')
holy_grail_tokens = pickle.load(open('holy_grail_tokens.pkl', 'rb'))
print('Loaded holy grail tokens')

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

def get_headlines(rss_url):
    # retrieve headlines from the given rss url. If name is 'Heading: Text',
    # returns only Text.
    feeds = feedparser.parse(rss_url)
    headlines = []
    for e in feeds['entries']:
        h = e['title']
        try:
            prefix, full = h.split(':', 2)
        except ValueError:
            full = h
        headlines.append(full.strip())
    return headlines
            
# list of urls to get headlines from:
headline_urls = [('http://www.baynews9.com/content/'
                 'news/baynews9/feeds/rss.html/strange.html')]
# get headlines and sum into a single list
headlines = sum([get_headlines(url) for url in headline_urls], [])

holy_grail_text = untokenize(holy_grail_tokens)
holy_grail_sentences = nltk.sent_tokenize(holy_grail_text)
holy_grail_vocab = set(holy_grail_tokens)
stopwords = set(nltk.corpus.stopwords.words('english'))


def get_sentences_containing(s):
    return [x for x in holy_grail_sentences if ' '+ s+' ' in x]

def mangle_title(title):
    # searches for any word in title that's also in all_words_mp.
    # If it finds one, joins the sentences together at that word
    title_words = nltk.word_tokenize(title)
    ret = []
    for i, w in enumerate(title_words):
        if (w in holy_grail_vocab 
                and w not in stopwords
                and w not in string.punctuation
                and len(w) > 3
                and i > 2):
            print('found match for ', w)
            cands = get_sentences_containing(w)
            root = untokenize(title_words[:i])
            for c in cands:
                last_bit = c[c.find(w):]
                list_bit = last_bit.split(' ')
                if len(list_bit) > 3:
                    ret.append(root + " " + last_bit)
                    #print('news title', title_words)
                    #print('last bit', last_bit)
                    #print('all', root + " " + last_bit)
    return ret

candidates = sum([mangle_title(h) for h in headlines], [])
