from django.shortcuts import render
from django.http import HttpResponse 
from .models import * #added
from django.core.exceptions import ObjectDoesNotExist #added 

#added for forms. 
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import locationForm


#added:
import requests
import json
from datetime import datetime, timedelta

# Create your views here.

def greetingView(request):
    return HttpResponse('finally code doe ssomething!')

def greetingabcd(request):
    object = Location.objects.get(country='Hong Kong')
    numbers = object.population
    #numbers += 88800000000000
    return HttpResponse(numbers) # the ultimate line that determines what is displayed. inside the views.py file 


def queryAndReturnHKCOVID(daysbehind, url, resource):
    
    #data source 
    #url = 'https://api.data.gov.hk/v2/filter?q='

    #date and time stuff 
    yesterday = datetime.now() - timedelta(daysbehind)
    yesterdayFormatted = datetime.strftime(yesterday, '%d/%m/%Y')
    #end of date and time stuff 

    #decode json filters
    mylist = [[1,"eq",["18/03/2021"]]]

    mylist[0][2][0] = yesterdayFormatted #added for yesterday


    #print(mylist[0][2][0])

    queryDict = {
        "resource" : resource, #"http://www.chp.gov.hk/files/misc/latest_situation_of_reported_cases_covid_19_eng.csv",
        "section" : 1,
        "format": "json",
        "filters": mylist 
        }

    q = json.dumps(queryDict, separators=(",", ":"))

    askfrom = url+q

    response = requests.get(askfrom)

    ########### return if response.status_code == 200. 

    if response.status_code == 200:
        #print("------------------------------")
        #parsedResponse is a dictionary, stores the response from the query. 
        parsedResponse = response.json()[0]
        #print(parsedResponse)
        parsedResponse["querySuccess"] = True
        return parsedResponse #parsedResponse contains the covid data. 
    else: 
        #createdictionary mark failed. 
        parsedResponse = {"querySuccess": False}
        #parsedResponse["querySuccess"] = False
        return parsedResponse




def covidDataGenerator (request, pk=None):

    if pk:
        object = Location.objects.get(pk=pk)
    
    else:
        try : 
            Location.objects.get(country='Hong Kong')
        except :
            restructuredDictionary = {
                "retrieveResult": False,
                "Locations": Location.objects.all(),
            }
            return render (request, 'hk.html', restructuredDictionary)
        
    



    #checking if it exists at all. 
    try : 
        Location.objects.get(country='Hong Kong')
    except :
        restructuredDictionary = {
             "retrieveResult": False,
             "Locations": Location.objects.all(),
         }
        return render (request, 'hk.html', restructuredDictionary)
    else: 
        if pk == None:
            object = Location.objects.get(country='Hong Kong')
        
        #getting from database
        #object = Location.objects.get(country='Hong Kong')


        #create list. iterate through the items. 
        parsedResponseList = ["parsed1", "parsed2", "parsed3", "parsed4", "parsed5", "parsed6", "parsed7"]



        for i in range(len(parsedResponseList)):
            #print(i)
            parsedResponseList[i] = queryAndReturnHKCOVID(i+1, object.apisource, object.resourceurl )



       

        ######################### start building a new dictionary for the response so there's no spaces. 

        if parsedResponseList[0]["querySuccess"] == True and parsedResponseList[1]["querySuccess"] == True and parsedResponseList[2]["querySuccess"] == True and parsedResponseList[3]["querySuccess"] == True and parsedResponseList[4]["querySuccess"] == True and parsedResponseList[5]["querySuccess"] == True and parsedResponseList[6]["querySuccess"] == True :
            restructuredDictionary = {
                "country": object.country,
                "asOfDate":  parsedResponseList[0]['As of date'],
                "confirmedCaseCount" : parsedResponseList[0]["Number of confirmed cases"],
                "confirmedCasePerMillion": parsedResponseList[0]["Number of confirmed cases"] / object.population * 1000000,
                "fatalitiesCount": parsedResponseList[0]["Number of death cases"],
                "fatalitiesPerMillion": parsedResponseList[0]["Number of death cases"]/ object.population * 1000000,
                "newCaseCount" : parsedResponseList[0]["Number of confirmed cases"] - parsedResponseList[1]["Number of confirmed cases"],
                "sevenDayAverageNewCaseCount" : (parsedResponseList[0]["Number of confirmed cases"] - parsedResponseList[6]["Number of confirmed cases"])/7,
                "newFatalitiesCount": parsedResponseList[0]["Number of death cases"] - parsedResponseList[1]["Number of death cases"],
                "sevenDayAverageNewFatalitiesCount": (parsedResponseList[0]["Number of death cases"] - parsedResponseList[6]["Number of death cases"])/7,
                "retrieveResult": parsedResponseList[0]["querySuccess"],
                "Locations": Location.objects.all(),
                }
        else: 
            restructuredDictionary = {
                "retrieveResult": False,
                "Locations": Location.objects.all(),
            }
        
        
        return render (request, 'hk.html', restructuredDictionary)



def showAllCountries (request):
    context={}

    context["Locations"] = Locations.objects.all()
    return render(request,"all.html", context)




def createLocation(request):
    if request.method == 'POST':
        #create form instance
        form = locationForm(request.POST)
        if form.is_valid():
            countryf = form.cleaned_data['countryName']
            apisourcef = form.cleaned_data['apisource']
            resourceurlf = form.cleaned_data['resourceurl']
            populationf = form.cleaned_data['population']
            #print("entered form loop")
            #print(countryf, apisourcef, resourceurlf, populationf)
            newlocation = Location(country = countryf, apisource = apisourcef, resourceurl = resourceurlf, population = populationf)
            newlocation.save()
            #Location.objects.add(country = countryf, apisource = apisourcef, resourceurl = resourceurlf, population = populationf)
            return HttpResponseRedirect('/')
    
    else: 
        form = locationForm()
    
    return render(request, 'form.html', {'form': form})