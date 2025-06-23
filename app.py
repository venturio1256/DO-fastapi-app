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
    lineupDevice: str = Field(alias='device')
    lineupId: str = Field(alias='lineupId')
    lineupName: str = Field(alias='name')
    lineupLocation: str = Field(alias='location')
    lineupMso: dict[str, str] = Field(alias='mso')

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
    api_url = "http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=78701&api_key=kua9569t57crx43pdan75m8v"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        all_lineups = response.json()
    if all_lineups:
        print(all_lineups)
    else:
        print("No LineUps found")
    #lineup = Lineups(**test_data)
    return lineup

async def api_call():
    pass