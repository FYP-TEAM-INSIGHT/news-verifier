# ontology_populator.py
from datetime import datetime
from .models import FormattedNewsArticle


def populate_article_from_json(data, manager):
    """
    Populate a single article from JSON data into the ontology
    """
    onto = manager.ontology

    def parse_timestamp(ts_str):
        try:
            # Try native ISO format
            return datetime.fromisoformat(ts_str)
        except ValueError:
            try:
                return datetime.strptime(ts_str, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValueError(f"Unrecognized timestamp format: {ts_str}")

    # Add core article
    article_obj = FormattedNewsArticle(
        headline=data["headline"],
        content=data["content"],
        timestamp=parse_timestamp(data["timestamp"]),
        url=data["url"],
        source=data["source"],
    )
    article_indiv = manager.add_article(article_obj)

    with onto:
        cat_class = getattr(onto, data["category"], None)
        print(f"[DEBUG] Category class for {data['category']}: {cat_class}")
        if cat_class is None:
            raise ValueError(
                f"[ERROR] Category '{data['category']}' not found in ontology."
            )

        subcat_class = getattr(onto, data["subcategory"], None)
        print(f"[DEBUG] Subcategory class for {data['subcategory']}: {subcat_class}")
        if subcat_class is None:
            raise ValueError(
                f"[ERROR] Subcategory '{data['subcategory']}' not found in ontology."
            )

        def get_or_create(cls, name):
            safe_name = manager._safe_name(name)
            print(f"[DEBUG] Safe name for {name}: {safe_name}")
            existing = onto.search_one(iri="*" + safe_name)
            if existing:
                return existing
            ind = cls(safe_name)
            ind.canonicalName = name
            return ind

        def get_or_create_category(cls, name):
            safe_name = f"{name}"
            print(f"[DEBUG] Safe name for category {name}: {safe_name}")
            existing = onto.search_one(iri="*" + safe_name)
            if existing:
                return existing
            return cls(safe_name)

        cat_indiv = get_or_create_category(cat_class, data["category"])
        subcat_indiv = get_or_create_category(subcat_class, data["subcategory"])
        article_indiv.hasCategory.append(cat_indiv)
        article_indiv.hasCategory.append(subcat_indiv)

        person_inds = [get_or_create(onto.Person, n) for n in data.get("persons", [])]
        location_inds = [
            get_or_create(onto.Location, n) for n in data.get("locations", [])
        ]
        event_inds = [get_or_create(onto.Event, n) for n in data.get("events", [])]
        org_inds = [
            get_or_create(onto.Organization, n) for n in data.get("organizations", [])
        ]

        # Generic link
        for entity in person_inds + location_inds + event_inds + org_inds:
            article_indiv.mentionsEntity.append(entity)

        # Category/Subcategory specific mappings
        if data["category"] == "PoliticsAndGovernance":
            if data["subcategory"] == "InternationalPolitics":
                for org in org_inds:
                    article_indiv.hasForeignOrganization.append(org)
                for ev in event_inds:
                    article_indiv.hasForeignEvent.append(ev)
                for p in person_inds:
                    article_indiv.hasForeignPerson.append(p)
                for loc in location_inds:
                    article_indiv.hasForeignLocation.append(loc)
            elif data["subcategory"] == "DomesticPolitics":
                for org in org_inds:
                    article_indiv.hasDomesticOrganization.append(org)
                for ev in event_inds:
                    article_indiv.hasDomesticEvent.append(ev)
                for p in person_inds:
                    article_indiv.hasDomesticPerson.append(p)
                for loc in location_inds:
                    article_indiv.hasDomesticLocation.append(loc)
        elif data["category"] == "ScienceAndTechnology":
            if data["subcategory"] == "TechAndInnovation":
                for org in org_inds:
                    article_indiv.hasTechCompany.append(org)
                for ev in event_inds:
                    article_indiv.hasTechEvent.append(ev)
                for p in person_inds:
                    article_indiv.hasTechPerson.append(p)
                for loc in location_inds:
                    article_indiv.hasResearchLocation.append(loc)
            elif data["subcategory"] == "ResearchAndSpace":
                for org in org_inds:
                    article_indiv.hasResearchInstitution.append(org)
                for p in person_inds:
                    article_indiv.hasResearchPerson.append(p)
                for ev in event_inds:
                    article_indiv.hasResearchEvent.append(ev)
                for loc in location_inds:
                    article_indiv.hasResearchLocation.append(loc)
        elif data["category"] == "CultureAndEntertainment":
            if data["subcategory"] == "ScreenAndStage":
                for p in person_inds:
                    article_indiv.hasFilmDirectorActor.append(p)
                for org in org_inds:
                    article_indiv.hasFilmProductionCompany.append(org)
                for ev in event_inds:
                    article_indiv.hasResearchEvent.append(ev)
                for loc in location_inds:
                    article_indiv.hasResearchLocation.append(loc)
            elif data["subcategory"] == "MusicAndArts":
                for p in person_inds:
                    article_indiv.hasMusicArtist.append(p)
                for org in org_inds:
                    article_indiv.hasMusicCompany.append(org)
                for ev in event_inds:
                    article_indiv.hasMusicEvent.append(ev)
                for loc in location_inds:
                    article_indiv.hasMusicLocation.append(loc)
        elif data["category"] == "Sports":
            if data["subcategory"] == "Cricket":
                for org in org_inds:
                    article_indiv.hasCricketTeam.append(org)
                for p in person_inds:
                    article_indiv.hasCricketPlayer.append(p)
                for loc in location_inds:
                    article_indiv.hasCricketVenue.append(loc)
                for ev in event_inds:
                    article_indiv.hasCricketTournament.append(ev)
            elif data["subcategory"] == "Football":
                for org in org_inds:
                    article_indiv.hasFootballTeam.append(org)
                for p in person_inds:
                    article_indiv.hasFootballPlayer.append(p)
                for loc in location_inds:
                    article_indiv.hasFootballVenue.append(loc)
                for ev in event_inds:
                    article_indiv.hasFootballTournament.append(ev)
            elif data["subcategory"] == "Other":
                for org in org_inds:
                    article_indiv.hasTeam.append(org)
                for p in person_inds:
                    article_indiv.hasPlayer.append(p)
                for loc in location_inds:
                    article_indiv.hasVenue.append(loc)
                for ev in event_inds:
                    article_indiv.hasTournament.append(ev)
        elif data["category"] == "CrimeAndJustice":
            for p in person_inds:
                article_indiv.hasWitness.append(p)
            for org in org_inds:
                article_indiv.hasInvestigation.append(org)
            if data["subcategory"] == "CrimeReport":
                for ev in event_inds:
                    article_indiv.hasCrimeType.append(ev)
                for loc in location_inds:
                    article_indiv.hasCrimeLocation.append(loc)
            elif data["subcategory"] == "CourtsAndInvestigation":
                for ev in event_inds:
                    article_indiv.hasCourtCase.append(ev)
                for loc in location_inds:
                    article_indiv.hasCourtLocation.append(loc)
        else:
            print(
                f"[DEBUG] Unhandled category/subcategory: {data['category']}/{data['subcategory']}"
            )

    return article_indiv


def populate_bulk_articles(data_list, manager):
    """
    Populate multiple articles from a list of JSON data
    Returns statistics about the operation
    """
    successful = 0
    failed = 0
    errors = []

    for i, data in enumerate(data_list):
        try:
            populate_article_from_json(data, manager)
            successful += 1
            print(f"[INFO] Successfully processed article {i + 1}/{len(data_list)}")
        except Exception as e:
            failed += 1
            error_msg = f"Article {i + 1}: {str(e)}"
            errors.append(error_msg)
            print(f"[ERROR] {error_msg}")

    # Save the ontology after all articles are processed
    try:
        manager.save()
        print("[INFO] Ontology saved successfully")
    except Exception as e:
        error_msg = f"Failed to save ontology: {str(e)}"
        errors.append(error_msg)
        print(f"[ERROR] {error_msg}")

    return {
        "total_processed": len(data_list),
        "successful": successful,
        "failed": failed,
        "errors": errors,
    }
