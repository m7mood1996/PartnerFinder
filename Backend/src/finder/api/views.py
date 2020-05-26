import datetime
import collections

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from time import sleep
from ..models import OrganizationProfile, Address, Tag, Event, TagP, Participants, Location, MapIds, MapIDsB2match, \
    MapIDsB2matchUpcoming, Call, CallTag, Scores, UpdateSettings, AlertsSettings

from .serializers import OrganizationProfileSerializer, AddressSerializer, TagSerializer, EventSerializer, \
    ParticipantsSerializer, LocationSerializer, TagPSerializer, CallSerializer, CallTagSerializer, \
    AlertsSettingsSerializer, UpdateSettingsSerializer, ScoresSerializer
import json
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import gensim
from nltk.tokenize import word_tokenize
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import re

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ----------------------- NLP Processor Funcs --------------------------------------
def NLP_Processor(documents):
    """
    function to make new corpus for a certain set of documents
    :param documents: list of strings
    :return: Corpus of the documents
    """
    tokens = [process_Document(doc) for doc in documents]
    print(tokens)
    dictionary = get_ids(tokens)

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

    return [dictionary.doc2bow(lst) for lst in tokens]  # for each doc map termId : term frequency


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
    for doc in corpus:
        index.num_features += len(doc)
    index.num_features += 1000
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


def build_index(path):
    """
    build an empty index in disk
    :param path: path of the directory
    :return: Similarity object "index"
    """

    corpus = NLP_Processor([])
    tfidf = gensim.models.TfidfModel(corpus)

    return gensim.similarities.Similarity(path, tfidf[corpus], num_features=0)  # build the index


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
    res = [par.description]
    for tag in tags:
        res.append(tag)

    return ' '.join(res)


# ----------------------------------------------------------------------------------

# ----------------------- Gathering/Updating EU data Funcs -------------------------
LIST_OF_ATTRIBUTES = {'pic', 'businessName', 'legalName', 'classificationType', 'description',
                      'address', 'tagsAndKeywords', 'dataStatus', 'numberOfProjects', 'consorsiumRoles',
                      'collaborations'}


def getPicsFromCollaborations(collaborations):
    """
    function to get list of pics from list of organizations
    :param collaborations: list of organizations
    :return: list of pics
    """
    pics = set()
    for col in collaborations:
        pics.add(col['pic'])
    return pics


def getNumOfProjects(pic):
    """
    function to get number of projects for a certain EU organization
    :param pic: id of the organization
    :return: number of projects for this organization
    """

    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/api/orgProfile/publicProjects.json?pic=' + str(pic)
    response = []
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as error:
        print("Error - ", error)
        exit(0)

    return len(response.json()['publicProjects'])


def getOrganizationProfileFromEUByPIC(pic):
    """
    function to get organisation profile from the database of EU by pic number
    :param pic: id of the organization
    :return: organization profile in format of json
    """
    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/api/orgProfile/data.json?pic=' + str(pic)
    response = []
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as error:
        print("Error - ", error)
        exit(0)

    return getRelatedAttributes(response.json()['organizationProfile'])


def getRelatedAttributes(obj):
    """
    function to get the related fields from an EU organization object
    :param obj: EU organization
    :return: obj with the related fields
    """
    resObj = {}
    publicAttributes = obj['publicOrganizationData']

    for attribute in LIST_OF_ATTRIBUTES:
        if attribute in publicAttributes:
            if attribute == 'address':
                address = {'country': publicAttributes[attribute]['country'],
                           'city': publicAttributes[attribute]['city']}
                resObj[attribute] = address
            else:
                resObj[attribute] = publicAttributes[attribute]
        elif attribute == 'tagsAndKeywords' and attribute in obj:
            tags = obj[attribute]
            listOfTags = []
            for tag in tags:
                if 'text' in tag:
                    listOfTags.append(tag['text'])
            resObj[attribute] = listOfTags
        else:
            if attribute in obj:
                resObj[attribute] = obj[attribute]
            else:
                resObj[attribute] = ''

    resObj['numberOfProjects'] = getNumOfProjects(obj['publicOrganizationData']['pic'])
    resObj['consorsiumRoles'] = True if 'COORDINATOR' in resObj['consorsiumRoles'] else False
    resObj['pic'] = int(resObj['pic'])

    return resObj


def translateData(data):
    """
    function to translate non english data in object into english
    :param data: object
    :return: translated object
    """
    translator = Translator()
    for key in data:
        if type(data[key]) == str:
            try:
                data[key] = translator.translate(data[key]).text
            except:
                continue
    return data


class Graph:
    """
    class to define undirected unweighted graph
    """

    def __init__(self):
        self.graph = collections.defaultdict(set)
        self.vertices = set()

    def add(self, u, v):
        self.vertices.add(u)
        self.vertices.add(v)
        self.graph[u].add(v)
        self.graph[v].add(u)


def add_org_to_index(index, org):
    """
    function to add new organization to the index
    :param index: current index
    :param org: new EU organization
    :return: updated index
    """

    doc = get_document_from_org(org)
    originalID = org['pic']
    indexID = len(index)
    newMap = MapIds(originalID=originalID, indexID=indexID)
    newMap.save()
    index = add_documents(index, [doc])
    return index


