'''
Gracenote Models
'''

from pydantic import BaseModel, Field

class PreferredImage(BaseModel):
    width: str = Field(..., description="The width of the image in pixels.")
    height: str = Field(..., description="The height of the image in pixels.")
    uri: str = Field(..., description="The URI where the image can be accessed.")
    category: str = Field(..., description="The category of the image, e.g., Logo.")
    primary: str = Field(..., description="Indicates if this is the primary image.")

class Program(BaseModel):
    tmsId: str = Field(..., description="The unique identifier for the program.")
    rootId: str = Field(..., description="The root identifier for the program.")
    seriesId: str = Field(..., description="The series identifier for the program.")
    subType: str = Field(..., description="The subtype of the program, e.g., Series.")
    title: str = Field(..., description="The title of the program.")
    releaseYear: int = Field(..., description="The year the program was released.")
    releaseDate: str = Field(..., description="The date the program was released.")
    origAirDate: str = Field(..., description="The original air date of the program.")
    titleLang: str = Field(..., description="The language of the program title.")
    descriptionLang: str = Field(..., description="The language of the program description.")
    entityType: str = Field(..., description="The type of entity, e.g., Show.")
    genres: list[str] = Field(..., description="A list of genres the program belongs to.")
    shortDescription: str | None = Field(None, description="A short description of the program.")

class Airing(BaseModel):
    startTime: str = Field(..., description="The start time of the airing in ISO 8601 format.")
    endTime: str = Field(..., description="The end time of the airing in ISO 8601 format.")
    duration: int = Field(..., description="The duration of the airing in minutes.")
    qualifiers: list[str] = Field(..., description="A list of qualifiers for the airing, e.g., New, CC.")
    stationId: str = Field(..., description="The unique identifier for the station.")
    program: Program = Field(..., description="The program details associated with this airing.")

class Station(BaseModel):
    stationId: str = Field(..., description="The unique identifier for the station.")
    callSign: str = Field(..., description="The call sign of the station.")
    preferredImage: PreferredImage = Field(..., description="The preferred image details for the station.")
    airings: list[Airing] = Field(..., description="A list of airings scheduled on this station.")
