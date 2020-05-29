import datetime

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from time import sleep
from ..models import Event, TagP, Participants, Location, MapIDsB2match, \
    MapIDsB2matchUpcoming, Scores, UpdateSettings, AlertsSettings

from .serializers import OrganizationProfileSerializer, AddressSerializer, TagSerializer, EventSerializer, \
    ParticipantsSerializer, CallSerializer, CallTagSerializer, \
    AlertsSettingsSerializer, UpdateSettingsSerializer, ScoresSerializer
import json

import operator
from bs4 import BeautifulSoup
from selenium import webdriver

from celery.schedules import crontab
from celery.task import periodic_task

# from .NLP import *
# from .Utils import *
from .EU import *

from datetime import datetime

import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
                currAdjacent = getPicsFromCollaborations(
                    currOrg['collaborations'])
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
        B2MATCHRes = getB2MATCHPartByCountriesAndTags(tags, countries)

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
            response = {'email': alertsSettings.email,
                        'turned_on': alertsSettings.turned_on}
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
            alertsSettings = AlertsSettings(
                email=email, turned_on=turned_on, ID=1)
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
            response = {'EU': updateSettings.eu_last_update,
                        'B2MATCH': updateSettings.b2match_last_update}
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
            UpdateSettings.objects.filter(ID=1).update(
                b2match_last_update=b2matchDate)
        except:
            updateSettings = UpdateSettings(
                eu_last_update=euDate, b2match_last_update=b2matchDate, ID=1)
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
        if yes it sends an alert to the user's mail
        :param request: HTTP request
        :return: HTTP Response
        """
        response = {'Message': 'Please Turn Alerts ON!'}
        try:
            alerts_settings = AlertsSettings.objects.all()[0]
        except:
            alerts_settings['turned_on'] = False
        if not alerts_settings.turned_on:
            return Response(response, status=status.HTTP_200_OK)
        email = alerts_settings.email

        print("*" * 50)
        print("START BUILDING CONSORTIUM")
        print("*" * 50)
        response = {'Message': 'Error while building the consortium!'}

        # Call.objects.all().delete()
        # CallTag.objects.all().delete()
        # calls = get_proposal_calls()
        #
        # calls_to_send = []
        #
        # for call in calls:
        #     call = has_consortium(call)
        #     if call['hasConsortium']:
        #         calls_to_send.append({'title': call['title']})
        #         add_call_to_DB(call)

        calls = Call.objects.all()
        calls_to_send = []
        for call in calls:
            calls_to_send.append({'title': call.__dict__['title']})

        body = MIMEMultipart('alternative')

        calls = ''
        for call in calls_to_send:
            calls += '<li><b>' + call['title'] + '</b></li>'

        signature = 'Sincerly,<br>Consortium Builder Alerts'
        html = """\
        <html>
          <head><h3>You have new proposal calls that might interest you</h3></head>
          <body>
            <ol> 
            {}
            </ol>
            <br>
            <br>
            {}
          </body>
        </html>
        """.format(calls, signature)

        response = {'Message': 'Finished building consortium successfully!'}

        content = MIMEText(html, 'html')
        body.attach(content)
        body['Subject'] = 'EU Proposal Calls Alert'
        send_mail(receiver_email=email, message=body)
        return Response(response, status=status.HTTP_200_OK)


class CallTagViewSet(viewsets.ModelViewSet):
    queryset = CallTag.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CallTagSerializer


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
                dt = re.findall(
                    "((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)

            except:
                pass

            event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')

            url = get_the_participent_urls(url)
            upComing = False
            CurrentDate = datetime.datetime.now()
            if CurrentDate < event_date:
                upComing = True

            event = Event(event_name=event_title, event_url=url,
                          event_date=event_date, is_upcoming=upComing)
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
                    event_date_ = item.find(
                        class_="event-card-date").get_text()
                    event_date_ = event_date_.upper()
                    dt = re.findall(
                        "((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)

                except:
                    pass

                event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')
                try:
                    url = get_the_participent_urls(url)
                    upComing = False
                    CurrentDate = datetime.datetime.now()
                    if CurrentDate < event_date:
                        upComing = True

                    event = Event(event_name=event_title, event_url=url,
                                  event_date=event_date, is_upcoming=upComing)
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
        upcoming_events_soup = BeautifulSoup(
            upcoming_events_page.content, 'html.parser')
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
                dt = re.findall(
                    "((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)
            except:
                pass

            event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')

            url = get_the_participent_urls(url)
            upComing = False
            CurrentDate = datetime.datetime.now()
            if CurrentDate < event_date:
                upComing = True

            event = Event(event_name=event_title, event_url=url,
                          event_date=event_date, is_upcoming=upComing)
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
                    event_date_ = item.find(
                        class_="event-card-date").get_text()
                    event_date_ = event_date_.upper()
                    dt = re.findall(
                        "((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})", event_date_)

                except:
                    pass

                event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')
                try:
                    url = get_the_participent_urls(url)
                    upComing = False
                    CurrentDate = datetime.datetime.now()
                    if CurrentDate < event_date:
                        upComing = True
                    event = Event(event_name=event_title, event_url=url,
                                  event_date=event_date, is_upcoming=upComing)
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

                    index = add_par_to_index(
                        index, participant, part_temp[7], False)
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

                    index = add_par_to_index(
                        index, participant, part_temp[7], True)

        return Response({'message': 'done see DataBase'}, status=status.HTTP_200_OK)


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
        """
        API to update scores in the data base
        :param request: scores from user about RES, countries and orgs type
        :return: the updated scores
        """
        data = request.data['data']
        data = json.loads(data)

        try:
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

        return Response(ScoresSerializer(scores).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getscores(self, request):
        """
        API to send current scoures
        :param request:
        :return:
        """
        scores = Scores.objects.all()[0]
        return Response(ScoresSerializer(scores).data, status=status.HTTP_200_OK)


class AlertsB2match(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EventSerializer

    @action(detail=False, methods=['GET'])
    def alertB2match(self, request):
        events = Event.objects.filter(is_upcoming=True)
        myEvents = []
        for event in events:
            parts = event.event_part.all()
            count = len(parts)
            if count < 50:
                continue
            else:
                eventScore =getScoreForEvent(parts)
                myEvents.append( (event, eventScore))
                print(event.event_name,event.event_url,eventScore)
        myEvents.sort(key=operator.itemgetter(1),reverse=True)
        print(myEvents)




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