def addOrganizationToDB(org):
    """
    method to add new organization to the local db
    :param org: EU organization
    :return: True/False
    """
    ATTRIBUTES = {'description', 'tagsAndKeywords', 'dataStatus',
                  'numberOfProjects', 'consorsiumRoles'}
    response = True
    org['collaborations'] = len(org['collaborations'])
    try:
        obj = OrganizationProfile.objects.get(pic=org['pic'])
        updated = False
        for atr in ATTRIBUTES:
            if atr != 'tagsAndKeywords':
                if org[atr] != getattr(obj, atr):
                    setattr(obj, atr, org[atr])
                    updated = True

        oldTags = Tag.objects.filter(organizations=obj)
        tags = set()
        for tag in oldTags:
            tags.add(tag.tag)
        newTags = set()
        if len(tags) != len(org['tagsAndKeywords']):
            updated = True
            for tag in org['tagsAndKeywords']:
                if tag not in tags:
                    newTags.add(tag)

        for tag in newTags:
            try:
                currTag = Tag.objects.get(tag=tag)
                currTag.organizations.add(obj)
            except:
                currTag = Tag(tag=tag)
                currTag.save()
                currTag.organizations.add(obj)

        if updated:
            obj.save()
            response = True
    except:
        if 'address' in org:
            if 'country' in org['address'] and 'city' in org['address']:
                newAddress = Address(
                    country=org['address']['country'], city=org['address']['city'])
                newAddress.save()
        newOrg = OrganizationProfile(pic=org['pic'], legalName=org['legalName'], businessName=org['businessName'],
                                     classificationType=org['classificationType'], description=org['description'],
                                     address=newAddress, dataStatus=org['dataStatus'],
                                     numberOfProjects=org['numberOfProjects'],
                                     consorsiumRoles=org['consorsiumRoles'], collaborations=org['collaborations'])
        newOrg.save()
        for tag in org['tagsAndKeywords']:
            try:
                currTag = Tag.objects.get(tag=tag)
                currTag.organizations.add(newOrg)
            except:
                currTag = Tag(tag=tag)
                currTag.save()
                currTag.organizations.add(newOrg)

    return response


# ----------------------------------------------------------------------------------


# ----------------------- Processing query in EU data Funcs ------------------------
def getOrgsByTags(tags):
    """
    method to get all organizations with at least one tag from the list of tags.
    :param tags: list of tags
    :return: list of organizations objects
    """

    tags = ' '.join(tags)
    index = load_index('EU_Index')
    corpus = NLP_Processor([tags])
    res = index[corpus]

    res = process_query_result(res)
    res = sorted(res, key=lambda pair: pair[1], reverse=True)
    res = res[:100]
    res = [pair for pair in res if pair[1] > 0.6]
    res = [MapIds.objects.get(indexID=pair[0]) for pair in res]

    finalRes = []
    for mapId in res:
        finalRes.append(OrganizationProfile.objects.get(pic=mapId.originalID))

    return finalRes


def getOrganizationsByCountries(countries):
    """
    method to get all organizations that locates in one of the countries list.
    :param countries: list of countries
    :return: list of organizations objects
    """

    countries = [val.lower() for val in countries]

    countries = set(countries)
    res = []
    allOrgs = OrganizationProfile.objects.all()

    if not countries:
        return allOrgs

    for org in allOrgs:
        currCountry = org.address.country.lower()
        if currCountry in countries:
            res.append(org)

    return res


def getOrgsIntersection(orgs1, orgs2):
    """
    private method to get intersection between two lists of organizations
    :param orgs1: first list
    :param orgs2: second list
    :return: intersection list
    """
    res, seenPICS = [], set()

    for org in orgs1:
        seenPICS.add(org.pic)

    addedPICS = set()
    for org in orgs2:
        if org.pic in seenPICS and org.pic not in addedPICS:
            res.append(org)
            addedPICS.add(org.pic)

    return res


def getOrgsByCountriesAndTags(tags, countries):
    """
    private method to get organizations from the database that have a certain tags
    or located in one of the countries list.
    :param tags: list of tags
    :param countries: list of countries
    :return: list of organizations objects
    """
    orgsByCountries = getOrganizationsByCountries(countries)
    orgsByTags = getOrgsByTags(tags)

    res = getOrgsIntersection(orgsByCountries, orgsByTags)

    return res


# ----------------------------------------------------------------------------------

def add_Participants_from_Upcoming_Event():
    """
            method to define API to import all the participants from the events we have in our DB and save them to the local DB
    """
    events = Event.objects.filter(is_upcoming=True)
    for event in events:

        try:
            url_arr = getParticipentFromUrl(
                event.event_url + "/participants")
        except:
            continue

        for item in url_arr:

            part_temp = getParticipentDATA(item)

            location = Location(location=part_temp[3])
            location.save()
            try:
                participant = Participants(participant_name=part_temp[0], participant_img_url=part_temp[1],
                                           organization_name=part_temp[2], org_type=part_temp[4],
                                           org_url=part_temp[5],
                                           org_icon_url=part_temp[6], description=part_temp[8], location=location)

                participant.save()
                event.event_part.add(participant)

            except:
                continue

            for i in part_temp[7]:
                try:
                    currTag = TagP.objects.get(tag=i)
                    currTag.participant.add(participant)
                except:
                    currTag = TagP(tag=i)
                    currTag.save()
                    currTag.participant.add(participant)
            try:
                # this is the path for the index

                # index = load_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_upcoming_Index')
                index = load_index('B2MATCH_upcoming_Index')

                print("upcoming index loaded......")
            except:
                index = None

            if index is None:
                # this is the path for the index
                # index = build_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_upcoming_Index')
                index = build_index('B2MATCH_upcoming_Index')

                print("upcoming index built....")

            index = add_par_to_index(index, participant, part_temp[7], True)


