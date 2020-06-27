import requests
from .NLP import *
from ..models import MapIds, OrganizationProfile, Tag, Address, CallTag, Call
from dateutil.relativedelta import relativedelta
import time
from datetime import datetime
from .Utils import *

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

    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/api/orgProfile/publicProjects.json?pic=' + \
          str(pic)
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
    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/api/orgProfile/data.json?pic=' + \
          str(pic)
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

    resObj['numberOfProjects'] = getNumOfProjects(
        obj['publicOrganizationData']['pic'])
    resObj['consorsiumRoles'] = True if 'COORDINATOR' in resObj['consorsiumRoles'] else False
    resObj['pic'] = int(resObj['pic'])

    return resObj


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
    try:
        MapIds.objects.filter(indexID=indexID).delete()
    except:
        pass

    try:
        MapIds.objects.get(originalID=originalID)
        MapIds.objects.filter(originalID=originalID).update(indexID=indexID)
    except:
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


# ----------------------- Processing query in EU data Funcs ------------------------
def getOrgsByTags(tags):
    """
    method to get all organizations with at least one tag from the list of tags.
    :param tags: list of tags
    :return: list of organizations objects
    """
    tags = ' '.join(tags)
    index = load_index('EU_Index.0')
    corpus = NLP_Processor([tags])
    res = index[corpus]
    res = process_query_result(res)
    res = [pair for pair in res if pair[1] > 0.3]
    res = sorted(res, key=lambda pair: pair[1], reverse=True)
    # res = res[:100]
    res = [MapIds.objects.get(indexID=pair[0]) for pair in res]

    finalRes = []
    for mapId in res:
        finalRes.append(OrganizationProfile.objects.get(pic=mapId.originalID))
    print(finalRes)
    return finalRes


def getOrganizationsByCountries(countries):
    """
    method to get all organizations that locates in one of the countries list.
    :param countries: list of countries
    :return: list of organizations objects
    """
    if not countries:
        return OrganizationProfile.objects.all()
    return OrganizationProfile.objects.filter(address__country__in=countries)


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


# ----------------------- Consortium builder for open EU calls Funcs ---------------

LIST_OF_CALLS_ATTRIBUTES = {'type', 'status', 'ccm2Id', 'identifier', 'title', 'callTitle',
                            'deadlineDatesLong', 'tags', 'keywords', 'sumbissionProcedure'}

REST_ATTRIBUTES = {'description', 'conditions',
                   'ccm2Id', 'focusArea', 'supportInfo', 'actions'}


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
    #TODO: change sumbission to submission
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
                check_dates = [is_valid_date(date)
                               for date in obj['deadlineDatesLong']]
            except:
                continue

            if any(check_dates) and is_valid_status(obj) and is_relevant_action(obj):
                obj = get_call_to_save(obj)
                grants.append(obj)

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
        Call.objects.get(ccm2Id=call['ccm2Id'])
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
