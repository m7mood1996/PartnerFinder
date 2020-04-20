import datetime

from ..models import OrganizationProfile
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from time import sleep
from ..models import OrganizationProfile, Address, Tag, Event, TagP, Participants, Location
from .serializers import OrganizationProfileSerializer, AddressSerializer, TagSerializer, EventSerializer, \
    ParticipantsSerializer, LocationSerializer, TagPSerializer
import json
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator

import re
# def NLPPreProcess(tag):
#     # to lower case # done
#     # tokenizing
#     # remove stopwords
#     # stemming

def add_Participants_from_Upcoming_Event():
    """
            method to define API to import all the participants from the events we have in our DB and save them to the local DB
    """
    events = Event.objects.filter(is_upcoming=True)
    for event in events:
        print(event.event_name)
        print(event.event_url)
        try:
            url_arr = getParticipentFromUrl(
                event.event_url + "/participants")
        except:
            continue

        print(url_arr, "\t\t URL ARRAY")
        for item in url_arr:
            print("the url op participent is \t" + item)

            print("in the try \t" + item)
            part_temp = getParticipentDATA(item)

            print("xD" * 10)
            location = Location(location=part_temp[3])
            location.save()
            print("xD" * 10)
            try:
                participant = Participants(participant_name=part_temp[0], participant_img_url=part_temp[1],
                                           organization_name=part_temp[2], org_type=part_temp[4],
                                           org_url=part_temp[5],
                                           org_icon_url=part_temp[6], description=part_temp[8], location=location)

                participant.save()
                event.event_part.add(participant)
            except:
                continue
            print("xD" * 10)
            print("xD" * 10)
            print(location)
            print("xD" * 10)
            print(
                part_temp[7], "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk" * 3)
            for i in part_temp[7]:
                print(i)
                try:
                    currTag = TagP.objects.get(tag=i)
                    currTag.participant.add(participant)
                except:
                    currTag = TagP(tag=i)
                    currTag.save()
                    currTag.participant.add(participant)
        print("what!!!!")

def get_the_participent_urls(event_url):
    """
            method to get the particepents urls from event url
    """
    try:
        event_page = requests.get(event_url)
        all_events_soup = BeautifulSoup(event_page.content, 'html.parser')
        itemes = all_events_soup.find_all(class_="break-word")
        par_page = itemes[0].find("a")['href']
        # print(par_page, "\t ", event_url)

        return par_page
    except:
        return event_url


def getParticipentFromUrl(url_):
    """
            given particepant url extruct participent information

    """
    ##### for MacOS
    driver = webdriver.Chrome()
    ##### for Windows
    # driver = webdriver.Chrome('C:\\bin\chromedriver.exe')
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
    # print(num_of_part)
    j = 0
    while (j < num_of_part):

        while i < 8:
            res = str(script + str(i) + script2)
            # print(res)
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
    # print(num_of_part)
    # res = driver.execute_script("return document.getElementsByClassName(\"card card-participant card-hover flex-row\")[3].outerHTML")
    # print(res)
    driver.quit()

    # soup = BeautifulSoup(res, 'html.parser')
    ##------------------------ changes end here. Rest of the things are same. ------------------ ##
    # print(res)
    # box = soup.find(class_="card card-participant card-hover flex-row")
    """all_hackathons = box.find_all('div', {'class': 'challenge-card-modern'})
    for hackathon in all_hackathons:
        h_type = hackathon.find(
            'div', {'class': 'challenge-type'}).text.replace('\n', '')
        name = hackathon.find(
            'div', {'class': 'challenge-name'}).text.replace('\n', '')
        date = hackathon.find('div', {'class': 'date'}).text.replace('\n', '')
    """
    return participent_url_arr


