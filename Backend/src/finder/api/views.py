from ..models import OrganizationProfile
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from time import sleep
from ..models import OrganizationProfile, Address, Tag, Event, TagP, Participants, Location
from .serializers import OrganizationProfileSerializer, AddressSerializer, TagSerializer, EventSerializer, ParticipantsSerializer, LocationSerializer, TagPSerializer
import json
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator




def getParticipentFromUrl(url_):

    driver = webdriver.Chrome('/Users/mahmoodnael/PycharmProjects/TestTT/venv/lib/python3.7/chromedriver')
    driver.get(url_)
    sleep(1)
    num_of_part = int( driver.execute_script("return document.getElementsByClassName(\"opportunities-count-number\")[0].innerHTML"))
    sleep(1)
    driver.execute_script("scrollBy(0,400)")
    par = []

    script = "return document.getElementsByClassName(\"card card-participant card-hover flex-row\")["
    script2 = "].parentElement.outerHTML"
    i=0
    res = ""
    sleep(1)
    #print(num_of_part)
    j=0
    while(j < num_of_part):

        while i < 8:
            res = str(script + str(i) + script2)
            #print(res)
            try:
                par.append( driver.execute_script(str(script + str(i) + script2)))
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
        #url = url_ + item.find("a")['href']
        soup = BeautifulSoup(item, 'html.parser')
        url = url_ + '/'+(soup.find("a")['href']).split('/')[-1]
        participent_url_arr.append(url)
    #print(num_of_part)
    #res = driver.execute_script("return document.getElementsByClassName(\"card card-participant card-hover flex-row\")[3].outerHTML")
    #print(res)
    driver.quit()

    #soup = BeautifulSoup(res, 'html.parser')
    ##------------------------ changes end here. Rest of the things are same. ------------------ ##
    #print(res)
    #box = soup.find(class_="card card-participant card-hover flex-row")
    """all_hackathons = box.find_all('div', {'class': 'challenge-card-modern'})
    for hackathon in all_hackathons:
        h_type = hackathon.find('div', {'class': 'challenge-type'}).text.replace('\n', '')
        name = hackathon.find('div', {'class': 'challenge-name'}).text.replace('\n', '')
        date = hackathon.find('div', {'class': 'date'}).text.replace('\n', '')
    """
    return participent_url_arr


def getParticipentDATA(url_):
    translator = Translator()
    driver = webdriver.Chrome('/Users/mahmoodnael/PycharmProjects/TestTT/venv/lib/python3.7/chromedriver')
    driver.get(url_)
    sleep(1)
    participant_panel_detail = driver.execute_script("return document.getElementsByClassName(\"participant-panel-detail shadow-component\")[0].innerHTML")
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

    childcount = int(driver.execute_script("return document.getElementsByClassName(\"personal-info-holder\")[0].childElementCount"))
    list_ = []
    i=0

    temp0 = driver.execute_script(
        'return document.getElementsByClassName("personal-info-holder")[0].innerText')
    #print(temp0)
    temp1 = None
    if childcount == 3:
        temp1 = driver.execute_script('return document.getElementsByClassName("personal-info-holder")[0].children[1].outerHTML')
        soup = BeautifulSoup(temp1, 'html.parser')
        temp1 = soup.find('a')['href']
    temp0 = temp0.split('\n')

    name = temp0[0]
    org_name = temp0[1]
    location = temp0[2]
    org_url = temp1

    #print(translator.translate(name).text,',',translator.translate( org_name).text,',',translator.translate(location).text,',',org_url)

    org_type = None
    try:
        org_type = driver.execute_script('return document.getElementsByClassName("type")[0].innerText')
    except:
        pass

    org_logo = None
    try:
        org_logo = driver.execute_script('return document.getElementsByClassName("organisation-logo")[0].currentSrc')
    except:
        pass

    org_description = None
    try:
        org_description = driver.execute_script('return document.getElementsByClassName("description")[0].innerText')
    except:
        pass
    src = translator.translate(org_description).src
    tags = []
    try:
        tag_count = int(driver.execute_script('return document.getElementsByClassName("tag lg").length'))
    except:
        tag_count = 0
    i=0
    while i < tag_count:
        try:
            #tags.append(driver.execute_script('return document.getElementsByClassName("tag lg")[' + str(i) + '].innerText'))
            tags.append(translator.translate(
                driver.execute_script('return document.getElementsByClassName("tag lg")[' + str(i) + '].innerText'),
                src=src).text)
            i += 1
        except:
            i += 1
    """print('\n')
    print(org_type)
    print(org_url)
    print(org_logo)
    print(translator.translate(org_description).text)
    src =translator.translate(org_description).src
    for item in tags:
        print(translator.translate(item, src=src).text)
    print('\n')"""
    return name, img_src, org_name, location, translator.translate(
        org_type).text, org_url, org_logo, tags, translator.translate(org_description).text




class OrganizationProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrganizationProfileSerializer

    @action(detail=False, methods=['POST'])
    def createOrganization(self, request):
        response = {'Message': 'Organization Created Successfully!'}

        data = json.loads(request.data['data'])
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
            org = OrganizationProfile(pic=data['pic'], legalName=data['legalName'], businessName=data['businessName'], classificationType=data['classificationType'], description=data['description'],
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

    @action(detail=False, methods=['GET'])
    def getOrganizationsByTags(self, request):
        print("Data is ff: \t", request.query_params)
        tags = request.query_params['data']
        tags = tags.split(',')
        # tags = json.loads(tags)
        print("TAGS \t", tags)
        # tags = data['tags']
        res = []
        allTags = Tag.objects.all()
        for tag in allTags:
            if tag.tag in tags:
                res.extend(tag.organizations.all())
        response = []
        for val in res:
            response.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
                             'address': {'country': val.address.country, 'city': val.address.city}, 'description': val.description, 'classificationType' : val.classificationType})

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getOrganizationsByCountries(self, request):
        countries = request.query_params['data']
        countries = countries.split(',')
        print ("countries", countries)
        # countries = data['countries']
        res = []
        allOrgs = OrganizationProfile.objects.all()
        for org in allOrgs:
            if org.address.country in countries:
                res.append(org)
        response = []
        for val in res:
            response.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
                             'address': {'country': val.address.country, 'city': val.address.city}, 'description': val.description, 'classificationType' : val.classificationType})

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
        all_event_b2match = "https://events.b2match.com/?all=true"
        b2match = "https://events.b2match.com"
        all_events_page = requests.get(all_event_b2match)
        all_events_soup = BeautifulSoup(all_events_page.content, 'html.parser')
        itemes = all_events_soup.find_all(class_="last next")
        all_events_last_page = itemes[0].find("a")['href']
        all_events = all_events_soup.find_all(class_="event-card-wrapper col-sm-6 col-md-4")

        for item in all_events:
            try:
                url = b2match + item.find("a")['href']
            except:
                pass
            try:
                event_title = item.find(class_="event-card-title").get_text()
            except:
                pass

            # newEvent = B2match_event(url,date,event_title,event_location,event_text)
            # all_events_list.append(newEvent)
            event = Event(event_name=event_title, event_url=url)
            event.save()

        curr_page = "/?all=true&page="
        i = 2
        while 1:
            all_events_page = requests.get(b2match + curr_page + str(i))
            all_events_soup = BeautifulSoup(all_events_page.content, 'html.parser')
            all_events = all_events_soup.find_all(class_="event-card-wrapper col-sm-6 col-md-4")
            print(i)
            for item in all_events:
                try:
                    url = b2match + item.find("a")['href']
                except:
                    pass
                try:
                    event_title = item.find(class_="event-card-title").get_text()
                except:
                    pass

                # newEvent = B2match_event(url,date,event_title,event_location,event_text)
                # all_events_list.append(newEvent)
                try:
                    event = Event(event_name=event_title, event_url=url)
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
            response.append({'event_name': val.event_name, 'event_url': val.event_url})
        return Response(response, status=status.HTTP_200_OK)

class ParticipantsViewSet(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ParticipantsSerializer

    @action(detail=False, methods=['POST'])
    def add_Participants_from_Event(self, request):
        events = Event.objects.last()
        print(events.event_name)
        print(events.event_url)
        # url_arr =getParticipentFromUrl(events.event_url + "/participants")
        url_arr = getParticipentFromUrl('https://technology-business-cooperation-days-2020.b2match.io/participants')
        for item in url_arr:
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
            print("xD" * 10)

            print(part_temp[7], "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk" * 3)
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
                try:
                    tag = TagP.objects.get(tag=i)
                except:
                    tag = TagP(tag=i)
                    tag.save()
                try:
                    participant.tags.add(tag=tag)

                except:
                    pass"""
            print("hello", part_temp[3])

            """try:
                location = Location.objects.get(location=part_temp[3])
            except:"""
            # print("xD"*10,participant)
            #    location.save()
            # location.participant.add(participent=participent)

            print("what!!!!")
            # participent.location.add(location)

        return Response({'message': 'done see DataBase'}, status=status.HTTP_200_OK)


