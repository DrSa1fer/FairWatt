import requests

class TwoGis(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_info_at_address(self, address):
        url = f"https://catalog.api.2gis.com/3.0/items?key={self.api_key}&q={address}&locale=ru_RU"
        response = requests.get(url)

        json = response.json()
        status_code = json["meta"]["code"]
        if status_code == 200:
            return json["result"]["items"]
        else:
            return {"error": "Fail to companies",
                    "content": json["meta"]["error"]["message"]}

    def get_companies_at_address(self, address):
        url = f"https://catalog.api.2gis.com/3.0/items?key={self.api_key}&q={address}&locale=ru_RU"
        response = requests.get(url)

        json = response.json()
        status_code = json["meta"]["code"]
        if status_code != 200:
            return {"error": "Fail to companies",
                    "content": json["meta"]["error"]["message"]}

        items = json["result"]["items"]

        result = []

        for item in items:
            if item['type'] is 'branch':
                result.append({
                    "name": item["name"],
                    "purpose": item["purpose_name"]
                })

        return result