from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import httpx

base_url: str = "http://data.tmsapi.com/v1.1/"
api_key: str = "kua9569t57crx43pdan75m8v"

class Lineups(BaseModel):
    lineupType: str = Field(alias='type')
    lineupDevice: str = Field(alias='device', default=None)
    lineupId: str = Field(alias='lineupId')
    lineupName: str = Field(alias='name')
    lineupLocation: str = Field(alias='location', default=None)
    lineupMso: dict[str, str] = Field(alias='mso', default=None)

class Channels(BaseModel):
    channelId: str = Field(alias="channel")
    channelCallSign: str = Field(alias="callSign")
    channelStationId: str = Field(alias="stationId")
    channelAffiliateCallSign: str = Field(alias="affiliateCallSign", default=None)
    channelAffiliateId: str = Field(alias="affiliateId", default=None)
    channelSecondaryAffiliateIds: str = Field(alias="secondaryAffiliateIds", default=None)
    channelName: str = Field(alias="name", default=None)
    channelBcastLangs: str = Field(alias="bcastLangs", default=None)
    channelEdLangs: str = Field(alias="edLangs", default=None)
    channelType: str = Field(alias="type", default=None)
    channelPreferredImage: dict[str, str] = Field(alias='preferredImage', default=None)

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
        return response
    else:
        return {"Error api call":{response.status_code}}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to venturio Labs/v1/test "}

@app.get("/zipcode/{zipcode}")
async def lineups_zipcode(zipcode: int):
    print(zipcode)
    lineUps = []
    query_param = "lineups?country=USA&postalCode=" + str(zipcode) + "&"
    print(query_param)
    api_response = await api_call(query_param)
    #api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=78701&api_key=kua9569t57crx43pdan75m8v"
    #async with httpx.AsyncClient() as client:
    #    response = await client.get(api_url)
    all_lineups = api_response.json()
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
    all_details = api_response.json()
    lineupDetails = Lineups(**all_details)
    print(lineupDetails)
    return lineupDetails

@app.get("/lineup/{lineupId}/airings")
async def lineup_grid(LineupId: int):
    pass

@app.get("/lineup/{lineupId}/listing")
async def lineup_channels(lineupId: int):
    lineupListing = []
    query_param = "lineups/" + str(lineupId) + "/channels?"
    api_response = await api_call(query_param)
    all_channels = api_response.json()
    if all_channels: 
        print(all_channels)
        for channel in all_channels:
            print(channel)
            lineupListing.append(Channels(**channel))
    else:
        print("No channels found")
    return lineupListing

