#!/usr/bin/env python3
"""Offline prayer times, qibla bearing and Hijri date estimates for trip planning.

No network needed. Based on the standard astronomical method used by PrayTimes.org.
Times are ESTIMATES for planning. Always tell the traveller to confirm with the
local mosque or a trusted local timetable, especially Fajr and Isha at high latitudes.

Usage examples:
  python3 prayer_tools.py times --lat 41.0082 --lon 28.9784 --tz 3 --date 2027-04-10 --method Diyanet
  python3 prayer_tools.py times --lat 51.5072 --lon -0.1276 --tz 1 --start 2026-10-20 --days 7 --asr hanafi
  python3 prayer_tools.py qibla --lat 36.5101 --lon -4.8825
  python3 prayer_tools.py hijri --date 2027-02-08
  python3 prayer_tools.py ramadan --year 2027
  python3 prayer_tools.py methods

Add --json to any command for machine-readable output.
"""
import argparse
import datetime as dt
import json
import math
import sys

# ---------------------------------------------------------------- methods
# fajr / isha in degrees below horizon, or isha as minutes after maghrib ("90min").
METHODS = {
    "MWL":       {"name": "Muslim World League", "fajr": 18, "isha": 17},
    "ISNA":      {"name": "Islamic Society of North America", "fajr": 15, "isha": 15},
    "Egypt":     {"name": "Egyptian General Authority of Survey", "fajr": 19.5, "isha": 17.5},
    "Makkah":    {"name": "Umm al-Qura, Makkah", "fajr": 18.5, "isha": "90min"},
    "Karachi":   {"name": "University of Islamic Sciences, Karachi", "fajr": 18, "isha": 18},
    "Tehran":    {"name": "Institute of Geophysics, Tehran", "fajr": 17.7, "isha": 14, "maghrib": 4.5},
    "Diyanet":   {"name": "Diyanet, Turkey (approximation)", "fajr": 18, "isha": 17},
    "JAKIM":     {"name": "JAKIM, Malaysia", "fajr": 20, "isha": 18},
    "Singapore": {"name": "MUIS, Singapore", "fajr": 20, "isha": 18},
    "Kemenag":   {"name": "Kemenag, Indonesia", "fajr": 20, "isha": 18},
    "Gulf":      {"name": "Gulf region", "fajr": 19.5, "isha": "90min"},
    "Kuwait":    {"name": "Kuwait", "fajr": 18, "isha": 17.5},
    "Qatar":     {"name": "Qatar", "fajr": 18, "isha": "90min"},
    "France":    {"name": "UOIF, France", "fajr": 12, "isha": 12},
    "Russia":    {"name": "Spiritual Administration of Muslims of Russia", "fajr": 16, "isha": 15},
    "Morocco":   {"name": "Morocco", "fajr": 19, "isha": 17},
    "Tunisia":   {"name": "Tunisia", "fajr": 18, "isha": 18},
    "Algeria":   {"name": "Algeria", "fajr": 18, "isha": 17},
    "Jordan":    {"name": "Jordan", "fajr": 18, "isha": 18},
}

# Sensible default method by country code, used when the caller passes --country.
COUNTRY_DEFAULT = {
    "GB": "MWL", "IE": "MWL", "DE": "MWL", "NL": "MWL", "BE": "MWL", "ES": "MWL", "PT": "MWL",
    "IT": "MWL", "BA": "MWL", "AL": "MWL", "GR": "MWL", "AT": "MWL", "CH": "MWL",
    "TR": "Diyanet", "SA": "Makkah", "AE": "Gulf", "OM": "Gulf", "BH": "Gulf", "QA": "Qatar",
    "KW": "Kuwait", "EG": "Egypt", "MA": "Morocco", "TN": "Tunisia", "DZ": "Algeria",
    "JO": "Jordan", "MY": "JAKIM", "SG": "Singapore", "ID": "Kemenag", "BN": "JAKIM",
    "PK": "Karachi", "IN": "Karachi", "BD": "Karachi", "LK": "Karachi", "MV": "Karachi",
    "US": "ISNA", "CA": "ISNA", "FR": "France", "RU": "Russia", "IR": "Tehran",
    "AZ": "MWL", "UZ": "MWL", "KZ": "MWL", "JP": "MWL", "KR": "MWL", "TH": "MWL",
    "ZA": "MWL", "TZ": "MWL", "KE": "MWL", "MU": "MWL", "AU": "MWL", "NZ": "MWL",
}

KAABA_LAT = 21.422487
KAABA_LON = 39.826206

