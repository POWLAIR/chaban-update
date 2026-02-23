import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import uuid
from pathlib import Path

API_URL = (
    "https://opendata.bordeaux-metropole.fr/api/explore/v2.1"
    "/catalog/datasets/previsions_pont_chaban/records"
)

TZ = pytz.timezone("Europe/Paris")


def fetch_closures() -> list[dict]:
    params = {"limit": 100, "order_by": "date_passage ASC"}
    resp = requests.get(API_URL, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("results", [])


def parse_dt(date_str: str, time_str: str) -> datetime | None:
    """Assemble une date + heure en datetime Paris-aware."""
    if not time_str:
        return None
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        return TZ.localize(dt)
    except ValueError:
        return None


def build_event(closure: dict) -> Event | None:
    date_str    = closure.get("date_passage", "")
    bateau      = closure.get("bateau") or "Inconnu"
    type_fermt  = closure.get("type_de_fermeture") or ""
    heure_fermt = closure.get("fermeture_a_la_circulation") or ""
    heure_rouv  = closure.get("re_ouverture_a_la_circulation") or ""

    if not date_str:
        return None

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    start = parse_dt(date_str, heure_fermt) or TZ.localize(
        datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0)
    )
    end = parse_dt(date_str, heure_rouv) or (start + timedelta(hours=1))

    event = Event()
    event.add("summary", f"Pont Chaban ferme - {bateau}")
    event.add("dtstart", start)
    event.add("dtend", end)
    event.add(
        "description",
        f"Bateau : {bateau}\n"
        f"Type   : {type_fermt}\n"
        f"Fermeture   : {heure_fermt or 'N/A'}\n"
        f"Reouverture : {heure_rouv or 'N/A'}",
    )
    event.add("location", "Pont Chaban-Delmas, Bordeaux, France")
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"pont-chaban-{date_str}-{bateau}"))
    event.add("uid", uid)

    return event


def main() -> None:
    print("Recuperation des fermetures du Pont Chaban-Delmas...")
    closures = fetch_closures()
    print(f"{len(closures)} entrees trouvees.")

    cal = Calendar()
    cal.add("prodid", "-//Pont Chaban-Delmas//FR")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "Pont Chaban-Delmas - Fermetures")
    cal.add("x-wr-timezone", "Europe/Paris")
    cal.add("refresh-interval;value=duration", "P2D")
    cal.add("x-published-ttl", "P2D")

    count = 0
    for closure in closures:
        event = build_event(closure)
        if event:
            cal.add_component(event)
            count += 1

    out = Path("docs/pont_chaban.ics")
    out.parent.mkdir(exist_ok=True)
    out.write_bytes(cal.to_ical())
    print(f"{count} evenements ecrits dans {out}")


if __name__ == "__main__":
    main()
