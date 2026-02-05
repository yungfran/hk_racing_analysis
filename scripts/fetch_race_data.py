import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

DATA_OUT = os.path.join("data", "output")
os.makedirs(DATA_OUT, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_sectional_table(race_date, race_no):
    url = (
        "https://racing.hkjc.com/zh-hk/local/information/"
        f"displaysectionaltime?racedate={race_date}&RaceNo={race_no}"
    )

    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")

    if table is None:
        return None

    rows = []
    for tr in table.find_all("tr")[1:]:
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) < 6:
            continue

        rows.append({
            "race_no": race_no,
            "horse_no": tds[1],
            "horse_name": tds[2],
            "sectional_times": tds[3:-1],
            "finish_time": tds[-1]
        })

    return pd.DataFrame(rows)


def fetch_all_races(race_date):
    all_df = []

    for race_no in range(1, 10):
        df = fetch_sectional_table(race_date, race_no)
        if df is not None and not df.empty:
            all_df.append(df)

    if not all_df:
        return None

    return pd.concat(all_df, ignore_index=True)


if __name__ == "__main__":
    # ⚠️ 之後可改成自動日期
    RACE_DATE = "04/02/2026"

    df = fetch_all_races(RACE_DATE)

    if df is None:
        print("❌ 未能抓取任何賽事資料")
    else:
        out_path = os.path.join(DATA_OUT, "raw_sectional.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"✅ 已儲存官方分段資料：{out_path}")
