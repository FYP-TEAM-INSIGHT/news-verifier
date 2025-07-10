"""
schema.py  ── vocabulary builder for the Sinhala-news ontology
Call `schema.build_all(my_onto)` exactly **once** on a fresh Owlready2
ontology instance.

"""

from datetime import datetime
from owlready2 import Thing, DataProperty, ObjectProperty, FunctionalProperty

# ───────────────────────────────────────────────────────────
#  Core hierarchy
# ───────────────────────────────────────────────────────────


def _core_classes(onto):
    with onto:

        class NewsArticle(Thing):
            pass

        class NewsCategory(Thing):
            pass

        class NamedEntity(Thing):
            pass

        class Statement(Thing):
            pass

        class NewsVerb(Thing):
            pass

        class NewsOccurDuration(Thing):
            pass

    return onto


def _named_entity_subclasses(onto):
    with onto:

        class Person(onto.NamedEntity):
            pass

        class Organization(onto.NamedEntity):
            pass

        class Location(onto.NamedEntity):
            pass

        class Event(onto.NamedEntity):
            pass

    return onto


# ───────────────────────────────────────────────────────────
#  Top-level news categories  (+ immediate sub-categories)
# ───────────────────────────────────────────────────────────


def _news_categories(onto):
    with onto:
        # main branches
        class PoliticsAndGovernance(onto.NewsCategory):
            pass

        class ScienceAndTechnology(onto.NewsCategory):
            pass

        class CultureAndEntertainment(onto.NewsCategory):
            pass

        class Sports(onto.NewsCategory):
            pass

        class CrimeAndJustice(onto.NewsCategory):
            pass

        # sub-branches
        class InternationalPolitics(PoliticsAndGovernance):
            pass

        class DomesticPolitics(PoliticsAndGovernance):
            pass

        class TechAndInnovation(ScienceAndTechnology):
            pass

        class ResearchAndSpace(ScienceAndTechnology):
            pass

        class ScreenAndStage(CultureAndEntertainment):
            pass

        class MusicAndArts(CultureAndEntertainment):
            pass

        class Cricket(Sports):
            pass

        class Football(Sports):
            pass

        class Other(Sports):
            pass

        class CrimeReport(CrimeAndJustice):
            pass

        class CourtsAndInvestigation(CrimeAndJustice):
            pass

    return onto


# ───────────────────────────────────────────────────────────
#  Generic data-properties
# ───────────────────────────────────────────────────────────


def _article_data_props(onto):
    with onto:

        class hasTitle(DataProperty, FunctionalProperty):
            range = [str]

        class hasFullText(DataProperty):
            range = [str]

        class hasPublicationDate(DataProperty, FunctionalProperty):
            range = [datetime]

        class hasSourceURL(DataProperty, FunctionalProperty):
            range = [str]

        class processedDate(DataProperty, FunctionalProperty):
            range = [datetime]

        class publisherName(DataProperty):
            range = [str]

    return onto


def _named_entity_data_props(onto):
    with onto:

        class canonicalName(DataProperty, FunctionalProperty):
            range = [str]

        class alias(DataProperty):
            range = [str]

    return onto


def _statement_props(onto):
    with onto:
        # literal data
        class hasPredicateVerb(DataProperty, FunctionalProperty):
            range = [str]

        class sourceSentence(DataProperty):
            range = [str]

        # links
        class hasSubject(ObjectProperty, FunctionalProperty):
            range = [onto.NamedEntity]

        class hasActionVerb(ObjectProperty, FunctionalProperty):
            range = [onto.NewsVerb]

        class hasCategory(ObjectProperty):
            range = [onto.NewsCategory]

        class hasSubCategory(ObjectProperty):
            range = [
                onto.InternationalPolitics,
                onto.DomesticPolitics,
                onto.TechAndInnovation,
                onto.ResearchAndSpace,
                onto.ScreenAndStage,
                onto.MusicAndArts,
                onto.Cricket,
                onto.Football,
                onto.Other,
                onto.CrimeReport,
                onto.CourtsAndInvestigation,
            ]

        class mentionsEntity(ObjectProperty):
            range = [onto.NamedEntity]

        class containsStatement(ObjectProperty):
            range = [onto.Statement]

        # statement-object helpers
        class hasStatementSubject(ObjectProperty, FunctionalProperty):
            range = [onto.NamedEntity]

        class hasStatementObjectEntity(ObjectProperty, FunctionalProperty):
            range = [onto.NamedEntity]

        class hasStatementObjectLiteral(DataProperty, FunctionalProperty):
            range = [str]

    return onto


# ───────────────────────────────────────────────────────────
#  Politics & Governance domain-specific properties
# ───────────────────────────────────────────────────────────


