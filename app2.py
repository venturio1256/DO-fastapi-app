from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
import httpx    
import json
##### import my libraries
from gn_library import models2

base_url: str = "http://data.tmsapi.com/v1.1/"
api_key: str = "kua9569t57crx43pdan75m8v"

test_data = {
        "type": "VMVPD",
        "device": "X",
        "lineupId": "USA-HULU751-X",
        "name": "Hulu Denver",
        "location": "Denver",
        "mso": {
            "id": "17842",
            "name": "Hulu"
        }
    }

tools = [
{
    "type": "function",
    "function": {
        "name": "get_lineup_details",
        "description": "Returns details for a given lineup",
        "parameters": {
            "type": "object",
            "properties": {
                "lineupId": {
                    "type": "string",
                    "description": "The lineup id."
                }
            },
            "required": ["lineupId"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_lineup_grid",
        "description": "Returns schedule airing and associated program metadata for a lineup to be contained within a TV grid. \nAllows for up to 6 hours of schedule metadata for a given date up to 14 days in advance.",
        "parameters": {
            "type": "object",
            "properties": {
                "lineupId": {
                    "type": "string",
                    "description": "The lineup id."
                }
            },
            "required": ["lineupId"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "get_lineup_listing",
        "description": "Returns a list of stations and channel positions associated with the lineup provided.",
        "parameters": {
            "type": "object",
            "properties": {
                "lineupId": {
                    "type": "string",
                    "description": "The lineup id."
                }
            },
            "required": ["lineupId"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_sports_details",
        "description": "Returns all (or specified) sports details with associated organizations.",
        "parameters": {
            "type": "object",
            "properties": {
                "SportId": {
                    "type": "string",
                    "description": "The sports Ids."
                }
            },
            "required": ["SportId"]
        }
    }
}

    
]

async def api_call(query_params: str):
    """
    Master function call to external API
    """
    q_api_key = "api_key=" + api_key
    api_url = base_url + query_params + q_api_key
    print(api_url)
    
    #api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=80230&api_key=kua9569t57crx43pdan75m8v"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        print(response)
    if response.status_code == 200:
        return response.json()
    else:
        error_response = {"Error api call": response.status_code}
        return json.dumps(error_response)
    #return response.json()

async def response_list(api_response, model):
    '''
    Handling of the API response in List format.
    return the JSON under List object based on BaseModel
    '''
    if isinstance(api_response,list) and api_response:
        respList = []
        respDict = {}
        apilists = api_response
        print(apilists)
        try:
            for respDict in apilists:
                print(type(respDict))
                respList.append(model(**respDict))
            return respList
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    else:
        print("No list found")
        return None
        
async def response_dict(api_response, model):
    '''
    Handling of the API response in dictionary format.
    return the JSON under List object based on BaseModel
    '''
    if isinstance(api_response,dict) and api_response:
        respDict = {}
        apidicts = api_response
        try:
            respDict = model(**apidicts)
            print(type(respDict))
            return respDict
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    else:
        print("No details found")
        return None


app = FastAPI()

@app.get("/")
async def root():
    '''Welcome message for the API root endpoint.''' 
    return {"message": "Welcome to venturio Labs/v1/test "}

@app.get("/zipcode/{zipcode}")
async def lineups_zipcode(zipcode: int):
    """
    Returns a list of lineups for a country and postal code.
    """
    print(zipcode)
    query_param = "lineups?country=USA&postalCode=" + str(zipcode) + "&"
    print(query_param)
    api_response = await api_call(query_param)

    result_response = await response_list(api_response, models2.Lineup)
    if result_response:
        print("LineUps:\n ",result_response)
    else:
        print("No Lineups for this location found")

    return result_response

@app.get("/lineup/{lineupId}")
async def lineup_detail(lineupId: str):
    """
    Returns details for a given lineup.
    """
    query_param = "lineups/" + str(lineupId) + "?"
    api_response = await api_call(query_param)
    result_response = await response_dict(api_response, models2.Lineup)
    if result_response:
        print("Lineup details:\n ",result_response)
    else:
        print("No lineup details found")

    return result_response


@app.get("/lineup/{lineupId}/airings")
async def lineup_grid(lineupId: str):
    """
    Returns schedule airing and associated program metadata for a lineup to be contained within a TV grid. 
    Allows for up to 6 hours of schedule metadata for a given date up to 14 days in advance.
    """
    lineupAirings = []
    query_param = "lineups/" + lineupId + "/grid?startDateTime=2025-10-01T00:00Z&endDateTime=2025-10-03T01:00Z&size=basic&stationId=10035&"
    api_response = await api_call(query_param)
    result_response = await response_list(api_response, models2.Station)
    if result_response:
        print("Stations airings:\n ",result_response)
    else:
        print("No airings found on the local stations")

    return result_response

@app.get("/lineup/{lineupId}/listing")
async def lineup_channels(lineupId: str):
    """
    Returns a list of stations and channel positions associated with the lineup provided.
    """
    #api_response = {}
    #lineupListing = []
    query_param = "lineups/" + lineupId + "/channels?"
    api_response = await api_call(query_param)
    result_response = await response_list(api_response, models2.LineupChannel)
    if result_response:
        print("Channels available:\n ",result_response)
    else:
        print("No channels found on the local stations")

    return result_response

@app.get("/sports/{SportId}")
async def sport_detail(SportId:str):
    """
    Returns all (or specified) sports with associated organizations.
    """
    sports = SportId.split(",")
    if sports:
        query_param = "sports/" + str(SportId) + "?includeOrg=true&"
    else:
        query_param = "sports/all?includeOrg=true&"
    api_response = await api_call(query_param)
    result_response = await response_list(api_response, models2.Sport)
    if result_response:
        print("Stations airings:\n ",result_response)
    else:
        print("No airings found on the local stations")

    return result_response

@app.get("/sports/{SportId}/events/airings?lineupId={lineupId}")
async def sports_grid(SportId:str, lineupId:str):
    """
    Returns schedule airing and associated program metadata for one or several sports to be contained within a TV grid. 
    Allows for up to 6 hours of schedule metadata for a given date up to 14 days in advance.
    """
    print(lineupId, SportId)
    sports = SportId.split(",")
    if sports:
        query_param = "sports/" + str(SportId) + "/events/airings?lineupId=" + lineupId
    else:
        query_param = "sports/all/events/airings?lineupId=" + lineupId
    query_param += "&startDateTime=2025-10-01T00:00Z&endDateTime=2025-10-03T01:00Z&liveOnly=true&"
    print(query_param)
    api_response = await api_call(query_param)
    result_response = await response_list(api_response, models2.SportAiring)
    if result_response:
        print("Sports airings:\n ",result_response)
    else:
        print("No sports airings found on the local stations")

    return result_response
