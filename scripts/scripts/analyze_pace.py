import pandas as pd
import ast
import os

DATA_RAW = os.path.join("data", "output", "raw_sectional.csv")
DATA_OUT = os.path.join("data", "output", "race_analysis_full.csv")

# ⚠️ 示意：官方班次標準步速（秒）
# 真實可日後接 HKJC / RacingKing 標準表
STANDARD_PACE = {
    "1000": [12.0, 11.8, 11.9, 12.2, 12.5],
    "1200": [12.2, 11.9, 11.8, 12.0, 12.3, 12.8],
    "1400": [12.4, 12.0, 11.9, 11.9, 12.1, 12.4, 12.9],
    "1600": [12.6, 12.2, 12.0, 11.9, 12.0, 12.2, 12.6, 13.0]
}

def parse_times(sectional):
    out = []
    for t in sectional:
        try:
            out.append(float(t))
        except:
            out.append(None)
    return out


def analyze():
    df = pd.read_csv(DATA_RAW)

    results = []

    for _, row in df.iterrows():
        secs = parse_times(ast.literal_eval(row["sectional_times"]))
        distance = str(len(secs) * 200)

        if distance not in STANDARD_PACE:
            continue

        standard = STANDARD_PACE[distance]
        diffs = []

        for s, std in zip(secs, standard):
            if s is None:
                diffs.append(None)
            else:
                diffs.append(round(s - std, 2))

        results.append({
            "race_no": row["race_no"],
            "horse_no": row["horse_no"],
            "horse_name": row["horse_name"],
            "distance": distance,
            "sectional_diff": diffs,
            "avg_diff": round(sum(d for d in diffs if d is not None) / len(diffs), 2)
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv(DATA_OUT, index=False, encoding="utf-8-sig")
    print(f"✅ 已輸出完整步速分析：{DATA_OUT}")


if __name__ == "__main__":
    analyze()