def get_the_participent_urls(event_url):
    """
            method to get the particepents urls from event url
    """
    try:
        event_page = requests.get(event_url)
        all_events_soup = BeautifulSoup(event_page.content, 'html.parser')
        itemes = all_events_soup.find_all(class_="break-word")
        par_page = itemes[0].find("a")['href']

        return par_page
    except:
        return event_url


def getParticipentFromUrl(url_):
    """
            given particepant url extruct participent information

    """
    ##### for MacOS
    # driver = webdriver.Chrome()
    ##### for Windows
    driver = webdriver.Chrome('C:\\bin\chromedriver.exe')
    driver.get(url_)
    sleep(1)
    num_of_part = int(driver.execute_script(
        "return document.getElementsByClassName(\"opportunities-count-number\")[0].innerHTML"))
    sleep(1)
    driver.execute_script("scrollBy(0,400)")
    par = []

    script = "return document.getElementsByClassName(\"card card-participant card-hover flex-row\")["
    script2 = "].parentElement.outerHTML"
    i = 0
    res = ""
    sleep(1)
    j = 0
    while (j < num_of_part):

        while i < 8:
            res = str(script + str(i) + script2)
            try:
                par.append(driver.execute_script(
                    str(script + str(i) + script2)))
                i += 1

            except:
                break
        driver.execute_script("scrollBy(0,500)")
        sleep(2)
        driver.execute_script("scrollBy(0,500)")
        sleep(2)
        j += i
        i = 0

    participent_url_arr = []
    for item in par:
        # url = url_ + item.find("a")['href']
        soup = BeautifulSoup(item, 'html.parser')
        url = url_ + '/' + (soup.find("a")['href']).split('/')[-1]
        participent_url_arr.append(url)

    driver.quit()

    return participent_url_arr