def getParticipentDATA(url_):
    """
            after getint the participent info, do low level NLP and make up the participant object

    """
    translator = Translator()
    ### for macOS
    driver = webdriver.Chrome()
    ### for Windows
    # driver = webdriver.Chrome('C:\\bin\chromedriver.exe')

    driver.get(url_)
    sleep(1)
    participant_panel_detail = driver.execute_script(
        "return document.getElementsByClassName(\"participant-panel-detail shadow-component\")[0].innerHTML")
    soup = BeautifulSoup(participant_panel_detail, 'html.parser')
    img_src = None
    participant_name = None
    try:
        print("in img find \t")
        img_src = soup.find("img")['src']
    except:
        pass
    try:
        print("in participant_name find \t")

        participant_name = driver.execute_script(
            "return document.getElementsByClassName(\"name\")[0].innerText")
    except:
        pass

    childcount = int(driver.execute_script(
        "return document.getElementsByClassName(\"personal-info-holder\")[0].childElementCount"))
    list_ = []
    i = 0

    temp0 = driver.execute_script(
        'return document.getElementsByClassName("personal-info-holder")[0].innerText')
    print(temp0)
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

    # print(translator.translate(name).text,',',translator.translate( org_name).text,',',translator.translate(location).text,',',org_url)

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
        print(src)
    except:
        src = "en"
    print(src)
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
    print('\nwhat was that')
    """print(org_type)
    print(org_url)
    print(org_logo)
    print(translator.translate(org_description).text)
    src =translator.translate(org_description).src
    for item in tags:
        print(translator.translate(item, src=src).text)
    print('\n')"""
    try:
        desc = translator.translate(org_description).text
    except:
        desc = ""
    print("befor the last")

    try:
        org_type_t = translator.translate(org_type).text
    except:
        org_type_t = ""
    print("the last")
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

    def translateData(self, data):
        translator = Translator()
        for key in data:
            if type(data[key]) == str:
                data[key] = translator.translate(data[key]).text

        return data

    @action(detail=False, methods=['POST'])
    def createOrganization(self, request):

        """
        method to define API to create new organization and save it to the local DB
        """

        response = {'Message': 'Organization Created Successfully!'}

        data = json.loads(request.data['data'])
        data = self.translateData(data)

        try:
            OrganizationProfile.objects.get(pic=data['pic'])
            response = {
                'Message': 'Organization with the same PIC is already exists!'}
        except:
            if 'address' in data:
                if 'country' in data['address'] and 'city' in data['address']:
                    newAddress = Address(
                        country=data['address']['country'], city=data['address']['city'])
                    newAddress.save()
            org = OrganizationProfile(pic=data['pic'], legalName=data['legalName'], businessName=data['businessName'],
                                      classificationType=data['classificationType'], description=data['description'],
                                      address=newAddress)
            org.save()
            for tag in data['tagsAndKeywords']:
                try:
                    currTag = Tag.objects.get(tag=tag)
                    currTag.organizations.add(org)
                except:
                    currTag = Tag(tag=tag)
                    currTag.save()
                    currTag.organizations.add(org)

        return Response(response, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['GET'])
    # def getOrganizationsByTags(self, request):
    #     """
    #     method to define API to get all organizations with at least one tag from the list of tags.
    #     """
    #     tags = request.query_params['data']
    #     tags = tags.split(',')
    #     res = []
    #     allTags = Tag.objects.all()
    #     for tag in allTags:
    #         if tag.tag in tags:
    #             res.extend(tag.organizations.all())
    #     response = []
    #     for val in res:
    #         response.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
    #                          'address': {'country': val.address.country, 'city': val.address.city},
    #                          'description': val.description, 'classificationType': val.classificationType})
    #
    #     return Response(response, status=status.HTTP_200_OK)

    def getOrganizationsByTags(self, tags):
        """
        method to get all organizations with at least one tag from the list of tags.
        """
        tags = set(tags)
        res = []
        allTags = Tag.objects.all()
        for tag in allTags:
            if tag.tag in tags:
                res.extend(tag.organizations.all())

        return res

    # @action(detail=False, methods=['GET'])
    # def getOrganizationsByCountries(self, request):
    #     """
    #     method to define API to get all organizations that locates in one of the countries list.
    #     """
    #     countries = request.query_params['data']
    #     countries = countries.split(',')
    #     res = []
    #     allOrgs = OrganizationProfile.objects.all()
    #
    #     for org in allOrgs:
    #         if org.address.country in countries:
    #             res.append(org)
    #     response = []
    #     for val in res:
    #         response.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
    #                          'address': {'country': val.address.country, 'city': val.address.city},
    #                          'description': val.description, 'classificationType': val.classificationType})
    #
    #     return Response(response, status=status.HTTP_200_OK)

    def getOrganizationsByCountries(self, countries):
        """
        method to get all organizations that locates in one of the countries list.
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

    def getOrgsByCountriesAndTags(self, tags, countries):
        orgsByCountries = self.getOrganizationsByCountries(countries)
        orgsByTags = self.getOrganizationsByTags(tags)

        res = self.getOrgsIntersection(orgsByCountries, orgsByTags)

        # write method to rank the orgs by tags

        return res

    def getOrgsIntersection(self, orgs1, orgs2):
        res, seenPICS = [], set()

        for org in orgs1:
            seenPICS.add(org.pic)

        addedPICS = set()
        for org in orgs2:
            if org.pic in seenPICS and org.pic not in addedPICS:
                res.append(org)
                addedPICS.add(org.pic)

        return res

    @action(detail=False, methods=['GET'])
    def searchByCountriesAndTags(self, request):

        """
            genirc function to search Orgs from EU and participants from B2Match
        """

        data = request.data['data']
        data = json.loads(data)
        countries = data['countries']
        tags = data['tags']

        EURes = self.getOrgsByCountriesAndTags(tags, countries)

        # btmatch search result
        # print("RES", EURes)
        B2MATCHRes = self.getB2MATCHPartByCountriesAndTags(tags, countries)
        B2MATCH = []
        EU = []
        for val in EURes:
            print(val.pic, 'address', val.address)
            EU.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
                       'address': {'country': val.address.country, 'city': val.address.city},
                       'description': val.description, 'classificationType': val.classificationType})

        for val in B2MATCHRes:
            print(val.participant_name, 'address', val.location.location)
            B2MATCH.append({'participant_name': val.participant_name, 'organization_name': val.organization_name, 'org_type': val.org_type,
                       'address': val.location.location, 'description': val.description, 'participant_img': val.participant_img_url,
                       'org_url': val.org_url, 'org_icon_url': val.org_icon_url})


        print(B2MATCH)
        response = {'EU': EU, 'B2MATCH': B2MATCH}

        return Response(response, status=status.HTTP_200_OK)

    # def B2MatchSearchByTagsAndCountries(self, tags, countries):

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
            currLocation = participant.location.location.lower().split(" ",1)[1]
            if currLocation in countries:
                res.append(participant)
        return res

    def getParticipantsByTags(self, tags):
        """
        method to get all organizations with at least one tag from the list of tags.
        """
        tags = set(tags)
        res = []
        allTags = TagP.objects.all()
        for tag in allTags:
            if tag.tag in tags:
                res.extend(tag.participant.all())
        return res

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
        print(res)
        return res





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


def changeEventStatus(eventNoLongerUpcoming):
    print("updating......\n")
    for event in eventNoLongerUpcoming:
        e =Event.objects.get(event_name=event.event_name)
        e.is_upcoming = True
        e.save()
        print("[EVN]\t\t")
        print(e)
        print("\n")


def deleteEventsTree(toupdate):
    print("deleting......\n")
    for event in toupdate:
        currEvent = Event.objects.get(event_name=event.event_name)
        # get all the participant from each Event

        participants = list(currEvent.event_part.all())
        for part in participants:
            tags = part.tagsAndKeywordsP.all()
            for tag in tags:
                if tag.participant.all().count() < 2:
                    print("[Tag]\t\t")
                    print(tag)
                    print("\n")
                    tag.delete()
            print("[Par]\t\t")
            print(part)
            print("\n")
            part.delete()

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
                event_date_ =event_date_.upper()
                dt= re.findall("((([0-9]{2})| ([0-9]{1}))\ (\w+)\,\ [0-9]{4})",event_date_)

                print(dt[0][0])
            except:
                pass
            """try:
                event_date = datetime.datetime.strptime(event_date_, '%d %m ,%Y ')
            except:
                event_date = datetime.datetime.strptime(event_date_, '%d - %d %m ,%Y ')
            """
            event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')

            # newEvent = B2match_event(url,date,event_title,event_location,event_text)
            # all_events_list.append(newEvent)
            url = get_the_participent_urls(url)
            upComing = False
            CurrentDate = datetime.datetime.now()
            if CurrentDate < event_date:
                print("hello hello hello")

                upComing = True
            print(event_date)
            print(CurrentDate)
            print(upComing)
            event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming= upComing)
            print(url)
            event.save()

        curr_page = "/?all=true&page="
        i = 2
        while 1:
            all_events_page = requests.get(b2match + curr_page + str(i))
            all_events_soup = BeautifulSoup(
                all_events_page.content, 'html.parser')
            all_events = all_events_soup.find_all(
                class_="event-card-wrapper col-sm-6 col-md-4")
            print(i)
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

                    print(dt[0][0])

                except:
                    pass
                """try:
                    event_date = datetime.datetime.strptime(event_date_, '%d %m ,%Y ')
                except:
                    event_date = datetime.datetime.strptime(event_date_, '%d - %d %m ,%Y ')
                """
                event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')
                try:
                    url = get_the_participent_urls(url)
                    upComing = False
                    CurrentDate = datetime.datetime.now()
                    if CurrentDate < event_date:
                        print("hello hello hello")

                        upComing = True
                    print(event_date)
                    print(CurrentDate)
                    print(upComing)
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

                print(dt[0][0])
            except:
                pass
            """try:
                event_date = datetime.datetime.strptime(event_date_, '%d %m ,%Y ')
            except:
                event_date = datetime.datetime.strptime(event_date_, '%d - %d %m ,%Y ')
            """
            event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')

            # newEvent = B2match_event(url,date,event_title,event_location,event_text)
            # all_events_list.append(newEvent)
            url = get_the_participent_urls(url)
            upComing = False
            CurrentDate = datetime.datetime.now()
            if CurrentDate < event_date:
                print("hello hello hello")
                upComing = True
            print(event_date)
            print(CurrentDate)
            print(upComing)
            event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming=upComing)
            newEvents.append(event)
            print(url)
            # event.save()

        curr_page = "/?page="
        i = 2
        while 1:
            upcoming_events_page = requests.get(b2match + curr_page + str(i))
            upcoming_events_soup = BeautifulSoup(
                upcoming_events_page.content, 'html.parser')
            upcoming_events = upcoming_events_soup.find_all(
                class_="event-card-wrapper col-sm-6 col-md-4")
            print(i)
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

                    print(dt[0][0])

                except:
                    pass
                """try:
                    event_date = datetime.datetime.strptime(event_date_, '%d %m ,%Y ')
                except:
                    event_date = datetime.datetime.strptime(event_date_, '%d - %d %m ,%Y ')
                """
                event_date = datetime.datetime.strptime(dt[0][0], '%d %B, %Y')
                try:
                    url = get_the_participent_urls(url)
                    upComing = False
                    CurrentDate = datetime.datetime.now()
                    if CurrentDate < event_date:
                        print("hello hello hello")

                        upComing = True
                    print(event_date)
                    print(CurrentDate)
                    print(upComing)
                    event = Event(event_name=event_title, event_url=url, event_date=event_date, is_upcoming=upComing)
                    newEvents.append(event)
                    # event.save()
                except:
                    pass

                # all_events_list.append({"naem": event_title, "date": date, "location": event_location, "url": url, "event_text": event_text})

            if (curr_page + str(i) == upcoming_events_last_page):
                break

            i += 1
        myEvents = list(Event.objects.filter(is_upcoming=True))

        toupdate = []
        eventNoLongerUpcoming = []
        print(len(myEvents))
        print(len(newEvents))
        newEvents2 = []
        for e in newEvents:
            newEvents2.append(e.event_name)

        for event in myEvents:
            if event.event_name not in newEvents2:
                eventNoLongerUpcoming.append(event)
            else:
                toupdate.append(event)
        print(toupdate)
        print("\n\n")
        print(eventNoLongerUpcoming)

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
            print(event.event_name)
            print(event.event_url)
            try:
                url_arr = getParticipentFromUrl(
                    event.event_url + "/participants")
            except:
                continue

            print(url_arr, "\t\t URL ARRAY")
            for item in url_arr:
                print("the url op participent is \t" + item)

                print("in the try \t" + item)
                part_temp = getParticipentDATA(item)

                print("xD" * 10)
                location = Location(location=part_temp[3])
                location.save()
                print("xD" * 10)
                try:
                    participant = Participants(participant_name=part_temp[0], participant_img_url=part_temp[1],
                                               organization_name=part_temp[2], org_type=part_temp[4],
                                               org_url=part_temp[5],
                                               org_icon_url=part_temp[6], description=part_temp[8], location=location)

                    participant.save()
                    event.event_part.add(participant)
                except:
                    continue
                print("xD" * 10)
                print("xD" * 10)
                print(location)
                print("xD" * 10)
                print(
                    part_temp[7], "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk" * 3)
                for i in part_temp[7]:
                    print(i)
                    try:
                        currTag = TagP.objects.get(tag=i)
                        currTag.participant.add(participant)
                    except:
                        currTag = TagP(tag=i)
                        currTag.save()
                        currTag.participant.add(participant)
            print("what!!!!")
        # print(events.event_name)
        # print(events.event_url)
        # url_arr =getParticipentFromUrl(events.event_url + "/participants")
        # url_arr = getParticipentFromUrl('https://technology-business-cooperation-days-2020.b2match.io/participants')
        """
        for item in url_arr:
            print("the url op participent is \t" + item)
            try:
                part_temp = getParticipentDATA(item)
            except:
                continue

            print("xD" * 10)
            location = Location(location=part_temp[3])
            location.save()
            print("xD" * 10)
            participant = Participants(participant_name=part_temp[0], participant_img_url=part_temp[1],
                                       organization_name=part_temp[2], org_type=part_temp[4], org_url=part_temp[5],
                                       org_icon_url=part_temp[6], description=part_temp[8], location=location)

            participant.save()

            print("xD" * 10)
            print("xD" * 10)
            print(location)
            print("xD" * 10)"""
        """
            print(
                part_temp[7], "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk" * 3)
            for i in part_temp[7]:
                print(i)
                try:
                    currTag = TagP.objects.get(tag=i)
                    currTag.participant.add(participant)
                except:
                    currTag = TagP(tag=i)
                    currTag.save()
                    currTag.participant.add(participant)
            """
        """
                  try:
                      tag = TagP.objects.get(tag=i)
                  except:
                      tag = TagP(tag=i)
                      tag.save()
                  try:
                      participant.tags.add(tag=tag)

                  except:
                      pass"""
        # print("hello", part_temp[3])

        """try:
                location = Location.objects.get(location=part_temp[3])
            except:"""
        # print("xD"*10,participant)
        #    location.save()
        # location.participant.add(participent=participent)

        # print("what!!!!")
        # participent.location.add(location)

        return Response({'message': 'done see DataBase'}, status=status.HTTP_200_OK)
