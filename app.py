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

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to venturio Labs/v1/test "}

@app.get("/zipcode/{zipcode}")
async def lineups_zipcode(zipcode: int):
    print(zipcode)
    lineUps = []
    query_param = "lineups?country=USA&postalCode=" + str(zipcode)
    api_response = api_call(base_url, query_param, api_key)
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

async def api_call(base_url: str, api_key: str, query_params: str):
    q_api_key = "&api_key=" + api_key
    api_url = base_url + query_params + q_api_key
    #api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=78701&api_key=kua9569t57crx43pdan75m8v"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)    
    return response