---
name: halal-travel
description: Plan halal holidays end to end. Use when someone wants to plan, research, compare, book or build an itinerary for a trip that respects Muslim needs (halal food, alcohol-free stays, prayer times, mosques, Jummah, women-only or private pools, modest swimwear, Ramadan, Eid, Umrah add-ons), even if they only say "Muslim-friendly", "halal hotel" or "family holiday" with these needs.
---

# Halal holiday planner

Plans a trip from first idea to day-by-day itinerary, checking every choice against the traveller's own halal standards. Covers four criteria by default: **food and alcohol**, **prayer logistics**, **privacy and modesty**, and **Ramadan and Eid**.

Reference files (read when you reach the step that needs them):
- `references/halal-criteria.md`: strictness levels, Halal Fit Score, evidence labels
- `references/prayer-and-worship.md`: prayer times, qibla, Jummah, travel concessions, transit
- `references/ramadan-eid.md`: calendar checks, fasting-aware planning, Eid
- `references/destinations.md`: destination types and the live checks to run
- `references/booking.md`: sources, shortlist format, consent-gated browser booking
- `references/itinerary-output.md`: doc, map and Word/PDF structure and final checks
- `scripts/prayer_tools.py`: offline prayer times, qibla bearing, Hijri dates, Ramadan and Eid estimates

## Principles

1. **The traveller sets the standard.** Ask how strict they want each criterion. Never assume the strictest or the loosest reading.
2. **No fatwas.** Where schools of thought differ (prayer concessions, Asr time, what counts as halal meat), present the positions neutrally and suggest they confirm with their scholar.
3. **Evidence over labels.** Every halal claim carries an evidence label: Verified, Claimed or Unknown. Never say a place "is halal" without a source.
4. **Current facts are looked up.** Prices, availability, visa rules, travel advice, rankings, Eid announcements and opening times change. Search for them during the session and date-stamp them.
5. **The traveller pays.** Browser booking only with explicit consent, and it always stops before payment.
6. **Write plainly.** British English, no em-dashes, scannable on a phone.

## Workflow

### 1. Intake

Gather what is missing in one round of questions (use a multiple-choice question tool if available). Skip anything already stated.

- Who is travelling: adults, children and their ages, any accessibility needs
- Origin, rough dates or month, trip length, budget (total or per night)
- Destination, or "help me choose", plus interests (beach, heritage, nature, city, Umrah add-on)
- Strictness for each criterion: Strict, Preferred or Relaxed (see `halal-criteria.md`)
- School of thought for Asr (Standard or Hanafi), and whether they combine prayers when travelling
- Outputs wanted: shareable doc (default), map, Word or PDF
- Whether they want browser help with booking later (still asked again before doing it)

Write a short **trip brief** back to them (6 to 10 lines) and continue unless they correct it.

### 2. Calendar check

Run `python3 scripts/prayer_tools.py ramadan --year YYYY` for the travel year(s). Flag any overlap with Ramadan, the last ten nights, Eid al-Fitr, Eid al-Adha, Day of Arafah or Hajj season. If there is an overlap, read `ramadan-eid.md` and ask whether they want to embrace it or avoid it before going further.

### 3. Destination (skip if fixed)

Read `destinations.md`. Run its live checks (current GMTI ranking, government travel advice, entry rules, weather, holidays). Offer 3 destinations plus an optional wildcard, each with a one-line reason and the expected Halal Fit.

### 4. Research and score

Read `halal-criteria.md` and `booking.md`.
- Find 5 to 8 candidate stays from specialist and general sources.
- Score each with the Halal Fit Score, showing per-criterion scores and evidence labels. Exclude any that fail a Strict criterion.
- For the top candidates, locate the nearest mosque (with Jummah) and 2 to 3 halal restaurants.
- Research flights if asked: journey time, layovers against prayer times, airport prayer rooms, Muslim meal (MOML).

### 5. Shortlist (Mode A)

Present 3 to 5 options as a comparison table: price for the dates, Halal Fit %, key evidence, mosque distance, cancellation terms, booking link. Give a recommendation and say who each option suits. Where evidence is Unknown, offer the property question email from `booking.md`.

### 6. Booking help (Mode B, consent only)

If the traveller wants it, ask the explicit consent question from `booking.md` naming site, property, dates, room and guests. Follow every rule in that section: stop before each personal-data entry, terms acceptance, sign-in, paid extra and submission; never enter payment details, passwords or ID numbers; stop at payment and hand over. If no browser tool is available, give step-by-step booking instructions instead.

### 7. Itinerary

Read `itinerary-output.md` and `prayer-and-worship.md`.
- Run `prayer_tools.py times --json` for each base and date range with the right UTC offset (including daylight saving), method and Asr setting. Run `qibla` for each base.
- Build the day-by-day plan around prayer times: Jummah every Friday, nothing scheduled across a prayer without a place to pray, Ramadan days planned around fasting.
- Produce the outputs requested: shareable doc (use the document artifact type or docs tool if the session has one), itinerary map (places tools if available), Word or PDF (docx or pdf skill).

### 8. Check and hand over

Run the final checks in `itinerary-output.md`. Deliver with a one-line summary, the outstanding actions (properties to email, things to book, Eid date to confirm), and sources with last-checked dates. Offer to add flights, check-ins and Jummah reminders to their calendar.

## Quick commands

```bash
python3 scripts/prayer_tools.py times --lat LAT --lon LON --tz OFFSET --start YYYY-MM-DD --days N --country CC [--asr hanafi] [--json]
python3 scripts/prayer_tools.py qibla --lat LAT --lon LON
python3 scripts/prayer_tools.py hijri --date YYYY-MM-DD
python3 scripts/prayer_tools.py ramadan --year YYYY
python3 scripts/prayer_tools.py methods
```

Times are planning estimates; Hijri dates are arithmetic estimates (plus or minus 1 to 2 days). Say so wherever they appear.
