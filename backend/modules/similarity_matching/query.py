# Define SPARQL queries
# -----------------------------------------cricket queries-----------------------------------------
# Query to get cricket teams
query1 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Cricket) .
  ?article ns:hasCricketTeam ?team .
  ?team ns:canonicalName ?organizationName .
}
"""

# Query to get cricket players
query2 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketPlayer ?player.
  ?player ns:canonicalName ?personName
}
"""
# Query to get cricket venues
query3 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketVenue ?venue.
  ?venue ns:canonicalName ?locationName
}
"""

# Query to get cricket tournaments
query4 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketTournament ?tournement.
  ?tournement ns:canonicalName ?eventName
}
"""
# -----------------------------------------football queries-----------------------------------------
# Query to get football teams
query5 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Football) .
  ?article ns:hasFootballTeam ?team .
  ?team ns:canonicalName ?organizationName .
}
"""
# Query to get football players
query6 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Football)
  ?article ns:hasFootballPlayer ?player.
  ?player ns:canonicalName ?personName
}
"""
# Query to get football venues
query7 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketVenue ?venue.
  ?venue ns:canonicalName ?locationName
}
"""

# query to get football tournaments
query8 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Football)
  ?article ns:hasFootballTournament ?tournement.
  ?tournement ns:canonicalName ?eventName
}
"""

# ------------------------------------------OTHER SPORT  queries-----------------------------------------

query9 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Other) .
  ?article ns:hasTeam ?team .
  ?team ns:canonicalName ?organizationName .
}
"""


query10 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Other)
  ?article ns:hasPlayer ?player.
  ?player ns:canonicalName ?personName
}
"""

query11 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Other)
  ?article ns:hasVenue ?venue.
  ?venue ns:canonicalName ?locationName
}
"""

query12 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Other)
  ?article ns:hasTournament ?tournement.
  ?tournement ns:canonicalName ?eventName
}
"""

# ------------------------------------------International Politics queries-----------------------------------------
query13 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:InternationalPolitics)
  ?article ns:hasForeignOrganization ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query14 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:InternationalPolitics)
  ?article ns:hasForeignEvent ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query15 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:InternationalPolitics)
  ?article ns:hasForeignPerson ?per.
  ?per ns:canonicalName ?personName
}
"""

query16 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:InternationalPolitics)
  ?article ns:hasForeignLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""

# ------------------------------------------Domestic Politics queries-----------------------------------------

query17 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:DomesticPolitics)
  ?article ns:hasDomesticOrganization ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query18 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:DomesticPolitics)
  ?article ns:hasDomesticEvent ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query19 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:DomesticPolitics)
  ?article ns:hasDomesticPerson ?per.
  ?per ns:canonicalName ?personName
}
"""

query20 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:DomesticPolitics)
  ?article ns:hasDomesticLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""
# ------------------------------------------Tech And Innovation queries-----------------------------------------

query21 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:TechAndInnovation)
  ?article ns:hasTechCompany ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query22 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:TechAndInnovation)
  ?article ns:hasTechEvent ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query23 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:TechAndInnovation)
  ?article ns:hasTechPerson ?per.
  ?per ns:canonicalName ?personName
}
"""

query24 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:TechAndInnovation)
  ?article ns:hasTechLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""

# ------------------------------------------Research & Space queries-----------------------------------------

query25 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ResearchAndSpace)
  ?article ns:hasResearchInstitution ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query26 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ResearchAndSpace)
  ?article ns:hasResearchEvent ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query27 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ResearchAndSpace)
  ?article ns:hasResearchPerson ?per.
  ?per ns:canonicalName ?personName
}
"""

query28 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ResearchAndSpace)
  ?article ns:hasResearchLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""
# ------------------------------------------ screen & stage queries-----------------------------------------

query29 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ScreenAndStage)
  ?article ns:hasFilmProductionCompany ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query30 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ScreenAndStage)
  ?article ns:hasStageEvent ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query31 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ScreenAndStage)
  ?article ns:hasFilmDirectorActor ?per.
  ?per ns:canonicalName ?personName
}
"""

query32 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:ScreenAndStage)
  ?article ns:hasFilmLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""

# ------------------------------------------ music & arts queries-----------------------------------------

query33 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:MusicAndArts)
  ?article ns:hasMusicCompany ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query34 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:MusicAndArts)
  ?article ns:hasMusicEvent ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query35 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:MusicAndArts)
  ?article ns:hasMusicArtist ?per.
  ?per ns:canonicalName ?personName
}
"""

query36 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:MusicAndArts)
  ?article ns:hasMusicLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""

# -------------------------------------------Crime & Justice queries(common for both sub category)-----------------------------------------

query37 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?organizationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:CrimeAndJustice)
  ?article ns:hasInvestigation ?org.
  ?org ns:canonicalName ?organizationName
}
"""

query38 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?personName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:CrimeAndJustice)
  ?article ns:hasWitness ?per.
  ?per ns:canonicalName ?personName
}
"""

# -------------------------------------------crime report queries-----------------------------------------

query39 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:CrimeReport)
  ?article ns:hasCrimeType ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query40 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:CrimeReport)
  ?article ns:hasCrimeLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""


# -------------------------------------------courts & investigation queries-----------------------------------------

query41 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?eventName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:CourtsAndInvestigation)
  ?article ns:hasCourtCase ?evt.
  ?evt ns:canonicalName ?eventName
}
"""

query42 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?locationName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:CourtsAndInvestigation)
  ?article ns:hasCourtLocation ?loc.
  ?loc ns:canonicalName ?locationName
}
"""

query43 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT ?publisher
WHERE {
  ?article ns:publisherName ?publisher 
  
}
"""

query44 = """
PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>

SELECT DISTINCT ?trustSementics
WHERE {
  ?article ns:hasFullText ?trustSementics .
}
"""
