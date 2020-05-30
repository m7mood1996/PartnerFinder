from ..models import Event, TagP, Participants, Location, MapIDsB2match, \
    MapIDsB2matchUpcoming, Scores
from .NLP import *
from bs4 import BeautifulSoup
from selenium import webdriver
from .Utils import *
from time import sleep
import re
import operator


def deleteEventsTree(toupdate):
    """
    function to delete events and its participants
    :param toupdate:
    :return:
    """
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


def getTagsForPart(part):
    """
    function to get the tags from participant
    :param part: participant
    :return: list of tags
    """
    myTags = []
    tags = TagP.objects.filter(participants=part).tag
    for tagp in tags:
        myTags.append(tagp.tag)
    return myTags


def addEventsParToMainIndex(event):
    """
    function to add participant to the index
    :param event:
    :return:
    """
    partsipants = event.event_part

    # index = load_index('/Users/mahmoodnael/PycharmProjects/PartnerFinderApril/Backend/src/B2MATCH_Index')
    index = load_index('B2MATCH_Index')
    for part in partsipants:
        tags = getTagsForPart(part)
        des = get_document_from_par(part, tags)
        index = add_par_to_index(index, part, des, False)


def changeEventStatus(eventNoLongerUpcoming):
    """
    function to change event status when its date pass
    :param eventNoLongerUpcoming:
    :return:
    """
    for event in eventNoLongerUpcoming:
        e = Event.objects.get(event_name=event.event_name)
        e.is_upcoming = True
        e.save()
        addEventsParToMainIndex(e)


def add_Participants_from_Upcoming_Event():
    """
    function to define API to import all the participants from the events we have in our DB and save them to the local DB

    :return:
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
    function to get the participants urls from event url
    :param event_url: events url
    :return: participants url
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
    given participant url extruct participent information
    :param url_: the event url
    :return: participant url
    """
    # for MacOS
    # driver = webdriver.Chrome()
    # for Windows
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
     after geting the participant info, do low level NLP and make up the participant object
    :param url_: the main url of the participant
    :return: participant information
    """

    translator = Translator()
    # for macOS
    # driver = webdriver.Chrome()
    # for Windows
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
        participant_name = driver.execute_script(
            "return document.getElementsByClassName(\"name\")[0].innerText")
    except:
        pass

    childcount = int(
        driver.execute_script("return document.getElementsByClassName(\"personal-info-holder\")[0].childElementCount"))
    list_ = []
    i = 0

    temp0 = driver.execute_script(
        'return document.getElementsByClassName("personal-info-holder")[0].innerText')
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


def getPartIntersection(par1, par2):
    """
    function to get the intersect of two lists of participants
    :param par1: list of participants
    :param par2: list of participants
    :return: list of participant
    """
    res, seenPart = [], set()

    for par in par1:
        seenPart.add(par.participant_name)

    addedPar = set()
    for par in par2:
        if par.participant_name in seenPart and par.participant_name not in addedPar:
            res.append(par)
            addedPar.add(par.participant_name)
    return res


def getParticipantsByTags(tags):
    """
    function to get all organizations with at least one tag from the list of tags.
    :param tags: list of tags
    :return: list of participants
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
    res2 = [MapIDsB2matchUpcoming.objects.get(
        indexID=pair[0]) for pair in res2]

    finalRes = []
    for mapId in res1:
        finalRes.append(Participants.objects.get(pk=mapId.originalID))

    for mapId in res2:
        finalRes.append(Participants.objects.get(pk=mapId.originalID))

    print(finalRes[0].description)
    print(len(finalRes))
    return finalRes


def getB2MatchParByCountry(countries):
    """
    function to get all Participants that locates in one of the countries list.
    :param countries:  list of countries
    :return: list of participants
    """
    countries = [val.lower() for val in countries]
    countries = set(countries)
    res = []
    allPart = Participants.objects.all()

    if not countries:
        return allPart

    for participant in allPart:

        try:
            currLocation = participant.location.location.lower().split(" ", 1)[
                1]
        except:
            currLocation = participant.location.location.lower()
        if currLocation in countries:
            res.append(participant)
    return res


def getB2MATCHPartByCountriesAndTags(tags, countries):
    """
    function to get list of participants from DB based on tags and countries
    :param tags: list of tags to get participants
    :param countries: list of countries to get participants
    :return: list of participants
    """
    apaarticipantsByCountries = getB2MatchParByCountry(countries)
    ParticipantsByTags = getParticipantsByTags(tags)

    res = getPartIntersection(apaarticipantsByCountries, ParticipantsByTags)

    # write method to rank the orgs by tags

    return res



def fields(scores):
    return [ f.name for f in scores._meta.fields + scores._meta.many_to_many ]


def getSimilar(str1,str2):
    return str1.lower().replace('_', ' ') in str2.lower().replace('_',' ').replace('-',' ')

def getScoreForEvent(parts):
    """
    :param event: an Event
    :return: event with
    """
    scores = Scores.objects.all()[0]
    field = fields(scores)
    dic = {}
    for item in field:
        dic[item] = 0
    field[-3] = 'R&D Institution'
    eventScore = []
    locIndex = 0
    typeIndex = -1
    for part in parts:
        loc = part.location
        orgType = part.org_type
        for item in field:
            if getSimilar(item , loc.location):
                locIndex = field.index(item)
                dic[item] +=1
            if item == 'R&D Institution':
                if getSimilar(item,orgType):
                    typeIndex = field.index(item)
                elif getSimilar('r&d',orgType):
                    typeIndex = field.index(item)
                elif item in orgType:
                    typeIndex = field.index(item)

            elif item in orgType:
                typeIndex = field.index(item)
        locScore = getattr(scores, field[locIndex])
        if  field[typeIndex] =='R&D Institution':
            typeScore = getattr(scores,'R_D_Institution' )
        else:
            typeScore = getattr(scores, field[typeIndex])
        eventScore.append((locIndex, locScore * typeScore))
        locIndex=0
        typeIndex=-1
    field[-3] = 'R_D_Institution'
    theScore = 0
    for id,score in eventScore:
        if id == 0:
            continue
        theScore += dic[field[id]] * score

    return theScore *scores.RES
