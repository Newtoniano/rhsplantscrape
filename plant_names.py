#%%
import math
import time

import pandas as pd
import requests

#%%
url = "https://plants.rhs.org.uk/api/Plant/AdvanceSearch"
payload = {"startFrom": 0, "pageSize": 5, "includeAggregation": False}
headers = {
    "authority": "plants.rhs.org.uk",
    "accept": "application/json, text/plain, */*",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "",
    "content-type": "application/json",
    "origin": "https://www.rhs.org.uk",
    "referer": "https://www.rhs.org.uk/",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
}
#%%
response = requests.request("POST", url, json=payload, headers=headers)
data = response.json()
#%%
# Calculate how many loops we need to do to extract all the data
max_pageSize = 100  # determined empirically by trying until it gives an error
loop_count = math.ceil(
    data["totalHit"] / max_pageSize
)  # rounded up to make sure we get all entries
#%%
plant_names_data = []
# plant_ids = []  deprecated, see below

for loop in range(loop_count):
    payload = {
        "startFrom": 0 + (loop * max_pageSize),
        "pageSize": max_pageSize,
        "includeAggregation": False,
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()
    # Store all the plant names data we get from the api
    plant_names_data.extend(data["hits"])
    # Get plant id and add it to a list only if plant isn't a synonym of another entry
    # DEPRECATED, doing it with pandas instead, see below
    # for entry in data["hits"]:
    #    if entry["isSynonym"] == False:
    #        plant_ids.append(entry["id"])
    time.sleep(1)  # throttling api requests to avoid issues
#%%
# Convert list to a pandas dataframe for easier manipulation
# df_ids = pd.Series(plant_ids) deprecated, see below
df_plants = pd.DataFrame(plant_names_data)
# Retreive plant ids of plants that aren't just a syntonim duplicate of another plant
df_unique_plants = df_plants.loc[df_plants["isSynonym"] == False]
unique_plants_ids = df_unique_plants["id"]

#%%
# Export plant dataframes to csv for later use
df_plants.to_csv("./csv/raw_plant_names_data.csv")
unique_plants_ids.to_csv("./csv/unique_plants_ids.csv", index=False, header=False)