# ---------------------------------------------------------------- maths helpers
def dsin(d): return math.sin(math.radians(d))
def dcos(d): return math.cos(math.radians(d))
def dtan(d): return math.tan(math.radians(d))
def darcsin(x): return math.degrees(math.asin(max(-1.0, min(1.0, x))))
def darccos(x): return math.degrees(math.acos(max(-1.0, min(1.0, x))))
def darctan2(y, x): return math.degrees(math.atan2(y, x))
def darccot(x): return math.degrees(math.atan(1.0 / x))
def fix(a, b):
    a = a - b * math.floor(a / b)
    return a + b if a < 0 else a


def julian(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5


def sun_position(jd):
    d = jd - 2451545.0
    g = fix(357.529 + 0.98560028 * d, 360)
    q = fix(280.459 + 0.98564736 * d, 360)
    L = fix(q + 1.915 * dsin(g) + 0.020 * dsin(2 * g), 360)
    e = 23.439 - 0.00000036 * d
    RA = darctan2(dcos(e) * dsin(L), dcos(L)) / 15.0
    eqt = q / 15.0 - fix(RA, 24)
    decl = darcsin(dsin(e) * dsin(L))
    return decl, eqt


class PrayerCalculator:
    def __init__(self, lat, lon, tz, method="MWL", asr="standard", high_lat="angle", elevation=0.0):
        if method not in METHODS:
            raise ValueError(f"Unknown method {method}. Try: {', '.join(METHODS)}")
        self.lat, self.lon, self.tz = lat, lon, tz
        self.m = METHODS[method]
        self.method = method
        self.asr_factor = 2 if asr.lower() == "hanafi" else 1
        self.high_lat = high_lat
        self.elev = elevation

    def _mid_day(self, jd, t):
        _, eqt = sun_position(jd + t)
        return fix(12 - eqt, 24)

    def _sun_angle_time(self, jd, angle, t, ccw=False):
        decl, _ = sun_position(jd + t)
        noon = self._mid_day(jd, t)
        cos_val = (-dsin(angle) - dsin(decl) * dsin(self.lat)) / (dcos(decl) * dcos(self.lat))
        if cos_val > 1 or cos_val < -1:
            return float("nan")  # sun never reaches this angle today
        h = darccos(cos_val) / 15.0
        return noon + (-h if ccw else h)

    def _asr_time(self, jd, t):
        decl, _ = sun_position(jd + t)
        angle = -darccot(self.asr_factor + dtan(abs(self.lat - decl)))
        return self._sun_angle_time(jd, angle, t)

    def compute(self, date):
        jd = julian(date.year, date.month, date.day) - self.lon / (15 * 24.0)
        riseset = 0.833 + 0.0347 * math.sqrt(max(self.elev, 0))
        # first pass with default guesses (day portions)
        guess = {"fajr": 5, "sunrise": 6, "dhuhr": 12, "asr": 13, "sunset": 18, "maghrib": 18, "isha": 18}
        t = {k: v / 24.0 for k, v in guess.items()}
        times = {
            "fajr": self._sun_angle_time(jd, self.m["fajr"], t["fajr"], ccw=True),
            "sunrise": self._sun_angle_time(jd, riseset, t["sunrise"], ccw=True),
            "dhuhr": self._mid_day(jd, t["dhuhr"]),
            "asr": self._asr_time(jd, t["asr"]),
            "sunset": self._sun_angle_time(jd, riseset, t["sunset"]),
        }
        mag = self.m.get("maghrib")
        times["maghrib"] = self._sun_angle_time(jd, mag, t["maghrib"]) if isinstance(mag, (int, float)) else times["sunset"]
        isha = self.m["isha"]
        times["isha"] = float("nan") if isinstance(isha, str) else self._sun_angle_time(jd, isha, t["isha"])

        # adjust to timezone
        for k in times:
            times[k] = times[k] + self.tz - self.lon / 15.0
        if isinstance(isha, str):
            times["isha"] = times["maghrib"] + int(isha.replace("min", "")) / 60.0
        notes = self._high_lat_adjust(times)
        return times, notes

    def _high_lat_adjust(self, times):
        notes = []
        night = fix(times["sunrise"] - times["sunset"], 24) if not (math.isnan(times["sunrise"]) or math.isnan(times["sunset"])) else float("nan")
        if math.isnan(night):
            notes.append("Sun does not rise or set on this date here; use a local timetable.")
            return notes

        def portion(angle):
            if self.high_lat == "night_middle":
                return night / 2
            if self.high_lat == "one_seventh":
                return night / 7
            return night * angle / 60.0  # angle-based (default)

        fa = self.m["fajr"]
        p = portion(fa)
        if math.isnan(times["fajr"]) or fix(times["sunrise"] - times["fajr"], 24) > p:
            times["fajr"] = times["sunrise"] - p
            notes.append(f"Fajr adjusted with high-latitude rule ({self.high_lat}).")
        isha = self.m["isha"]
        if not isinstance(isha, str):
            p = portion(isha)
            if math.isnan(times["isha"]) or fix(times["isha"] - times["sunset"], 24) > p:
                times["isha"] = times["sunset"] + p
                notes.append(f"Isha adjusted with high-latitude rule ({self.high_lat}).")
        return notes


def fmt(h):
    if h is None or math.isnan(h):
        return "--:--"
    h = fix(h + 0.5 / 60.0, 24)  # round to nearest minute
    hh = int(h)
    mm = int((h - hh) * 60)
    return f"{hh:02d}:{mm:02d}"


# ---------------------------------------------------------------- qibla
def qibla(lat, lon):
    dlon = math.radians(KAABA_LON - lon)
    p1, p2 = math.radians(lat), math.radians(KAABA_LAT)
    y = math.sin(dlon)
    x = math.cos(p1) * math.tan(p2) - math.sin(p1) * math.cos(dlon)
    bearing = (math.degrees(math.atan2(y, x)) + 360) % 360
    # great-circle distance (km)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    dist = 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    points = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return bearing, points[int((bearing + 11.25) // 22.5) % 16], dist


# ---------------------------------------------------------------- hijri (tabular / arithmetic)
HIJRI_MONTHS = ["Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani", "Jumada al-Ula",
                "Jumada al-Akhirah", "Rajab", "Shaban", "Ramadan", "Shawwal",
                "Dhu al-Qadah", "Dhu al-Hijjah"]
HIJRI_EPOCH = 1948439.5  # Julian day of 1 Muharram 1 AH (civil)


def gregorian_to_jd(d):
    return julian(d.year, d.month, d.day)


def jd_to_gregorian(jd):
    jd = jd + 0.5
    z = math.floor(jd)
    a = z
    if z >= 2299161:
        alpha = math.floor((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - math.floor(alpha / 4)
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e)
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return dt.date(int(year), int(month), int(day))


def hijri_to_jd(y, m, d):
    return d + math.ceil(29.5 * (m - 1)) + (y - 1) * 354 + math.floor((3 + 11 * y) / 30) + HIJRI_EPOCH - 1


def gregorian_to_hijri(date):
    jd = math.floor(gregorian_to_jd(date)) + 0.5
    y = math.floor((30 * (jd - HIJRI_EPOCH) + 10646) / 10631)
    m = min(12, math.ceil((jd - (29 + hijri_to_jd(y, 1, 1))) / 29.5) + 1)
    d = int(jd - hijri_to_jd(y, m, 1) + 1)
    return int(y), int(m), d


def hijri_to_gregorian(y, m, d):
    return jd_to_gregorian(hijri_to_jd(y, m, d))


def islamic_dates_for_year(greg_year):
    """Key dates whose estimated start falls in the given Gregorian year (+/- 1-2 days)."""
    out = []
    h_start = gregorian_to_hijri(dt.date(greg_year, 1, 1))[0]
    for hy in (h_start, h_start + 1):
        events = [
            ("Islamic New Year (1 Muharram)", hy, 1, 1),
            ("Ashura (10 Muharram)", hy, 1, 10),
            ("Ramadan begins (1 Ramadan)", hy, 9, 1),
            ("Laylat al-Qadr window (21-29 Ramadan) starts", hy, 9, 21),
            ("Eid al-Fitr (1 Shawwal)", hy, 10, 1),
            ("Day of Arafah (9 Dhu al-Hijjah)", hy, 12, 9),
            ("Eid al-Adha (10 Dhu al-Hijjah)", hy, 12, 10),
        ]
        for name, y, m, d in events:
            g = hijri_to_gregorian(y, m, d)
            if g.year == greg_year:
                out.append({"event": name, "hijri": f"{d} {HIJRI_MONTHS[m-1]} {y} AH", "estimated_date": g.isoformat()})
    out.sort(key=lambda e: e["estimated_date"])
    return out


# ---------------------------------------------------------------- CLI
def parse_date(s):
    return dt.date.fromisoformat(s)


def cmd_times(a):
    method = a.method
    if not method:
        method = COUNTRY_DEFAULT.get((a.country or "").upper(), "MWL")
    calc = PrayerCalculator(a.lat, a.lon, a.tz, method, a.asr, a.high_lat, a.elevation)
    start = parse_date(a.date or a.start or dt.date.today().isoformat())
    rows = []
    for i in range(a.days):
        d = start + dt.timedelta(days=i)
        times, notes = calc.compute(d)
        row = {"date": d.isoformat(), "weekday": d.strftime("%a")}
        row.update({k: fmt(times[k]) for k in ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]})
        if d.weekday() == 4:
            row["note"] = "Friday: Jummah replaces Dhuhr; check local khutbah time"
        if notes:
            row["note"] = (row.get("note", "") + " " + " ".join(notes)).strip()
        rows.append(row)
    meta = {"method": f"{method} ({METHODS[method]['name']})", "asr": a.asr, "utc_offset": a.tz,
            "lat": a.lat, "lon": a.lon,
            "caveat": "Planning estimate. Confirm with the local mosque timetable."}
    if a.json:
        print(json.dumps({"meta": meta, "days": rows}, indent=2))
        return
    print(f"Method: {meta['method']} | Asr: {a.asr} | UTC{a.tz:+g}")
    print(f"{'Date':<11}{'Day':<5}{'Fajr':<7}{'Rise':<7}{'Dhuhr':<7}{'Asr':<7}{'Maghrib':<9}{'Isha':<7}")
    for r in rows:
        print(f"{r['date']:<11}{r['weekday']:<5}{r['fajr']:<7}{r['sunrise']:<7}{r['dhuhr']:<7}{r['asr']:<7}{r['maghrib']:<9}{r['isha']:<7}{r.get('note','')}")
    print(meta["caveat"])


def cmd_qibla(a):
    b, point, dist = qibla(a.lat, a.lon)
    res = {"bearing_deg_true_north": round(b, 1), "compass_point": point, "distance_to_makkah_km": round(dist)}
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Qibla: {b:.1f} deg from true north ({point}), {dist:,.0f} km to Makkah")


def cmd_hijri(a):
    d = parse_date(a.date)
    y, m, day = gregorian_to_hijri(d)
    res = {"gregorian": d.isoformat(), "hijri": f"{day} {HIJRI_MONTHS[m-1]} {y} AH",
           "caveat": "Arithmetic estimate; actual dates depend on moon sighting and can differ by 1-2 days."}
    print(json.dumps(res, indent=2) if a.json else f"{res['gregorian']} = {res['hijri']} (estimate, +/- 1-2 days)")


def cmd_ramadan(a):
    events = islamic_dates_for_year(a.year)
    if a.json:
        print(json.dumps({"year": a.year, "events": events,
                          "caveat": "Estimates +/- 1-2 days; confirm with local announcements."}, indent=2))
        return
    print(f"Key Islamic dates in {a.year} (estimates, +/- 1-2 days, depend on moon sighting):")
    for e in events:
        print(f"  {e['estimated_date']}  {e['event']:<46} {e['hijri']}")


def cmd_methods(a):
    if a.json:
        print(json.dumps({"methods": METHODS, "country_defaults": COUNTRY_DEFAULT}, indent=2))
        return
    for k, v in METHODS.items():
        print(f"{k:<10} {v['name']:<48} fajr {v['fajr']}  isha {v['isha']}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("times", help="Prayer times for a place and date range")
    t.add_argument("--lat", type=float, required=True)
    t.add_argument("--lon", type=float, required=True)
    t.add_argument("--tz", type=float, required=True, help="UTC offset in hours for the travel dates, including DST")
    t.add_argument("--date", help="Single date YYYY-MM-DD")
    t.add_argument("--start", help="Start date YYYY-MM-DD")
    t.add_argument("--days", type=int, default=1)
    t.add_argument("--method", choices=list(METHODS), help="Calculation method (default from --country, else MWL)")
    t.add_argument("--country", help="ISO country code to pick the local default method")
    t.add_argument("--asr", choices=["standard", "hanafi"], default="standard")
    t.add_argument("--high-lat", dest="high_lat", choices=["angle", "night_middle", "one_seventh"], default="angle")
    t.add_argument("--elevation", type=float, default=0.0)
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_times)

    q = sub.add_parser("qibla", help="Qibla bearing from a location")
    q.add_argument("--lat", type=float, required=True)
    q.add_argument("--lon", type=float, required=True)
    q.add_argument("--json", action="store_true")
    q.set_defaults(func=cmd_qibla)

    h = sub.add_parser("hijri", help="Estimate the Hijri date for a Gregorian date")
    h.add_argument("--date", required=True)
    h.add_argument("--json", action="store_true")
    h.set_defaults(func=cmd_hijri)

    r = sub.add_parser("ramadan", help="Estimated Ramadan, Eid and other key dates in a Gregorian year")
    r.add_argument("--year", type=int, required=True)
    r.add_argument("--json", action="store_true")
    r.set_defaults(func=cmd_ramadan)

    m = sub.add_parser("methods", help="List calculation methods and country defaults")
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=cmd_methods)

    a = p.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
