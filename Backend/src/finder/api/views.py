import datetime

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from time import sleep
from ..models import Event, TagP, Participants, Location, MapIDsB2match, \
    MapIDsB2matchUpcoming, Scores, UpdateSettings, AlertsSettings

from .serializers import OrganizationProfileSerializer, AddressSerializer, TagSerializer, EventSerializer, \
    ParticipantsSerializer, CallSerializer, CallTagSerializer, \
    AlertsSettingsSerializer, UpdateSettingsSerializer, ScoresSerializer, EventsForAlertsSerializer
import json

import operator
from bs4 import BeautifulSoup
from selenium import webdriver

from celery.schedules import crontab
from celery.task import periodic_task

from .EU import *
from .B2MATCH import *
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import re
import os


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrganizationProfileSerializer

    @action(detail=False, methods=['GET'])
    def update_organizations(self, request):
        """
        method to define API to update organizations in the local DB
        :param request: HTTP request
        :return: HTTP Response
        """

        print("*" * 50)
        print("START UPDATING EU DB")
        print("*" * 50)

        try:
            try:
                index = load_index('EU_Index_Temp')
                if os.path.exists('EU_Index_Temp.0') and os.path.getsize('EU_Index_Temp.0') > os.path.getsize(
                        'EU_Index.0'):
                    destroy_and_rename(old_index_name='EU_Index', new_index_name='EU_Index_Temp')
                else:
                    index.destroy()
            except:
                pass
            index = build_index('EU_Index_Temp')
            status = {}
            graph = Graph()
            visitngQueue = collections.deque()
            startOrg = '999993953'
            visitngQueue.append(startOrg)
            status[startOrg] = 'visiting'
            while len(visitngQueue) > 0:
                currPic = visitngQueue.popleft()
                try:
                    currOrg = get_organization_profile_by_pic(currPic)
                    currAdjacent = get_pics_from_collaborations(
                        currOrg['collaborations'])
                except:
                    continue
                for pic in currAdjacent:
                    if pic not in graph.vertices or status[pic] == 'notVisited':
                        graph.add(currPic, pic)
                        status[pic] = 'visiting'
                        visitngQueue.append(pic)

                currOrg = translate_data(currOrg)
                add_organization_to_DB(currOrg)
                index = add_org_to_index(index, currOrg)
                status[currPic] = 'visited'

            if os.path.exists('EU_Index_Temp.0') and os.path.getsize('EU_Index_Temp.0') > os.path.getsize('EU_Index.0'):
                destroy_and_rename(old_index_name='EU_Index', new_index_name='EU_Index_Temp')
            else:
                index.destroy()

            response = {'success': 'Organizations updated successfully!'}
            if not setUpdateSettings(euDate=time.mktime(datetime.datetime.now().timetuple())):
                raise
        except:
            setUpdateSettings(euDate=time.mktime(datetime.datetime.now().timetuple()))
            if os.path.exists('EU_Index_Temp.0') and os.path.getsize('EU_Index_Temp.0') > os.path.getsize('EU_Index.0'):
                destroy_and_rename(old_index_name='EU_Index', new_index_name='EU_Index_Temp')
            else:
                index.destroy()
            response = {'error': 'Error while updating organizations.'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def generic_search(self, request):
        """
        method to define API that defines generic function to search organizations from EU and participants from B2Match
        :param request: HTTTP request with tags, countries, types, and role fields
        :return: HTTP response with the relevant objects
        """

        try:
            data = request.query_params['data']
            data = json.loads(data)
            print(data)
            countries = data['countries']
            types = data['types']
            tags = data['tags']
            role = data['role']
            EURes = get_orgs_by_parameters(tags=tags, countries=countries, types=types,
                                           role=role)
            B2MATCHRes = getB2MATCHPartByCountriesAndTags(tags, countries)

            B2MATCH = []
            EU = []
            for val in EURes:
                EU.append({'legalName': val.legalName,
                           'country': val.address.country,
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
        except:
            response = {'EU': [], 'B2MATCH': [], 'error': 'Error while searching for organizations and participants'}

        return Response(response, status=status.HTTP_200_OK)


class AlertsSettingsViewSet(viewsets.ModelViewSet):
    queryset = AlertsSettings.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AlertsSettingsSerializer

    @action(detail=False, methods=['GET'])
    def get_settings(self, request):
        """
        method to define API to get alerts settings
        :param request: HTTP request
        :return: HTTP Response
        """
        try:
            alertsSettings = AlertsSettings.objects.all()[0]
            response = {'email': alertsSettings.email,
                        'turned_on': alertsSettings.turned_on}
        except:
            response = {'email': '', 'turned_on': '', 'error': 'Error while uploading alerts settings'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def set_settings(self, request):
        """
        method to define API to update the alerts settings
        :param request: HTTP request with updated email and turned_on flag
        :return: HTTP response
        """

        try:
            data = request.query_params['data']
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

            response = {'success': 'Alerts Settings Updated Successfully.'}
        except:
            response = {'error': 'Error while updating alerts settings'}

        return Response(response, status=status.HTTP_200_OK)


class UpdateSettingsViewSet(viewsets.ModelViewSet):
    queryset = UpdateSettings.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UpdateSettingsSerializer

    @action(detail=False, methods=['GET'])
    def get_settings(self, request):
        """
        method to define API to get last update times
        :param request: HTTP request
        :return: HTTP Response
        """
        try:
            updateSettings = UpdateSettings.objects.all()[0]
            response = {'EU': updateSettings.eu_last_update,
                        'B2MATCH': updateSettings.b2match_last_update}
        except:
            response = {'EU': '', 'B2MATCH': '', 'error': 'Error while uploading updates settings'}

        return Response(response, status=status.HTTP_200_OK)


class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CallSerializer

    @action(detail=False, methods=['GET'])
    def consortium_builder(self, request):
        """
        method to define API to build a consortium for EU grants calls that have at least three months deadline and
        there are three different potential partners from at least three different countries.
        if we have at least one relevant call an email will be sent to the user
        :param request: HTTP request
        :return: HTTP Response
        """

        try:
            response = {'success': 'Please Turn Alerts ON!'}
            try:
                alerts_settings = AlertsSettings.objects.all()[0]
            except:
                alerts_settings['turned_on'] = False
            if not alerts_settings.turned_on:
                return Response(response, status=status.HTTP_200_OK)

            email = alerts_settings.email

            Call.objects.all().delete()
            CallTag.objects.all().delete()
            calls = get_proposal_calls()

            calls_to_send = []

            for call in calls:
                call = has_consortium(call)
                if call['hasConsortium']:
                    calls_to_send.append({'title': call['title']})
                    add_call_to_DB(call)

            body = MIMEMultipart('alternative')

            calls = ''
            for call in calls_to_send:
                calls += '<li><b>' + call['title'] + '</b>.</li>'

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

            content = MIMEText(html, 'html')
            body.attach(content)
            body['Subject'] = 'EU Proposal Calls Alert'
            if len(calls_to_send) > 0:
                send_mail(receiver_email=email, message=body)
            response = {'success': 'Finished building consortium successfully!'}
        except:
            response = {'error': 'Error while building consortium.'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_calls(self, request):
        """
        method to define API to get all calls that has a potential participants
        :param request: HTTP request
        :return: HTTP Response
        """
        response = {'calls': []}
        try:
            calls = Call.objects.all()
            res = []
            for call in calls:
                res.append({'type': call.type, 'status': call.status, 'ccm2Id': call.ccm2Id,
                            'identifier': call.identifier, 'title': call.title,
                            'callTitle': call.callTitle, 'deadlineDate': call.deadlineDate,
                            'sumbissionProcedure': call.sumbissionProcedure})
            response['calls'] = res
        except:
            response = {'error': 'Error while uploading consortium calls', 'calls': []}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def search_organizations(self, request):
        """
        method to define API to search for organizations for a specific ccm2id call
        :param request: HTTP request
        :return: HTTP Response
        """
        try:
            data = request.query_params['data']
            data = json.loads(data)
            id = int(data['ccm2Id'])
            call = Call.objects.get(ccm2Id=id)
            tags = CallTag.objects.filter(calls=call)
            tagsList = []
            for tag in tags:
                tagsList.append(tag.tag)

            EURes = get_orgs_by_parameters(tags=tagsList, countries=[], types=[], role='')
            EU = []
            for val in EURes:
                EU.append({'legalName': val.legalName,
                           'country': val.address.country,
                           'description': val.description, 'classificationType': val.classificationType,
                           'dataStatus': val.dataStatus, 'numberOfProjects': val.numberOfProjects,
                           'consorsiumRoles': val.consorsiumRoles})

            response = {'EU': EU}
        except:
            response = {'EU': [], 'error': 'Error while uploading organizations.'}

        return Response(response, status=status.HTTP_200_OK)


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
        Event.objects.all().delete()
        TagP.objects.all().delete()
        Participants.objects.all().delete()
        MapIDsB2matchUpcoming.objects.all().delete()
        MapIDsB2match.objects.all().delete()
        Location.objects.all().delete()
        setUpdateSettings(b2matchDate=time.mktime(datetime.datetime.now().timetuple()))
        try:
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
        except:
            response = {'error': 'Error while adding events.'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def update_upcoming_events(self, request):
        """
                updating upcoming events in the database <not tested yet>
        """
        print("updating....")

        try:
            load_index("B2MATCH_upcoming_Index_temp")
            os.remove("B2MATCH_upcoming_Index_temp")
            os.remove("B2MATCH_upcoming_Index_temp.0")
        except:
            pass
        try:
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
                print("\t\ti =", i)

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
            print("returnd from changing event status")
            deleteEventsTree(toupdate)

            for e in toupdate:
                e.delete()

            for e in newEvents:
                try:
                    e.save()
                except:
                    print(e.event_name, "NAME EVENT")
                # e.save()

            add_Participants_from_Upcoming_Event()
            # delete old index and replace with new one
            deleteOldIndexAndReplace()
            if not setUpdateSettings(b2matchDate=time.mktime(datetime.datetime.now().timetuple())):
                raise
            response = {'success': 'B2MATCH repository updated successfully'}
        except:
            setUpdateSettings(b2matchDate=time.mktime(datetime.datetime.now().timetuple()))
            response = {'error': 'Error while updating B2match repository.'}

        return Response(response, status=status.HTTP_200_OK)


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
        try:
            events = Event.objects.all()
            for event in events:

                try:
                    url_arr = getParticipentFromUrl(
                        event.event_url)
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
                                                   org_icon_url=part_temp[6], description=part_temp[8],
                                                   location=location)

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
            response = {'success': 'Adding participant successfully.'}
        except:
            response = {'error': 'Error while adding participant'}
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
        try:
            data = request.query_params['data']
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
                                R_D_Institution=data['R_D_Institution'], Start_Up=data['Start_Up'],
                                Others=data['Others']
                                )
            scores.save()
            response = {'success': 'Scores updated successfully.'}
        except:
            response = {'error': 'Error while updating scores.'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getscores(self, request):
        """
        API to send current scoures
        :param request:
        :return:
        """
        try:
            scores = Scores.objects.all()[0]
            response = ScoresSerializer(scores).data
        except:
            response = {'error': 'Error while uploading scores.'}

        return Response(response, status=status.HTTP_200_OK)


class AlertsB2match(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EventSerializer

    @action(detail=False, methods=['GET'])
    def alertB2match(self, request):
        """
        api for alerts sends recommnded events via mail and saves them temprorarly to the database
        :param request:
        :return:
        """
        try:
            events = Event.objects.filter(is_upcoming=True)
            myEvents = []
            for event in events:
                parts = event.event_part.all()
                count = len(parts)
                if count < 50:
                    continue
                else:
                    eventScore = getScoreForEvent(parts)
                    myEvents.append((event, eventScore))
                    print(event.event_name, event.event_url, eventScore)
                    updateAlertsEvents(myEvents)

            myEvents.sort(key=operator.itemgetter(1), reverse=True)
            print(myEvents)
            alerts_settings = AlertsSettings.objects.all()[0]
            email = alerts_settings.email
            body = MIMEMultipart('alternative')
            ms = ''
            for ev in myEvents:
                ms += '<li><b>' + ev[0].event_name + '</b><a href="' + ev[0].event_url + '">' + ev[
                    0].event_url + '</a></li>'

            signature = 'Sincerly,<br>B2MATCH Event Alerts'
            html = """\
                    <html>
                      <head><h3>You have new events that might interest you</h3></head>
                      <body>
                        <ol> 
                        {}
                        </ol>
                        <br>
                        <br>
                        {}
                      </body>
                    </html>
                    """.format(ms, signature)

            response = {'success': 'Finished building recommended events successfully.'}

            content = MIMEText(html, 'html')
            body.attach(content)
            body['Subject'] = 'B2MATCH Events Alert'
            send_mail(receiver_email=email, message=body)
        except:
            response = {'error': 'Error while building recommended events.'}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getEventFromAlerts(self, request):
        """
        function to send response of events returned from alerts
        :param request:
        :return:
        """
        try:
            events = EventsForAlerts.objects.all()
            myEvents = sorted(events, key=lambda x: x.event_score, reverse=True)
            # myEvents.sort(key=event_score, reverse=True)
            response = []
            for event in myEvents:
                response.append({'event_name': event.event_name, 'event_url': event.event_url})
        except:
            response = {'error': 'Error while uploading recommended events.'}

        return Response(response, status=status.HTTP_200_OK)


def setUpdateSettings(euDate=None, b2matchDate=None):
    """
    function to update the last update settings (times)
    :param euDate: EU last update
    :param b2matchDate: B2match last update
    :return: True/False
    """

    if not b2matchDate and not euDate:
        return False

    if euDate:
        euDate = int(euDate)
    if b2matchDate:
        b2matchDate = int(b2matchDate)

    try:
        UpdateSettings.objects.get(ID=1)
        if euDate:
            UpdateSettings.objects.filter(ID=1).update(eu_last_update=euDate)
        if b2matchDate:
            UpdateSettings.objects.filter(ID=1).update(
                b2match_last_update=b2matchDate)
    except:
        updateSettings = UpdateSettings(
            eu_last_update=euDate, b2match_last_update=b2matchDate, ID=1)
        updateSettings.save()

    return True
