from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
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

    q_api_key = "api_key=" + api_key
    api_url = base_url + query_params + q_api_key
    print(api_url)
    
    #api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=80230&api_key=kua9569t57crx43pdan75m8v"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
    if response.status_code == 200:
        api_response = response.json()
    else:
        api_response = json.dumps({"Error api call":{response.status_code}})
    return response.json()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to venturio Labs/v1/test "}

@app.get("/zipcode/{zipcode}")
async def lineups_zipcode(zipcode: int):
    api_response = {}
    print(zipcode)
    lineUps = []
    query_param = "lineups?country=USA&postalCode=" + str(zipcode) + "&"
    print(query_param)
    api_response = await api_call(query_param)
    #api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=78701&api_key=kua9569t57crx43pdan75m8v"
    #async with httpx.AsyncClient() as client:
    #    response = await client.get(api_url)
    all_lineups = api_response
    if all_lineups: 
        print(all_lineups)
        for lineup in all_lineups:
            print(lineup)
            lineUps.append(Lineups(**lineup))
    else:
        print("No LineUps found")
    #lineup = Lineups(**test_data)
    #lineup = all_lineups[0]
    return lineUps

@app.get("/lineup/{lineupId}")
async def lineup_detail(lineupId: str):
    query_param = "lineups/" + str(lineupId) + "?"
    api_response = await api_call(query_param)
    all_details = api_response
    lineupDetails = Lineups(**all_details)
    print(lineupDetails)
    return lineupDetails

@app.get("/sports/{SportId}")
async def lineup_detail(SportId:str):
    sports = SportId.split(",")
    if sports:
        query_param = "sports/" + str(SportId) + "?"
    else:
        query_param = "sports/all?"
    api_response = await api_call(query_param)
    all_sports = api_response
    sportDetails = SportModel(**all_sports)
    print(sportDetails)
    return sportDetails

@app.get("/lineup/{lineupId}/airings")
async def lineup_grid(lineupId: str):
    lineupAirings = []
    query_param = "lineups/" + lineupId + "/grid?startDateTime=2025-06-25T18:00Z&endDateTime=2025-06-25T18:15Z&size=basic&"
    api_response = await api_call(query_param)
    all_airings = api_response
    if all_airings: 
        print(all_airings)
        for airing in all_airings:
            print("Airing ",airing)
            lineupAirings.append(models.Station(**airing))
    else:
        print("No channels found")
    return lineupAirings

@app.get("/lineup/{lineupId}/listing")
async def lineup_channels(lineupId: str):
    api_response = {}
    lineupListing = []
    query_param = "lineups/" + lineupId + "/channels?"
    api_response = await api_call(query_param)
    all_channels = api_response
    if all_channels: 
        print(all_channels)
        for channel in all_channels:
            print(channel)
            lineupListing.append(Channels(**channel))
    else:
        print("No channels found")
    return lineupListing