def getParticipentDATA(url_):
    """
            after getint the participent info, do low level NLP and make up the participant object

    """
    translator = Translator()
    ### for macOS
    # driver = webdriver.Chrome()
    ### for Windows
    driver = webdriver.Chrome('C:\\bin\chromedriver.exe')

    driver.get(url_)
    sleep(1)
    participant_panel_detail = driver.execute_script(
        "return document.getElementsByClassName(\"participant-panel-detail shadow-component\")[0].innerHTML")
    soup = BeautifulSoup(participant_panel_detail, 'html.parser')
    img_src = None
    participant_name = None
    try:

        img_src = soup.find("img")['src']
    except:
        pass
    try:
        participant_name = driver.execute_script("return document.getElementsByClassName(\"name\")[0].innerText")
    except:
        pass

    childcount = int(
        driver.execute_script("return document.getElementsByClassName(\"personal-info-holder\")[0].childElementCount"))
    list_ = []
    i = 0

    temp0 = driver.execute_script('return document.getElementsByClassName("personal-info-holder")[0].innerText')
    temp1 = None
    if childcount == 3:
        temp1 = driver.execute_script(
            'return document.getElementsByClassName("personal-info-holder")[0].children[1].outerHTML')
        soup = BeautifulSoup(temp1, 'html.parser')
        temp1 = soup.find('a')['href']
    temp0 = temp0.split('\n')
    try:
        name = temp0[0]
    except:
        name = ""
    try:
        org_name = temp0[1]
        org_name = org_name.split("at")[-1]
    except:
        org_name = ""
    try:
        location = temp0[2]
    except:
        location = ""
    try:
        org_url = temp1
    except:
        org_url = ""

    org_type = None
    try:
        org_type = driver.execute_script(
            'return document.getElementsByClassName("type")[0].innerText')
    except:
        pass

    org_logo = None
    try:
        org_logo = driver.execute_script(
            'return document.getElementsByClassName("organisation-logo")[0].currentSrc')
    except:
        pass

    org_description = None
    try:
        org_description = driver.execute_script(
            'return document.getElementsByClassName("description")[0].innerText')
    except:
        pass
    try:
        src = translator.translate(org_description).src
    except:
        src = "en"
    tags = []
    try:
        tag_count = int(driver.execute_script(
            'return document.getElementsByClassName("tag lg").length'))
    except:
        tag_count = 0
    i = 0
    while i < tag_count:
        try:
            # tags.append(driver.execute_script('return document.getElementsByClassName("tag lg")[' + str(i) + '].innerText'))
            recc_tag = driver.execute_script(
                'return document.getElementsByClassName("tag lg")[' + str(i) + '].innerText')
        except:
            i += 1
            continue
        try:
            recc_tag_trans = translator.translate(recc_tag, src=src).text
            tags.append(recc_tag_trans)
            i += 1
        except:
            tags.append(recc_tag)
            i += 1

    try:
        desc = translator.translate(org_description).text
    except:
        desc = ""

    try:
        org_type_t = translator.translate(org_type).text
    except:
        org_type_t = ""

    driver.quit()
    if desc != "":
        org_description = desc
    elif org_description == None:
        org_description = ""
    if org_type_t != "":
        org_type = org_type_t
    elif org_type == None:
        org_type = ""
    return name, img_src, org_name, location, org_type, org_url, org_logo, tags, org_description


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrganizationProfileSerializer

    @action(detail=False, methods=['GET'])
    def updateOrganizations(self, request):
        """
        method to define API to update organizations in the local DB
        :param request: HTTP request
        :return: HTTP Response
        """

        print("*" * 50)
        print("START UPDATING EU DB")
        print("*" * 50)

        MapIds.objects.all().delete()

        response = {'Message': 'Error while updating the organizations!'}
        try:
            index = load_index('EU_Index')
        except:
            index = None

        if index is None:
            index = build_index('EU_Index')
        else:
            index.destroy()
            index = build_index('EU_Index')

        status = {}
        graph = Graph()
        visitngQueue = collections.deque()
        startOrg = '999993953'
        visitngQueue.append(startOrg)
        status[startOrg] = 'visiting'
        while len(visitngQueue) > 0:
            currPic = visitngQueue.popleft()
            try:
                currOrg = getOrganizationProfileFromEUByPIC(currPic)
                currAdjacent = getPicsFromCollaborations(currOrg['collaborations'])
            except:
                continue
            for pic in currAdjacent:
                if pic not in graph.vertices or status[pic] == 'notVisited':
                    graph.add(currPic, pic)
                    status[pic] = 'visiting'
                    visitngQueue.append(pic)

            currOrg = translateData(currOrg)
            addOrganizationToDB(currOrg)
            index = add_org_to_index(index, currOrg)
            status[currPic] = 'visited'

        response = {'Message': 'Organizations updated successfully!'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def searchByCountriesAndTags(self, request):
        """
        generic function to search organizations from EU and participants from B2Match
        :param request: request with tags and countries fields
        :return:
        """

        data = request.query_params['data']
        data = json.loads(data)
        countries = data['countries']
        tags = data['tags']
        EURes = getOrgsByCountriesAndTags(tags, countries)
        B2MATCHRes = self.getB2MATCHPartByCountriesAndTags(tags, countries)

        B2MATCH = []
        EU = []
        for val in EURes:
            EU.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
                       'address': {'country': val.address.country, 'city': val.address.city},
                       'description': val.description, 'classificationType': val.classificationType,
                       'dataStatus': val.dataStatus, 'numberOfProjects': val.numberOfProjects,
                       'consorsiumRoles': val.consorsiumRoles})

        for val in B2MATCHRes:
            B2MATCH.append({'participant_name': val.participant_name, 'organization_name': val.organization_name,
                            'org_type': val.org_type,
                            'address': val.location.location, 'description': val.description,
                            'participant_img': val.participant_img_url,
                            'org_url': val.org_url, 'org_icon_url': val.org_icon_url})

        response = {'EU': EU, 'B2MATCH': B2MATCH}

        return Response(response, status=status.HTTP_200_OK)

    def getB2MatchParByCountry(self, countries):
        """
        method to get all Participants that locates in one of the countries list.
        """
        countries = [val.lower() for val in countries]
        countries = set(countries)
        res = []
        allPart = Participants.objects.all()

        if not countries:
            return allPart

        for participant in allPart:

            try:
                currLocation = participant.location.location.lower().split(" ", 1)[1]
            except:
                currLocation = participant.location.location.lower()
            if currLocation in countries:
                res.append(participant)
        return res

    def getParticipantsByTags(self, tags):
        """
        method to get all organizations with at least one tag from the list of tags.
        """
        tags = ' '.join(tags)
        index1 = load_index('B2MATCH_Index')  # B2match_index
        index2 = load_index('B2MATCH_upcoming_Index')  # B2match_upcoming_index
        corpus = NLP_Processor([tags])
        print(corpus)
        res1 = index1[corpus]
        res2 = index2[corpus]
        print(res1, res2)

        res1 = process_query_result(res1)
        res2 = process_query_result(res2)

        res1 = sorted(res1, key=lambda pair: pair[1], reverse=True)
        res1 = res1[:101]
        res2 = sorted(res2, key=lambda pair: pair[1], reverse=True)
        res2 = res2[:101]

        res1 = [pair for pair in res1 if pair[1] > 0.3]
        res1 = [MapIDsB2match.objects.get(indexID=pair[0]) for pair in res1]
        res2 = [pair for pair in res2 if pair[1] > 0.3]
        res2 = [MapIDsB2matchUpcoming.objects.get(indexID=pair[0]) for pair in res2]

        finalRes = []
        for mapId in res1:
            finalRes.append(Participants.objects.get(pk=mapId.originalID))

        for mapId in res2:
            finalRes.append(Participants.objects.get(pk=mapId.originalID))

        print(finalRes[0].description)
        print(len(finalRes))
        return finalRes

    def getB2MATCHPartByCountriesAndTags(self, tags, countries):
        apaarticipantsByCountries = self.getB2MatchParByCountry(countries)
        ParticipantsByTags = self.getParticipantsByTags(tags)

        res = self.getPartIntersection(apaarticipantsByCountries, ParticipantsByTags)

        # write method to rank the orgs by tags

        return res

    def getPartIntersection(self, par1, par2):
        res, seenPart = [], set()

        for par in par1:
            seenPart.add(par.participant_name)

        addedPar = set()
        for par in par2:
            if par.participant_name in seenPart and par.participant_name not in addedPar:
                res.append(par)
                addedPar.add(par.participant_name)
        return res


class AlertsSettingsViewSet(viewsets.ModelViewSet):
    queryset = AlertsSettings.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AlertsSettingsSerializer

    @action(detail=False, methods=['GET'])
    def getSettings(self, request):
        """
        method to define API to get updates settings.
        :param request: HTTP request
        :return: HTTP Response
        """
        try:
            alertsSettings = AlertsSettings.objects.all()[0]
            response = {'email': alertsSettings.email, 'turned_on': alertsSettings.turned_on}
        except:
            response = {'email': '', 'turned_on': ''}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def setSettings(self, request):
        """
        method to define API to update the update settings.
        :param request: HTTP request with update times
        :return: HTTP response
        """

        data = request.data['data']
        data = json.loads(data)
        email = data['email']
        turned_on = data['turned_on']

        try:
            AlertsSettings.objects.get(ID=1)
            AlertsSettings.objects.filter(ID=1).update(email=email)
            AlertsSettings.objects.filter(ID=1).update(turned_on=turned_on)
        except:
            alertsSettings = AlertsSettings(email=email, turned_on=turned_on, ID=1)
            alertsSettings.save()

        response = {'Message': 'Alerts Settings Updated Successfully.'}

        return Response(response, status=status.HTTP_200_OK)


