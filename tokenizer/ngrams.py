__author__ = 'cris'

from itertools import islice

'''
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
'''

def is_hashtag(word):
    if word.startswith('#'):
            return True
    return False

def is_url(word):
    if word.startswith('http'):
            return True
    return False

def is_mention(word):
    if word.startswith('@'):
            return True
    return False

def is_url_or_mention(word):
    if word.startswith('http') or word.startswith('@'):
            return True
    return False

def contains_hashtag(iterable):
    for elem in iterable:
        if elem.startswith('#'):
            return True
    return False

def contains_mention(iterable):
    for elem in iterable:
        if elem.startswith('@'):
            return True
    return False

def contains_url(iterable):
    for elem in iterable:
        if elem.startswith('http'):
            return True
    return False

def contains_urls_mentions(iterable):
    for elem in iterable:
        if elem.startswith('http') or elem.startswith("@"):
            return True
    return False

def contains_non_words(iterable):
    for elem in iterable:
        if elem.startswith('http') or elem.startswith('#') or elem.startswith("@"):
            return True
    return False

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield u' '.join(result)

def window_no_twitter_elems(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if (len(result) == n) and (not contains_non_words(result)):
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        if not contains_non_words(result):
            yield u' '.join(result)

def window_no_hashtags(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if (len(result) == n) and ( not contains_hashtag(result)):
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        if not contains_hashtag(result):
            yield u' '.join(result)


if __name__ == '__main__':

    tweetsAsTokens = "this is @is #a tag test apple tree http://fu.com".split()
    print(tweetsAsTokens)
    # print contains_url(tweetsAsTokens)
    # for i in tweetsAsTokens:
    #     print is_url(i)

    for i in window(tweetsAsTokens,3):
        print i
