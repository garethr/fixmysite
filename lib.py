import re
import unicodedata
    
def slugify(value):
    """ Slugify a string, to make it URL friendly. """

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+','-',value)