def _politics_props(onto):
    with onto:
        # ── international ──────────────────────────
        class hasForeignOrganization(ObjectProperty):
            range = [onto.Organization]

        class hasForeignEvent(ObjectProperty):
            range = [onto.Event]

        class hasForeignPerson(ObjectProperty):
            range = [onto.Person]

        class hasForeignLocation(ObjectProperty):
            range = [onto.Location]

        # ── domestic ──────────────────────────
        class hasDomesticOrganization(ObjectProperty):
            range = [onto.Organization]

        class hasDomesticEvent(ObjectProperty):
            range = [onto.Event]

        class hasDomesticPerson(ObjectProperty):
            range = [onto.Person]

        class hasDomesticLocation(ObjectProperty):
            range = [onto.Location]

    return onto


# ───────────────────────────────────────────────────────────
#  Science & Technology
# ───────────────────────────────────────────────────────────


def _science_props(onto):
    with onto:
        # ── Tech & Innovation ──────────────────────────
        class hasTechCompany(ObjectProperty):
            range = [onto.Organization]

        class hasTechEvent(ObjectProperty):
            range = [onto.Event]

        class hasTechPerson(ObjectProperty):
            range = [onto.Person]

        class hasTechLocation(ObjectProperty):
            range = [onto.Location]

        # ── Research & Space ───────────────────────────
        class hasResearchInstitution(ObjectProperty):
            range = [onto.Organization]

        class hasResearchPerson(ObjectProperty):
            range = [onto.Person]

        class hasResearchEvent(ObjectProperty):
            range = [onto.Event]

        class hasResearchLocation(ObjectProperty):
            range = [onto.Location]

    return onto


# ───────────────────────────────────────────────────────────
#  Culture & Entertainment
# ───────────────────────────────────────────────────────────


def _culture_props(onto):
    with onto:
        # screen & stage
        class hasFilmDirectorActor(ObjectProperty):
            range = [onto.Person]

        class hasFilmProductionCompany(ObjectProperty):
            range = [onto.Organization]

        class hasStageEvent(ObjectProperty):
            range = [onto.Event]

        class hasFilmLocation(ObjectProperty):
            range = [onto.Location]

        # music & arts
        class hasMusicArtist(ObjectProperty):
            range = [onto.Person]

        class hasMusicCompany(ObjectProperty):
            range = [onto.Organization]

        class hasMusicEvent(ObjectProperty):
            range = [onto.Event]

        class hasMusicLocation(ObjectProperty):
            range = [onto.Location]

    return onto


# ───────────────────────────────────────────────────────────
#  Sports
# ───────────────────────────────────────────────────────────


def _sports_props(onto):
    with onto:
        # cricket
        class hasCricketTeam(ObjectProperty):
            range = [onto.Organization]

        class hasCricketPlayer(ObjectProperty):
            range = [onto.Person]

        class hasCricketVenue(ObjectProperty):
            range = [onto.Location]

        class hasCricketTournament(ObjectProperty):
            range = [onto.Event]

        # football
        class hasFootballTeam(ObjectProperty):
            range = [onto.Organization]

        class hasFootballPlayer(ObjectProperty):
            range = [onto.Person]

        class hasFootballVenue(ObjectProperty):
            range = [onto.Location]

        class hasFootballTournament(ObjectProperty):
            range = [onto.Event]

        # catch-all other sports
        class hasTeam(ObjectProperty):
            range = [onto.Organization]

        class hasPlayer(ObjectProperty):
            range = [onto.Person]

        class hasVenue(ObjectProperty):
            range = [onto.Location]

        class hasTournament(ObjectProperty):
            range = [onto.Event]

    return onto


# ───────────────────────────────────────────────────────────
#  Crime & Justice
# ───────────────────────────────────────────────────────────


def _crime_props(onto):
    with onto:

        class hasWitness(ObjectProperty):
            range = [onto.Person]

        class hasInvestigation(ObjectProperty):
            range = [onto.Organization]

        # crime report
        class hasCrimeType(ObjectProperty):
            range = [onto.Event]

        class hasCrimeLocation(ObjectProperty):
            range = [onto.Location]

        # courts & investigation
        class hasCourtCase(ObjectProperty):
            range = [onto.Event]

        class hasCourtLocation(ObjectProperty):
            range = [onto.Location]

    return onto


# ───────────────────────────────────────────────────────────
#  Master builder
# ───────────────────────────────────────────────────────────


def build_all(onto):
    """
    Assemble the entire vocabulary on a *new* Owlready ontology.
    Call once, immediately after creating the ontology object.
    """
    for fn in (
        _core_classes,
        _named_entity_subclasses,
        _news_categories,
        _article_data_props,
        _named_entity_data_props,
        _statement_props,
        _politics_props,
        _science_props,
        _culture_props,
        _sports_props,
        _crime_props,
    ):
        fn(onto)
    return onto
