import urllib.request
import re
from bs4 import BeautifulSoup

class Product():
    def __init__(self, data):
        self.data = data

    def to_value_list(self):
        return (
                self.data["id"],
                self.data["area"],
                self.data["price"],
                self.data["elevator"],
                self.data["utility_cost"],
                self.data["appliances"],
                self.data["furnished"],
                self.data["rooms"],
                self.data["rooms_half"],
                " > ".join(self.data["location"]),
                self.data["view_center"][0],
                self.data["view_center"][1],
                0, # predicted
                0, # decided
                0  # done
        )

    @staticmethod
    def parse(html, product_id):
        data = {
            "id": product_id,
            "area": -1.0,
            "price": -1,
            "elevator": False,
            "utility_cost": -1,
            "appliances": False,
            "furnished": False,
            "rooms": 0,
            "rooms_half": 0,
            "location": [],
            "view_center": []
        }
        doc = BeautifulSoup(html, 'html.parser')

        area = doc.select("div.parameter-area-size > span.parameter-value")[0].contents[0]
        data["area"] = float(re.sub(r"[^0-9]", "", area))
        price = doc.select("div.parameter-price > span.parameter-value")[0].contents[0]
        data["price"] = int(float(re.sub(r"[^0-9]", "", price)))
        rooms = doc.select("div.parameter-room > span.parameter-value")[0].contents[0]

        # ask for location
        req = urllib.request.Request(
            url="https://ingatlan.com/detailspage/map?id=%s&beforeAction=true" % (product_id),
            method="GET"
        )
        req.add_header("Referer", "https://ingatlan.com/%s" % (product_id))
        req.add_header("X-Requested-With", "XMLHttpRequest")
        with urllib.request.urlopen(req) as response:
            locdoc = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')
            data["location"] = list(map(lambda x: x.contents[0].strip(), locdoc.select("div a.map-link")))
            y1, x1, y2, x2 = locdoc.find(id="details-map")["data-bbox"].split(",")
            data["view_center"] = [(float(x1) + float(x2)) / 2, (float(y1) + float(y2)) / 2]

        half_rooms = re.search(r"(\d+) fél", rooms)
        if half_rooms == None:
            half_rooms = 0
        else:
            half_rooms = int(float(half_rooms.group(1)))

        rooms = re.sub("%d fél" % (half_rooms), "", rooms)

        rooms = re.search(r"\d+", rooms)
        if rooms == None:
            rooms = 0
        else:
            rooms = int(float(rooms.group(0)))

        data["rooms"] = rooms
        data["rooms_half"] = half_rooms

        parameters = doc.select("div.paramterers > table > tr")
        for param in parameters:
            key, value = param.contents[1].contents[0], param.contents[3].contents[0]
            if value == "nincs megadva":
                continue

            if key == "Lift":
                data["elevator"] = (value == "van")
                continue
            if key == "Rezsiköltség":
                data["utility_cost"] = int(float(re.sub(r"[^0-9]", "", value)))
                continue
            if key == "Gépesített":
                data["appliances"] = (value == "igen")
                continue
            if key == "Bútorozott":
                data["furnished"] = (value == "igen")

        return Product(data)

