#%%
import time

import pandas as pd
import requests

#%%
# Load plant ids and put them into a list for later use
plant_ids = pd.read_csv(
    "./csv/unique_plants_ids.csv", squeeze=True, header=None
).tolist()
#%%
# Iterate over plant ids to pull details for each plant id, and then store them for later use
plants_details = []

for id in plant_ids:
    url = f"https://plants.rhs.org.uk/api/plant/details/{id}"

    headers = {
        "authority": "plants.rhs.org.uk",
        "accept": "application/json, text/plain, */*",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "",
        "content-length": "0",
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

    response = requests.request("POST", url, headers=headers)
    data = response.json()
    plants_details.append(data)
    time.sleep(1)  # Throttle api requests to avoid potential issues

# %%
plants_df = pd.json_normalize(plants_details)
plants_df.to_csv("./csv/plants_data.csv")

# %%
