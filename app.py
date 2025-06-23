from fastapi import FastAPI
from pydantic import BaseModel

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
    lineupType: str
    lineupDevice: str
    lineupId: str
    lineupName: str
    lineupLocation: str
    lineupMso: dict[str, str] = {}

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
    lineup = Lineups(**test_data)
    return lineup