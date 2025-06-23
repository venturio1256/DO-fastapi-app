from fastapi import FastAPI
from pydantic import BaseModel, Field

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
    lineup = Lineups(**test_data)
    return lineup