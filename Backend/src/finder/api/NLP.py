from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import gensim
from nltk.tokenize import word_tokenize


def NLP_Processor(documents):
    """
    function to make new corpus for a certain set of documents
    :param documents: list of strings
    :return: Corpus of the documents
    """
    tokens = [process_Document(doc) for doc in documents]
    try:
        dictionary = load_dictionary("Dictionary")
    except:
        dictionary = get_ids([])
        dictionary.save("Dictionary")

    print(dictionary)
    dictionary.add_documents(tokens)
    dictionary.save("Dictionary")
    print(dictionary)
    return build_corpus(dictionary, tokens)


def process_Document(document):
    """
    function to process a certain document which tokenize and make lower case for the current document
    :param document: string
    :return: list of tokens
    """
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    return [ps.stem(word.lower()) for word in word_tokenize(document) if
            not word in stop_words]  # tokenizing and normalize tokens


def get_ids(tokens):
    """
    a function to map each token into a unique id
    :param tokens: list of lists of tokens
    :return: Dictionary object
    """

    return gensim.corpora.Dictionary(tokens)  # mapping termId : term


def build_corpus(dictionary, tokens):
    """
    a function to build a corpus, which is mapping each token id to its frequency
    :param dictionary: object for mapping token -> token id
    :param tokens: list of lists of tokens
    :return: list of lists of tuples (id, frequency)
    """

    # for each doc map termId : term frequency
    return [dictionary.doc2bow(lst) for lst in tokens]


def process_query_result(result):
    """
    a function to process similarity result, it will map each document similarity percentage with the document
    id
    :param result: list of lists of percentages
    :return: pair of (doc id, doc similarity percentage)
    """

    if len(result) == 0:
        return []
    result = result[0]
    pairs = []
    for idx, sim_perc in enumerate(result):
        pairs.append((idx, sim_perc))

    return pairs


def add_documents(index, documents):
    """
    function to add new documents to existent index
    :param index: current index
    :param documents: list of strings
    :return: updated index
    """
    corpus = NLP_Processor(documents)
    index.num_features += len(corpus)
    for doc in corpus:
        index.num_features += (len(doc) * 2)
    index.add_documents(corpus)
    index.save()
    return index


def load_index(path):
    """
    function to load index from a specific directory in disk
    :param path: path to directory
    :return: Similarity Object
    """

    return gensim.similarities.Similarity.load(path)

def load_dictionary(path):
    """

    :param path:
    :return:
    """

    return gensim.corpora.Dictionary.load(path)

def build_index(path):
    """
    build an empty index in disk
    :param path: path of the directory
    :return: Similarity object "index"
    """

    corpus = NLP_Processor([])
    tfidf = gensim.models.TfidfModel(corpus, )

    # build the index
    return gensim.similarities.Similarity(path, tfidf[corpus], num_features=10000)


def get_document_from_org(org):
    """
    function to take string attributes which are description and tags and keywords from EU organization
    :param org: EU organization object
    :return: string of description and tags and keywords
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
