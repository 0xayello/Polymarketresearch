# fetch.py
import requests, pandas as pd, pyarrow.parquet as pq, datetime, pathlib

URL = "https://gamma-api.polymarket.com/markets"
params, mkts = dict(closed="true", limit=500, offset=0), []

while True:
    batch = requests.get(URL, params=params, timeout=30).json()
    if not batch: break
    mkts.extend(batch); params["offset"] += params["limit"]

df = pd.json_normalize(mkts)
path = pathlib.Path("data") / f"markets_{datetime.date.today()}.parquet"
path.parent.mkdir(exist_ok=True)
pq.write_table(df.to_arrow(), path)
print("Dump salvo em", path)