class UpdateSettingsViewSet(viewsets.ModelViewSet):
    queryset = UpdateSettings.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UpdateSettingsSerializer

    @action(detail=False, methods=['GET'])
    def getSettings(self, request):
        """
        method to define API to get updates settings.
        :param request: HTTP request
        :return: HTTP Response
        """
        try:
            updateSettings = UpdateSettings.objects.all()[0]
            response = {'EU': updateSettings.eu_last_update, 'B2MATCH': updateSettings.b2match_last_update}
        except:
            response = {'EU': '', 'B2MATCH': ''}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def setSettings(self, request):
        """
        method to define API to update the update settings.
        :param request: HTTP request with update times
        :return: HTTP response
        """

        data = request.data['data']
        data = json.loads(data)
        euDate = int(data['EU'])
        b2matchDate = int(data['B2MATCH'])

        try:
            UpdateSettings.objects.get(ID=1)
            UpdateSettings.objects.filter(ID=1).update(eu_last_update=euDate)
            UpdateSettings.objects.filter(ID=1).update(b2match_last_update=b2matchDate)
        except:
            updateSettings = UpdateSettings(eu_last_update=euDate, b2match_last_update=b2matchDate, ID=1)
            updateSettings.save()

        response = {'Message': 'Updates Settings Updated Successfully.'}

        return Response(response, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AddressSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TagSerializer


# ----------------------- Consortium builder for open EU calls Funcs ---------------

LIST_OF_CALLS_ATTRIBUTES = {'type', 'status', 'ccm2Id', 'identifier', 'title', 'callTitle',
                            'deadlineDatesLong', 'tags', 'keywords', 'sumbissionProcedure'}

REST_ATTRIBUTES = {'description', 'conditions', 'ccm2Id', 'focusArea', 'supportInfo', 'actions'}


def get_related_attributes(obj):
    """
    function to get related attributes from call object
    :param obj: call object
    :return: new object with the related attributes
    """
    resObj = {}
    for atr in LIST_OF_CALLS_ATTRIBUTES:
        if atr in obj:
            resObj[atr] = obj[atr]
        else:
            resObj[atr] = ''

    return resObj


def get_rest_attributes(obj):
    """
    function to get specific attributes for call object from another API
    :param obj: call object
    :return: new call object with additional attributes
    """
    id = obj['identifier'].lower()
    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/topicDetails/' + id + '.json'

    try:
        response = requests.get(url)
        response = response.json()['TopicDetails']
        for atr in REST_ATTRIBUTES:
            if atr in response:
                obj[atr] = response[atr]
            else:
                obj[atr] = ''
        return obj
    except:
        return {}


def get_call_to_save(obj):
    """

    :param obj:
    :return:
    """
    finalObj = {}
    for atr in LIST_OF_CALLS_ATTRIBUTES:
        try:
            if atr == 'tags' or atr == 'keywords':
                if 'tagsAndKeywords' in finalObj:
                    finalObj['tagsAndKeywords'].extend(obj[atr])
                else:
                    finalObj['tagsAndKeywords'] = [tag for tag in obj[atr]]
            elif atr == 'sumbissionProcedure' or atr == 'status':
                finalObj[atr] = obj[atr]['abbreviation']
            elif atr == 'deadlineDatesLong':
                finalObj[atr] = (max(obj['deadlineDatesLong']) // 1000)
            else:
                finalObj[atr] = obj[atr]
        except:
            finalObj[atr] = ''

    return finalObj


def is_valid_date(date):
    """
    function to check if the deadline is more than three months from now
    :param date: deadline date
    :return: True/False
    """
    try:
        date //= 1000
        three_months = datetime.now() + relativedelta(months=+3)
        print(datetime.fromtimestamp(date))
        three_months = time.mktime(three_months.timetuple())
        return date >= three_months
    except:
        return False


def is_valid_status(obj):
    """
    function to check if the status of a certain call is not closed yet
    :param obj: call object
    :return: True/False
    """
    try:
        return obj['status']['abbreviation'] != 'Closed'
    except:
        return False


def is_relevant_action(obj):
    """
    function to check if the demand tags are being included in the call object actions
    :param obj: call object
    :return: True/False
    """
    tags = ['ia', 'ria']
    try:
        for action in obj['actions']:
            types = action['types']
            curr_tags = []
            for type in types:
                type = type.lower()
                type.replace('-', '')
                type.replace(' ', '')
                curr_tags.extend(type.lower())
            curr_tags = ''.join(curr_tags)
            for tag in tags:
                if tag in curr_tags:
                    return True
    except:
        return False


def get_proposal_calls():
    """
    function to get all proposal calls for grants that are open and have at least three months deadline
    :return: list of object of open calls
    """
    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantsTenders.json'

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as err:
        print(err)
        return []

    res = response.json()['fundingData']['GrantTenderObj']
    grants = []
    for obj in res:
        if 'type' in obj and obj['type'] == 1:
            obj = get_related_attributes(obj)
            obj = get_rest_attributes(obj)
            try:
                check_dates = [is_valid_date(date) for date in obj['deadlineDatesLong']]
            except:
                continue

            if any(check_dates) and is_valid_status(obj) and is_relevant_action(obj):
                obj = get_call_to_save(obj)
                grants.append(obj)
                print("ADDED")
                for atr in obj:
                    print(atr, ':', obj[atr])

    return grants


def add_call_to_DB(call):
    """
    method to add new call to the local db
    :param call: EU call
    :return: True/False
    """

    response = True
    call = translateData(call)
    try:
        Call.objects.get(ccm2Id=call['pic'])
        response = False
    except:
        newCall = Call(type=call['type'], status=call['status'], ccm2Id=call['ccm2Id'],
                       identifier=call['identifier'], title=call['title'],
                       callTitle=call['callTitle'], deadlineDate=call['deadlineDatesLong'],
                       sumbissionProcedure=call['sumbissionProcedure'], hasConsortium=call['hasConsortium'])
        newCall.save()
        for tag in call['tagsAndKeywords']:
            try:
                currTag = CallTag.objects.get(tag=tag)
                currTag.calls.add(newCall)
            except:
                currTag = CallTag(tag=tag)
                currTag.save()
                currTag.calls.add(newCall)

    return response


def has_consortium(call):
    """
    function to check if there is a consortium for a specific EU call
    :param call: EU call
    :return: new call with new field hasConsortium: True/False
    """

    orgs = getOrgsByCountriesAndTags(call['tagsAndKeywords'], [])

    countries = set()
    for org in orgs:
        countries.add(org.address.country)

    call['hasConsortium'] = True if len(countries) >= 3 else False

    return call


def send_mail(email, subject, message):
    sender_mail = 'PartnerFinderAlerts@gmail.com'
    password = 'Alerts_123'
    ssl_port = 465
    smtp_server = 'smtp.gmail.com'
    receiver_mail = email
    message['Subject'] = subject
    # message = 'Subject: {}\n\n{}'.format(subject, body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, ssl_port, context=context) as server:
            server.login(sender_mail, password)
            server.sendmail(sender_mail, receiver_mail, message.as_string())
        print("SENT")
    except Exception as e:
        print("ERROR", e)


# ----------------------------------------------------------------------------------

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CallSerializer

    @action(detail=False, methods=['GET'])
    def consortium_builder(self, request):
        """
        method to build a consortium for EU grants calls that have at least three months
        it checks if there is a potential partners from at least three different countries
        if yes it sends an alert to the user
        :param request: HTTP request
        :return: HTTP Response
        """

        alerts_settings = AlertsSettings.objects.all()[0]
        response = {'Message': 'Please Turn Alerts ON!'}
        if not alerts_settings.turned_on:
            return Response(response, status=status.HTTP_200_OK)
        email = alerts_settings.email
        print("*" * 50)
        print("START BUILDING CONSORTIUM")
        print("*" * 50)
        response = {'Message': 'Error while building the consortium!'}

        Call.objects.all().delete()
        CallTag.objects.all().delete()
        calls = get_proposal_calls()

        calls_to_send = []

        for call in calls:
            call = has_consortium(call)
            if call['hasConsortium']:
                calls_to_send.append({'title': call['title']})
                add_call_to_DB(call)

        # calls = Call.objects.all()
        # calls_to_send = []
        # for call in calls:
        #     calls_to_send.append(call.__dict__['title'])

        body = MIMEMultipart('alternative')

        calls = ''
        for i, call in enumerate(calls_to_send):
            calls += '<li><b>' + call['title'] + '</b></li>'

        signature = 'Sincerly,<br>Consortium Builder Alerts'
        html = """\
        <html>
          <head><h3>You have new proposal calls that might interests you</h3></head>
          <body>
            <ul> 
            {}
            </ul>
            <br>
            <br>
            {}
          </body>
        </html>
        """.format(calls, signature)


        response = {'Message': 'Finished building consortium successfully!'}

        content = MIMEText(html, 'html')
        body.attach(content)

        send_mail(email, "EU Proposal Calls Alert", body)
        return Response(response, status=status.HTTP_200_OK)


class CallTagViewSet(viewsets.ModelViewSet):
    queryset = CallTag.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CallTagSerializer


def getTagsForPart(part):
    myTags = []
    tags = TagP.objects.filter(participants=part).tag
    for tagp in tags:
        myTags.append(tagp.tag)
    return myTags


def addEventsParToMainIndex(event):
    partsipants = event.event_part

    # index = load_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_Index')
    index = load_index('B2MATCH_Index')
    for part in partsipants:
        tags = getTagsForPart(part)
        des = get_document_from_par(part, tags)
        index = add_par_to_index(index, part, des, False)


def changeEventStatus(eventNoLongerUpcoming):
    for event in eventNoLongerUpcoming:
        e = Event.objects.get(event_name=event.event_name)
        e.is_upcoming = True
        e.save()
        addEventsParToMainIndex(e)


def deleteEventsTree(toupdate):
    for event in toupdate:
        currEvent = Event.objects.get(event_name=event.event_name)
        # get all the participant from each Event

        participants = list(currEvent.event_part.all())
        for part in participants:
            tags = part.tagsAndKeywordsP.all()
            for tag in tags:
                if tag.participant.all().count() < 2:
                    tag.delete()

            part.delete()
    MapIDsB2matchUpcoming.objects.all().delete()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        return Response({'message': 'cant add event like that'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def add_all_events(self, request):
        """
                method to define API to iimport all the events from B2MATCH and save it to the local DB
        """
        all_event_b2match = "https://events.b2match.com/?all=true"
        b2match = "https://events.b2match.com"
        all_events_page = requests.get(all_event_b2match)
        all_events_soup = BeautifulSoup(all_events_page.content, 'html.parser')
        itemes = all_events_soup.find_all(class_="last next")
        all_events_last_page = itemes[0].find("a")['href']
        all_events = all_events_soup.find_all(
            class_="event-card-wrapper col-sm-6 col-md-4")

        for item in all_events:
            try:
                url = b2match + item.find("a")['href']
            except:
                pass
            try:
                event_title = item.find(class_="event-card-title").get_text()
            except:
                pass
            try:
                event_date_ = item.find(class_="event-card-date").get_text()
                event_date_ = event_date_.upper()
                dt = re.findall("((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)


            except:
                pass

            event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')

            url = get_the_participent_urls(url)
            upComing = False
            CurrentDate = datetime.datetime.now()
            if CurrentDate < event_date:
                upComing = True

            event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming=upComing)
            event.save()

        curr_page = "/?all=true&page="
        i = 2
        while 1:
            all_events_page = requests.get(b2match + curr_page + str(i))
            all_events_soup = BeautifulSoup(
                all_events_page.content, 'html.parser')
            all_events = all_events_soup.find_all(
                class_="event-card-wrapper col-sm-6 col-md-4")
            for item in all_events:
                try:
                    url = b2match + item.find("a")['href']
                except:
                    pass
                try:
                    event_title = item.find(
                        class_="event-card-title").get_text()
                except:
                    pass

                # newEvent = B2match_event(url,date,event_title,event_location,event_text)
                # all_events_list.append(newEvent)
                try:
                    event_date_ = item.find(class_="event-card-date").get_text()
                    event_date_ = event_date_.upper()
                    dt = re.findall("((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)


                except:
                    pass

                event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')
                try:
                    url = get_the_participent_urls(url)
                    upComing = False
                    CurrentDate = datetime.datetime.now()
                    if CurrentDate < event_date:
                        upComing = True

                    event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming=upComing)
                    event.save()
                except:
                    pass

                # all_events_list.append({"naem": event_title, "date": date, "location": event_location, "url": url, "event_text": event_text})

            if (curr_page + str(i) == all_events_last_page):
                break

            i += 1
        res = Event.objects.all()
        response = []
        for val in res:
            response.append({'event_name': val.event_name,
                             'event_url': val.event_url})
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def update_upcoming_events(self, request):
        """
                updating upcoming events in the database <not tested yet>
        """
        print("updating....")
        # index = load_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_upcoming_Index')
        index = load_index('B2MATCH_upcoming_Index')
        index.destroy()
        newEvents = []
        upcoming_event_b2match = "https://events.b2match.com"
        b2match = "https://events.b2match.com"
        upcoming_events_page = requests.get(upcoming_event_b2match)
        upcoming_events_soup = BeautifulSoup(upcoming_events_page.content, 'html.parser')
        itemes = upcoming_events_soup.find_all(class_="last next")
        upcoming_events_last_page = itemes[0].find("a")['href']
        upcoming_events = upcoming_events_soup.find_all(
            class_="event-card-wrapper col-sm-6 col-md-4")

        for item in upcoming_events:
            try:
                url = b2match + item.find("a")['href']
            except:
                pass
            try:
                event_title = item.find(class_="event-card-title").get_text()
            except:
                pass
            try:
                event_date_ = item.find(class_="event-card-date").get_text()
                event_date_ = event_date_.upper()
                dt = re.findall("((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)
            except:
                pass

            event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')

            url = get_the_participent_urls(url)
            upComing = False
            CurrentDate = datetime.datetime.now()
            if CurrentDate < event_date:
                upComing = True

            event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming=upComing)
            newEvents.append(event)

        curr_page = "/?page="
        i = 2
        while 1:
            upcoming_events_page = requests.get(b2match + curr_page + str(i))
            upcoming_events_soup = BeautifulSoup(
                upcoming_events_page.content, 'html.parser')
            upcoming_events = upcoming_events_soup.find_all(
                class_="event-card-wrapper col-sm-6 col-md-4")
            for item in upcoming_events:
                try:
                    url = b2match + item.find("a")['href']
                except:
                    pass
                try:
                    event_title = item.find(
                        class_="event-card-title").get_text()
                except:
                    pass

                # newEvent = B2match_event(url,date,event_title,event_location,event_text)
                # all_events_list.append(newEvent)
                try:
                    event_date_ = item.find(class_="event-card-date").get_text()
                    event_date_ = event_date_.upper()
                    dt = re.findall("((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)

                except:
                    pass

                event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')
                try:
                    url = get_the_participent_urls(url)
                    upComing = False
                    CurrentDate = datetime.datetime.now()
                    if CurrentDate < event_date:
                        upComing = True
                    event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming=upComing)
                    newEvents.append(event)
                except:
                    pass

            if (curr_page + str(i) == upcoming_events_last_page):
                break

            i += 1
        myEvents = list(Event.objects.filter(is_upcoming=True))

        toupdate = []
        eventNoLongerUpcoming = []
        newEvents2 = []
        for e in newEvents:
            newEvents2.append(e.event_name)

        for event in myEvents:
            if event.event_name not in newEvents2:
                eventNoLongerUpcoming.append(event)
            else:
                toupdate.append(event)

        changeEventStatus(eventNoLongerUpcoming)

        deleteEventsTree(toupdate)

        for e in toupdate:
            e.delete()

        for e in newEvents:
            e.save()
        print("Adding new Participants....\n")
        add_Participants_from_Upcoming_Event()

        return Response([{'message': 'done, B2MATCH Reposutory updated'}], status=status.HTTP_200_OK)


def add_par_to_index(index, par, tags, upcoming):
    """
    function to add new participant to the index
    :param index: current index
    :param par: new participant
    :return: updated index
    """
    doc = get_document_from_par(par, tags)
    originalID = par.id

    indexID = len(index)
    if not upcoming:
        newMap = MapIDsB2match(originalID=originalID, indexID=indexID)
    else:
        newMap = MapIDsB2matchUpcoming(originalID=originalID, indexID=indexID)
    newMap.save()
    index = add_documents(index, [doc])
    return index


class ParticipantsViewSet(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ParticipantsSerializer

    @action(detail=False, methods=['POST'])
    def add_Participants_from_Event(self, request):
        """
                method to define API to import all the participants from the events we have in our DB and save them to the local DB
        """
        events = Event.objects.all()
        for event in events:

            try:
                url_arr = getParticipentFromUrl(
                    event.event_url + "/participants")
            except:
                continue
            for item in url_arr:
                try:
                    part_temp = getParticipentDATA(item)
                except:
                    continue
                location = Location(location=part_temp[3])
                location.save()
                try:
                    participant = Participants(participant_name=part_temp[0], participant_img_url=part_temp[1],
                                               organization_name=part_temp[2], org_type=part_temp[4],
                                               org_url=part_temp[5],
                                               org_icon_url=part_temp[6], description=part_temp[8], location=location)

                    participant.save()
                    event.event_part.add(participant)
                except:
                    continue

                for i in part_temp[7]:
                    try:
                        currTag = TagP.objects.get(tag=i)
                        currTag.participant.add(participant)
                    except:
                        currTag = TagP(tag=i)
                        currTag.save()
                        currTag.participant.add(participant)
                if not event.is_upcoming:
                    try:
                        # this is the path for the index
                        # index = load_index(
                        #     '/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_Index')
                        index = load_index('B2MATCH_Index')
                        print("index loaded......")
                    except:
                        index = None

                    if index is None:
                        # this is the path for the index
                        # index = build_index(
                        #     '/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_Index')
                        index = build_index('B2MATCH_Index')
                        print("index built....")

                    index = add_par_to_index(index, participant, part_temp[7], False)
                elif event.is_upcoming:
                    try:
                        # this is the path for the index

                        # index = load_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_upcoming_Index')
                        index = load_index('B2MATCH_upcoming_Index')
                        print("upcoming index loaded......")
                    except:
                        index = None

                    if index is None:
                        # this is the path for the index
                        # index = build_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_upcoming_Index')
                        index = build_index('B2MATCH_upcoming_Index')
                        print("upcoming index built....")

                    index = add_par_to_index(index, participant, part_temp[7], True)

        return Response({'message': 'done see DataBase'}, status=status.HTTP_200_OK)


def add_par_to_index(index, par, tags, upcoming):
    """
    function to add new participant to the index
    :param index: current index
    :param par: new participant
    :return: updated index
    """
    doc = get_document_from_par(par, tags)
    originalID = par.id

    indexID = len(index)
    if not upcoming:
        newMap = MapIDsB2match(originalID=originalID, indexID=indexID)
    else:
        newMap = MapIDsB2matchUpcoming(originalID=originalID, indexID=indexID)
    newMap.save()
    index = add_documents(index, [doc])
    return index


class ScoresViewSet(viewsets.ModelViewSet):
    queryset = Scores.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ScoresSerializer

    def create(self, request, *args, **kwargs):
        return Response({'message': 'cant add event like that'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def updatescores(self, request):
        data = request.data['data']
        data = json.loads(data)
        print("DATA", data)

        try:
            print("in try")
            scores = Scores.objects.all()[0]
            scores.RES = data['RES']
            scores.Italy = data['Italy']
            scores.France = data['France']
            scores.Austria = data['Austria']
            scores.Germany = data['Germany']
            scores.Denmark = data['Denmark']
            scores.Czech_Republic = data['Czech_Republic']
            scores.Finland = data['Finland']
            scores.Ireland = data['Ireland']
            scores.Israel = data['Israel']
            scores.Portugal = data['Portugal']
            scores.Ukranie = data['Ukranie']
            scores.United_Kingdom = data['United_Kingdom']
            scores.Turkey = data['Turkey']
            scores.Switzerland = data['Switzerland']
            scores.Spain = data['Spain']
            scores.Norway = data['Norway']

            scores.Association_Agency = data['Association_Agency']
            scores.University = data['University']
            scores.R_D_Institution = data['R_D_Institution']
            scores.Start_Up = data['Start_Up']
            scores.Others = data['Others']

        except:
            print("in except")
            scores = Scores(RES=data['RES'],
                            Italy=data['Italy'], France=data['France'], Austria=data['Austria'],
                            Germany=data['Germany'],
                            Denmark=data['Denmark'], Czech_Republic=data['Czech_Republic'], Finland=data['Finland'],
                            Ireland=data['Ireland'], Israel=data['Israel'], Portugal=data['Portugal'],
                            Ukranie=data['Ukranie'], United_Kingdom=data['United_Kingdom'], Turkey=data['Turkey'],
                            Switzerland=data['Switzerland'], Spain=data['Spain'], Norway=data['Norway'],
                            Association_Agency=data['Association_Agency'], University=data['University'],
                            R_D_Institution=data['R_D_Institution'], Start_Up=data['Start_Up'], Others=data['Others']
                            )
        scores.save()

        # response.append({'scores': scores})
        return Response('response', status=status.HTTP_200_OK)
