from datetime import datetime
from meetup.api import Client, MeetupObject

MEETUP_CLIENT_KEY = 'alpha_num_key'

CLIENT = Client(MEETUP_CLIENT_KEY)

def from_epoch(epoch: int, tz_offset: int = 0) -> datetime:
    """
    Returns a datetime from an epoch int with optional UTC timezone offset
    """
    return datetime.fromtimestamp((epoch - tz_offset) / 1000)

def get_group(name: str) -> MeetupObject:
    """
    Returns a MeetupObject for a group by url name
    """
    return CLIENT.GetGroup({'urlname': name})

def extract_details(group: MeetupObject) -> dict:
    """
    Returns a dict of extracted meetup group info
    """
    return {
        'name': group.name,
        'category': group.category['name'],
        'created': from_epoch(group.created),
        'city': group.city,
        'state': group.state,
        'country': group.country,
        'description': group.description,
        'url': group.link,
        'organizer': group.organizer['name'],
        'members': group.members,
        'member_title': group.who
    }

def next_meetup(group: MeetupObject) -> (str, datetime, int):
    """
    Returns the title, UTC datetime, and attendee count from a group
    """
    event = group.next_event
    time = from_epoch(event['time'], event['utc_offset'])
    return event['name'], time, event['yes_rsvp_count']
