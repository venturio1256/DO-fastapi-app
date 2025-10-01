'''
Gracenote Models
'''
from typing import List, Optional
from pydantic import BaseModel, Field

class OrgImageModel(BaseModel):
    """Defines the structure of the 'preferredImage' object within an organization."""
    uri: str = Field(description="The URI for the organization's preferred logo or image.")

class OrganizationModel(BaseModel):
    """Defines the structure of an 'organization' object."""
    organizationId: str = Field(description="The unique identifier for the sports organization.")
    organizationName: str = Field(description="The full name of the sports organization (e.g., 'King Super Cup').")
    preferredImage: OrgImageModel = Field(description="The preferred logo for the organization.")
    officialOrg: bool = Field(description="A boolean flag indicating if this is an official organization.")

class SportModel(BaseModel):
    """Defines the top-level object for a single sport."""
    sportsId: str = Field(description="The unique identifier for the sport.")
    sportsName: str = Field(description="The name of the sport (e.g., 'Soccer', 'Archery').")
    
    # This field is optional. We set `default=None` to indicate that it
    # may not be present in all Sport objects.
    organizations: Optional[List[OrganizationModel]] = Field(
        default=None,
        description="A list of organizations associated with this sport. This may be null."
    )


class PreferredImage(BaseModel):
    width: Optional[str] = Field(default=None, description="The width of the image in pixels.")
    height: Optional[str] = Field(default=None, description="The height of the image in pixels.")
    uri: Optional[str] = Field(default=None, description="The URI where the image can be accessed.")
    category: Optional[str] = Field(default=None, description="The category of the image, e.g., Logo.")
    primary: Optional[str] = Field(default=None, description="Indicates if this is the primary image.")

class Program(BaseModel):
    tmsId: str = Field(description="The unique identifier for the program.")
    rootId: str = Field(description="The root identifier for the program.")
    seriesId: Optional[str] = Field(default=None, description="The series identifier for the program.")
    subType: str = Field(description="The subtype of the program, e.g., Series.")
    title: str = Field(description="The title of the program.")
    releaseYear: Optional[int] = Field(default=None, description="The year the program was released.")
    releaseDate: Optional[str] = Field(default=None, description="The date the program was released.")
    origAirDate: Optional[str] = Field(default=None, description="The original air date of the program.")
    titleLang: str = Field(description="The language of the program title.")
    descriptionLang: Optional[str] = Field(default=None, description="The language of the program description.")
    entityType: str = Field(description="The type of entity, e.g., Show.")
    genres: List[str] = Field(default_factory=list, description="A list of genres the program belongs to.")
    shortDescription: Optional[str] = Field(default=None, description="A short description of the program.")

class Airing(BaseModel):
    startTime: str = Field(description="The start time of the airing in ISO 8601 format.")
    endTime: str = Field(description="The end time of the airing in ISO 8601 format.")
    duration: int = Field(description="The duration of the airing in minutes.")
    qualifiers: List[str] = Field(default_factory=list, description="A list of qualifiers for the airing, e.g., New, CC.")
    stationId: str = Field(description="The unique identifier for the station.")
    program: Program = Field(description="The program details associated with this airing.")

class Station(BaseModel):
    stationId: str = Field(description="The unique identifier for the station.")
    callSign: str = Field(description="The call sign of the station.")
    preferredImage: PreferredImage = Field(description="The preferred image details for the station.")
    airings: List[Airing] = Field(default_factory=list, description="A list of airings scheduled on this station.")
