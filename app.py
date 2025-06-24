from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import httpx

"""
{
  "type": "CABLE",
  "device": "X",
  "lineupId": "USA-CA66511-X",
  "name": "AT&T U-verse TV",
  "location": "Los Angeles",
  "mso": {
    "id": "17304",
    "name": "AT&T U-verse TV"
}
"""
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
    api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=78701&api_key=kua9569t57crx43pdan75m8v"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        all_lineups = response.json()
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

async def api_call():
    pass