from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, Field
import httpx
import json
##### import my libraries
from gn_library import models

base_url: str = "http://data.tmsapi.com/v1.1/"
api_key: str = "kua9569t57crx43pdan75m8v"

class Lineups(BaseModel):
    lineupType: str = Field(alias='type')
    lineupDevice: Optional[str]  = Field(alias='device', default=None)
    lineupId: str = Field(alias='lineupId')
    lineupName: str = Field(alias='name')
    lineupLocation: Optional[str] = Field(alias='location', default=None)
    lineupMso: Optional[dict[str, str]] = Field(alias='mso', default=None)

class Channels(BaseModel):
    channelId: str = Field(alias="channel")
    channelCallSign: str = Field(alias="callSign")
    channelStationId: str = Field(alias="stationId")
    channelAffiliateCallSign: Optional[str] = Field(alias="affiliateCallSign", default=None)
    channelAffiliateId: Optional[str] = Field(alias="affiliateId", default=None)
    channelSecondaryAffiliateIds: Optional[str] = Field(alias="secondaryAffiliateIds", default=None)
    channelName: Optional[str] = Field(alias="name", default=None)
    channelBcastLangs: Optional[str] = Field(alias="bcastLangs", default=None)
    channelEdLangs: Optional[str] = Field(alias="edLangs", default=None)
    channelType: Optional[str] = Field(alias="type", default=None)
    channelPreferredImage: Optional[dict[str, str]] = Field(alias='preferredImage', default=None)

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

async def api_call(query_params: str):
    """
    Generic call to master API
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

    result_response = await response_list(api_response, Lineups)
    if result_response:
        print("LineUps:\n ",result_response)
    else:
        print("No Lineups for this location found")

    return result_response
    '''
    if isinstance(api_response,list) and api_response:
        lineUps = []
        lineup = {}
        all_lineups = api_response
        print(all_lineups)
        try:
            for lineup in all_lineups:
                print(type(lineup))
                lineUps.append(Lineups(**lineup))
            return lineUps
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    else:
        print("No Lineups for this location found")
        return None
    #lineup = Lineups(**test_data)
    #lineup = all_lineups[0]
    #return lineUps
    '''
@app.get("/lineup/{lineupId}")
async def lineup_detail(lineupId: str):
    """
    Returns details for a given lineup.
    """
    query_param = "lineups/" + str(lineupId) + "?"
    api_response = await api_call(query_param)
    result_response = await response_dict(api_response, Lineups)
    if result_response:
        print("Lineup details:\n ",result_response)
    else:
        print("No lineup details found")

    return result_response

    '''
    if isinstance(api_response,dict) and api_response:
        all_details = api_response
        lineupDetails = {}
        try:
            lineupDetails = Lineups(**all_details)
            print(lineupDetails)
            return lineupDetails
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    else:
        print("No Lineup details found")
        return None
    '''
@app.get("/lineup/{lineupId}/airings")
async def lineup_grid(lineupId: str):
    """
    Returns schedule airing and associated program metadata for a lineup to be contained within a TV grid. 
    Allows for up to 6 hours of schedule metadata for a given date up to 14 days in advance.
    """
    lineupAirings = []
    query_param = "lineups/" + lineupId + "/grid?startDateTime=2025-07-09T18:00Z&endDateTime=2025-07-09T18:15Z&size=basic&"
    api_response = await api_call(query_param)
    result_response = await response_list(api_response, models.Station)
    if result_response:
        print("Stations airings:\n ",result_response)
    else:
        print("No airings found on the local stations")

    return result_response
'''
    if isinstance(api_response, list) and api_response: 
        all_airings = api_response
        #print(all_airings)
        try:
            for airing in all_airings:
                print("Airing ",airing)
                lineupAirings.append(models.Station(**airing))
            return lineupAirings
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    else:
        print("No airings found")
        return None
'''
@app.get("/lineup/{lineupId}/listing")
async def lineup_channels(lineupId: str):
    """
    Returns a list of stations and channel positions associated with the lineup provided.
    """
    #api_response = {}
    #lineupListing = []
    query_param = "lineups/" + lineupId + "/channels?"
    api_response = await api_call(query_param)
    result_response = await response_list(api_response, Channels)
    if result_response:
        print("Channels available:\n ",result_response)
    else:
        print("No channels found on the local stations")

    return result_response
    '''
    if isinstance(api_response, list) and api_response: 
        all_channels = api_response
        #print(all_channels)
        try:
            for channel in all_channels:
                print(channel)
                lineupListing.append(Channels(**channel))
            return lineupListing
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    
    else:
        print("No channels found")
        return None
    '''
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
    result_response = await response_list(api_response, models.SportModel)
    if result_response:
        print("Stations airings:\n ",result_response)
    else:
        print("No airings found on the local stations")

    return result_response
'''    
    if isinstance(api_response,list):
        all_sports = api_response
        #print(all_sports)
        sportDetails = []
        try:
            for sport in all_sports:
                sportDetails.append(models.SportModel(**sport))
            print(sportDetails)
            return sportDetails
        except ValidationError as e:
            print(f"Error mapping {e}")
            return None
    else:
        print("api_response ", type(api_response))
        return None
'''