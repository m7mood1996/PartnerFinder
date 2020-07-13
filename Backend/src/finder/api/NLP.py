from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import gensim
from nltk.tokenize import word_tokenize


def NLP_processor(documents, type):
    """
    function to make new corpus for a certain set of documents
    :param documents: list of lists of strings
    :param type: type of repository EU or B2MATCH
    :return: Corpus of the documents, list of lists of pairs (token_id, token_frequency)
    """
    if type == 'EU':
        dir = 'Dictionary'
    elif type == 'B2MATCH':
        dir = 'Dictionary_b2match'
    tokens = [process_document(doc) for doc in documents]
    try:
        dictionary = load_dictionary(dir)
    except:
        dictionary = build_dictionary([])
        dictionary.save(dir)
    dictionary.add_documents(tokens)
    dictionary.save(dir)
    return build_corpus(dictionary, tokens)


def process_document(document):
    """
    function to process a certain document by 1- tokenizing it 2- remove stop words 3- making lower cas of tokens
    4- stemming each token
    :param document: string
    :return: list of tokens
    """

    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    return [ps.stem(word.lower()) for word in word_tokenize(document) if
            not word in stop_words]  # tokenizing and normalize tokens


def build_dictionary(tokens):
    """
    function to build new dictionary with a certain tokens
    :param tokens: list of lists of tokens
    :return: Dictionary object
    """

    return gensim.corpora.Dictionary(tokens)  # mapping termId : term


def build_corpus(dictionary, tokens):
    """
    function to build a corpus, which is mapping each token id to its frequency
    :param dictionary: inner dictionary object for mapping token -> token id
    :param tokens: list of lists of tokens
    :return: list of lists of tuples (id, frequency)
    """

    # for each doc map termId : term frequency
    return [dictionary.doc2bow(lst) for lst in tokens]


def process_query_result(result):
    """
    function to process similarity result, it will map each document similarity percentage with the document id
    :param result: list of lists of percentages
    :return: pair of (doc id, doc similarity percentage)
    """

    if len(result) == 0:
        return []
    result = result[0]
    pairs = []
    for idx, sim_perc in enumerate(result):

        if sim_perc != 0:
            pairs.append((idx, sim_perc))
    return pairs


def add_documents(index, documents,type):
    """
    function to add new documents to existent index
    :param index: current index
    :param documents: list of lists of strings
    :param type: string to know which index b2match or eu
    :return: updated index
    """
    corpus = NLP_processor(documents,type)
    index.num_features += len(corpus) * 1000
    for doc in corpus:
        index.num_features += (len(doc) * 2)
    index.add_documents(corpus)
    index.save()
    return index


def load_index(path):
    """
    function to load index from a specific directory on disk
    :param path: path to directory
    :return: Similarity Object
    """

    return gensim.similarities.Similarity.load(path)


def load_dictionary(path):
    """
    function to load dictionary from a specific directory on disk
    :param path: path to directory
    :return: Dictionary object
    """

    return gensim.corpora.Dictionary.load(path)


def build_index(path, type):
    """
    build an empty index in disk and save it on a specific directory
    :param path: path of the directory
    :param type: string to know whatc index b2match or eu
    :return: Similarity object "index"
    """
    corpus = NLP_processor([], type)
    tfidf = gensim.models.TfidfModel(corpus)

    # build the index
    return gensim.similarities.Similarity(path, tfidf[corpus], num_features=10000)


def get_document_from_org(org):
    """
    function to take string attributes which are description and tags and keywords from EU organization and build a
    document for this organization
    :param org: EU organization object
    :return: string of description and tags and keywords (document)
    """

    res = [org['description']]
    for tag in org['tagsAndKeywords']:
        res.append(tag)

    return ' '.join(res)


def get_document_from_par(par, tags):
    """
    function to get the description and tags from participants
    :param par: participant
    :param tags: tags
    :return: string of combination of participants description and tags
    """

    res = [par.description]
    for tag in tags:
        res.append(tag)

    return ' '.join(res)
