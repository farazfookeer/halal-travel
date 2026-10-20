# Halal Travel skill

A Claude skill for planning halal holidays from first idea to day-by-day itinerary.

It checks every hotel, restaurant, flight and activity against the traveller's own standards across four criteria: food and alcohol, prayer logistics, privacy and modesty, and Ramadan and Eid. Each option gets a Halal Fit Score with evidence labels (Verified, Claimed, Unknown), so nothing is called halal without a source.

## What it does

1. **Intake**: who is travelling, dates, budget, and how strict each criterion should be
2. **Calendar check**: flags Ramadan, Eid, Arafah and Hajj season overlaps
3. **Destination shortlist**: live checks on the Global Muslim Travel Index, travel advice and entry rules
4. **Research and scoring**: properties scored for halal fit, with nearby mosques and halal food
5. **Shortlist with booking links**: the traveller books and pays
6. **Optional browser booking**: only with explicit consent, always stopping before payment
7. **Itinerary**: shareable doc, day-by-day map and Word or PDF, built around prayer times and Jummah

## Offline prayer tools

`skills/halal-travel/scripts/prayer_tools.py` needs no network or packages:

```bash
python3 prayer_tools.py times --lat 41.0082 --lon 28.9784 --tz 3 --start 2027-04-10 --days 7 --country TR
python3 prayer_tools.py qibla --lat 51.5072 --lon -0.1276
python3 prayer_tools.py ramadan --year 2027
python3 prayer_tools.py methods
```

Prayer times follow the standard astronomical method with 19 regional calculation conventions, Standard or Hanafi Asr, and high-latitude adjustments. Hijri dates use the arithmetic calendar and can differ from moon-sighting announcements by 1 to 2 days. All outputs are planning estimates; confirm with the local mosque.

Run the tests with `python3 -m unittest discover skills/halal-travel/scripts`.

## Install

- **Claude Code**: add this repo as a plugin, or copy `skills/halal-travel` into `~/.claude/skills/`.
- **Claude app**: upload the `skills/halal-travel` folder as a custom skill, or save it from a skill proposal card.

## Principles

- The traveller sets the standard; the skill never assumes the strictest or loosest reading.
- No fatwas: where schools differ, positions are presented neutrally.
- Current facts (prices, visas, rankings, Eid dates) are looked up and date-stamped.
- The traveller always makes the payment.

Built by Silsila Labs.

## Licence

MIT
