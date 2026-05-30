from datetime import datetime

import requests
from waste_collection_schedule import Collection, Icons
from waste_collection_schedule.exceptions import SourceArgumentNotFound

TITLE = "City of Oklahoma City"
DESCRIPTION = "Source for okc.schizo.dev (public feed) for City of Oklahoma City"
URL = "https://okc.schizo.dev"
COUNTRY = "us"
TEST_CASES = {
    "Test_001": {"objectID": "1781151"},
    "Test_002": {"objectID": "2002902"},
    "Test_003": {"objectID": 1935340},
}

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en,en-GB;q=0.7,en-US;q=0.3",
}
UNOFFICIAL_URL = "https://okc.schizo.dev/trash"

# Maps the feed's section keys to a waste type label and icon.
SECTIONS = {
    "trash": ("Trash", Icons.GENERAL_WASTE),
    "recycling": ("Recycle", Icons.RECYCLING),
    "bulkyWaste": ("Bulky", Icons.BULKY),
}

ICON_MAP = {
    "Trash": Icons.GENERAL_WASTE,
    "Recycle": Icons.RECYCLING,
    "Bulky": Icons.BULKY,
}

PARAM_DESCRIPTIONS = {  # Optional dict to describe the arguments, will be shown in the GUI configuration below the respective input field
    "en": {
        "objectID": "Object ID for the public feed (okc.schizo.dev).",
    },
}

PARAM_TRANSLATIONS = {
    "en": {
        "objectID": "Object ID",
    },
}

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": "Using a browser, go to https://data.okc.gov/portal/page/viewer?datasetName=Address%20Trash%20Services. "
    "Click on the `Map` tab, search for your address, then click on your house. "
    "Click on the `Table` tab, then click on the `Filter By Map` menu item and click `Apply` to reduce the list. "
    "The more you zoom in on your house, the better this filter works. "
    "Find your address in the filtered list and make a note of the `Object ID` number in the first column. "
    "This is the number you need to use as `objectID`."
}


class Source:
    def __init__(self, objectID: str = ""):
        self._object_id = str(objectID).strip()
        if not self._object_id:
            raise SourceArgumentNotFound("objectID", objectID)

    def fetch(self) -> list[Collection]:
        response = requests.get(
            UNOFFICIAL_URL,
            params={"recordID": self._object_id},
            headers=HEADERS,
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise SourceArgumentNotFound("objectID", self._object_id)

        entries: list[Collection] = []
        for key, (waste_type, icon) in SECTIONS.items():
            section = data.get(key)
            if not isinstance(section, dict):
                continue

            pickups = section.get("pickups")
            if not isinstance(pickups, list):
                continue

            for pickup in pickups:
                if not isinstance(pickup, dict):
                    continue
                raw_date = pickup.get("date")
                if not raw_date:
                    continue
                try:
                    pickup_date = datetime.strptime(str(raw_date), "%Y-%m-%d").date()
                except ValueError:
                    continue
                entries.append(Collection(date=pickup_date, t=waste_type, icon=icon))

        if not entries:
            raise SourceArgumentNotFound("objectID", self._object_id)

        return entries
