from craigslist import CraigslistForSale
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from slackclient import SlackClient
from util import post_listing_to_slack
import time
import settings

engine = create_engine('sqlite:///craigslist.db', echo=False)

Base = declarative_base()


class Listing(Base):
    """
    A table to store data on craigslist listings
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    updated = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def scrape_area(area):

    cl = CraigslistForSale(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_SECTION,
                        filters={'max_price': settings.MAX_PRICE, 'min_price': settings.MIN_PRICE,
                        'query': 'concept 2', 'search_titles': 'T'})

    results = []
    gen = cl.get_results(sort_by='newest', geotagged=True, limit=20)

    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:

            lat = 0
            lng = 0
            if result["geotag"] is not None:
                lat = result["geotag"][0]
                lng = result["geotag"][1]

            price = 0

            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lng=lng,
                name=result["name"],
                price=price,
                location=result["where"],
                cl_id=result["id"]
                )


            session.add(listing)
            session.commit()

            results.append(result)

    return results


def do_scrape():
    all_results = []
    for area in settings.AREAS:
        print("Searching {}".format(area))
        all_results += scrape_area(area)

    print ("{}: Got {} results".format(time.ctime(), len(all_results)))

    sc = SlackClient(settings.SLACK_TOKEN)
    for result in all_results:
        post_listing_to_slack(sc, result)