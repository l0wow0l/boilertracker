#!/usr/bin/env python3
"""Download today's Purdue dining court menus (with nutrition) into menu.json.

Usage:  python3 purdue_menu.py            # today's menu
        python3 purdue_menu.py 2026-10-14 # a specific date
Then open Boiler Tray and load menu.json from "직접 추가 · 메뉴 불러오기".

Uses only the Python standard library. Data comes from Purdue's public menu
service (api.hfs.purdue.edu), the same one behind dining.purdue.edu/menus.
Be polite: run it once or twice a day, not in a tight loop.
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date

BASE = "https://api.hfs.purdue.edu/menus/v2"
DAY = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()


def get(path):
    req = urllib.request.Request(f"{BASE}/{path}", headers={"User-Agent": "boiler-tray/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def nutrient(item, name):
    for n in item.get("Nutrition", []):
        if n.get("Name") == name:
            return n.get("Value") or 0
    return 0


def serving(item):
    for n in item.get("Nutrition", []):
        if n.get("Name") == "Serving Size":
            return n.get("LabelValue") or ""
    return ""


def main():
    courts = [l["Name"] for l in get("locations")["Location"] if l.get("Type") == "Dining Courts"]
    entries = {}  # (item id, court, meal) -> metadata
    for court in courts:
        try:
            menu = get(f"locations/{court}/{DAY}")
        except Exception as exc:  # a court may be closed that day
            print(f"skip {court}: {exc}")
            continue
        for meal in menu.get("Meals", []):
            for station in meal.get("Stations", []):
                for item in station.get("Items", []):
                    if item.get("NutritionReady"):
                        entries[(item["ID"], court, meal["Name"])] = item["Name"]

    ids = sorted({k[0] for k in entries})
    print(f"{len(courts)} courts, {len(ids)} unique items with nutrition")
    with ThreadPoolExecutor(max_workers=8) as pool:
        details = dict(zip(ids, pool.map(lambda i: get(f"items/{i}"), ids)))

    items = []
    for (item_id, court, meal), name in sorted(entries.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[1])):
        d = details[item_id]
        items.append({
            "id": f"{item_id}|{court}|{meal}",
            "name": name,
            "loc": court,
            "meal": meal,
            "serving": serving(d),
            "cal": round(nutrient(d, "Calories")),
            "p": round(nutrient(d, "Protein"), 1),
            "c": round(nutrient(d, "Total Carbohydrate"), 1),
            "f": round(nutrient(d, "Total fat"), 1),
        })

    with open("menu.json", "w", encoding="utf-8") as fh:
        json.dump({"date": DAY, "items": items}, fh, ensure_ascii=False)
    print(f"wrote menu.json ({len(items)} entries)")


if __name__ == "__main__":
    main()
