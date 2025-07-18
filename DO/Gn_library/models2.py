'''
Gracenote enhanced Models
'''
from typing import List, Optional, Any
from pydantic import BaseModel, Field
import datetime

# --- Pydantic Models ---

class Mso(BaseModel):
    """Pydantic model for MSO (Multiple System Operator)."""
    id: Optional[str] = None
    name: Optional[str] = None

class VideoQuality(BaseModel):
    """Pydantic model for video quality details."""
    signalType: Optional[str] = None
    truResolution: Optional[str] = None
    videoType: Optional[str] = None

class PreferredImage(BaseModel):
    """Pydantic model for preferred image details."""
    width: Optional[str] = None
    height: Optional[str] = None
    uri: Optional[str] = None
    category: Optional[str] = None
    primary: Optional[str] = None
    text: Optional[str] = None
    tier: Optional[str] = None

class Team(BaseModel):
    """Pydantic model for team details."""
    teamBrandId: Optional[str] = None
    name: Optional[str] = None
    teamId: Optional[str] = None
    sportsId: Optional[str] = None
    teamBrandName: Optional[str] = None
    nickName: Optional[str] = None
    properName: Optional[str] = None
    abbreviation: Optional[str] = None

class Program(BaseModel):
    """Pydantic model for program details."""
    tmsId: str
    rootId: str
    seriesId: str
    subType: str
    title: str
    releaseYear: Optional[int] = None
    releaseDate: Optional[str] = None
    origAirDate: Optional[str] = None
    titleLang: str
    descriptionLang: str
    entityType: str
    longDescription: Optional[str] = None
    shortDescription: Optional[str] = None
    preferredImage: Optional[PreferredImage] = None
    organizationId: Optional[str] = None
    sportsId: Optional[str] = None
    teams: Optional[List[Team]] = None
    eventTitle: Optional[str] = None
    gameDate: Optional[str] = None
    gameTime: Optional[str] = None
    gameTimeZone: Optional[str] = None
    genres: Optional[List[str]] = None
    episodeTitle: Optional[str] = None
    season: Optional[dict] = None

class Airing(BaseModel):
    """Pydantic model for airing details."""
    startTime: datetime.datetime
    endTime: datetime.datetime
    duration: int
    qualifiers: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    stationId: str
    program: Program

class Lineup(BaseModel):
    """Pydantic model for lineup details."""
    type: str
    device: Optional[str] = None
    lineupId: str
    name: str
    location: Optional[str] = None
    mso: Optional[Mso] = None

class LineupChannel(BaseModel):
    """Pydantic model for a channel in a lineup."""
    stationId: str
    callSign: str
    videoQuality: Optional[VideoQuality] = None
    affiliateCallSign: Optional[str] = None
    affiliateId: Optional[str] = None
    channel: str
    preferredImage: Optional[PreferredImage] = None

class LineupAiring(BaseModel):
    """Pydantic model for airings in a lineup."""
    stationId: str
    callSign: str
    channel: Optional[str] = None
    videoQuality: Optional[VideoQuality] = None
    preferredImage: Optional[PreferredImage] = None
    airings: Optional[List[Airing]] = None

class Station(BaseModel):
    """Pydantic model for station details."""
    stationId: str
    callSign: Optional[str] = None
    name: Optional[str] = None
    bcastLangs: Optional[List[str]] = None
    edLangs: Optional[List[str]] = None
    type: Optional[str] = None
    videoQuality: Optional[VideoQuality] = None
    affiliateCallSign: Optional[str] = None
    affiliateId: Optional[str] = None
    channel: Optional[str] = None
    preferredImage: Optional[PreferredImage] = None

class StationAiring(BaseModel):
    """Pydantic model for airings on a station."""
    startTime: datetime.datetime
    endTime: datetime.datetime
    duration: int
    qualifiers: Optional[List[str]] = None
    program: Program
    station: Station

class Organization(BaseModel):
    """Pydantic model for organization details."""
    organizationId: str
    organizationName: str
    preferredImage: Optional[PreferredImage] = None
    officialOrg: Optional[bool] = None

class Sport(BaseModel):
    """Pydantic model for sport details."""
    sportsId: str
    sportsName: str
    organizations: Optional[List[Organization]] = None

class SportAiring(BaseModel):
    """Pydantic model for sports airings."""
    startTime: datetime.datetime
    endTime: datetime.datetime
    duration: int
    qualifiers: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    program: Program
    stationId: str
    station: Station

class SportNonEventAiring(BaseModel):
    """Pydantic model for airings of sports non-events."""
    startTime: datetime.datetime
    endTime: datetime.datetime
    duration: int
    channels: Optional[List[str]] = None
    program: Program
    stationId: str
    station: Station

class University(BaseModel):
    """Pydantic model for university details."""
    universityId: str
    universityName: str
    nickName: Optional[str] = None
    preferredImage: Optional[PreferredImage] = None

class OrganizationTeam(BaseModel):
    """Pydantic model for a team in an organization."""
    width: Optional[str] = None
    height: Optional[str] = None
    uri: Optional[str] = None
    category: Optional[str] = None
    text: Optional[str] = None
    primary: Optional[str] = None
    tier: Optional[str] = None
    teamBrandId: Optional[str] = None
    teamId: Optional[str] = None
    sportsId: Optional[str] = None
    teamBrandName: Optional[str] = None
    nickName: Optional[str] = None
    properName: Optional[str] = None
    abbreviation: Optional[str] = None

class UniversityTeam(BaseModel):
    """Pydantic model for a team at a university."""
    teamBrandId: str
    teamId: str
    sportsId: str
    teamBrandName: str
    nickName: str
    properName: str
    abbreviation: str
    university: University
    preferredImage: Optional[PreferredImage] = None

class TeamDetail(BaseModel):
    """Pydantic model for detailed team information."""
    teamBrandId: str
    teamId: str
    sportsId: str
    teamBrandName: str
    nickName: str
    properName: str
    abbreviation: str
    university: Optional[University] = None
    preferredImage: Optional[PreferredImage] = None

class TeamAiring(BaseModel):
    """Pydantic model for team airings."""
    startTime: datetime.datetime
    endTime: datetime.datetime
    duration: int
    qualifiers: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    program: Program
    stationId: str
    station: Station

class OrganizationAiring(BaseModel):
    """Pydantic model for organization airings."""
    startTime: datetime.datetime
    endTime: datetime.datetime
    duration: int
    qualifiers: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    program: Program
    stationId: str
    station: Station
