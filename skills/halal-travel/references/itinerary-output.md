# Itinerary outputs

The traveller can have three outputs. Default to all three when they asked for "everything"; otherwise produce the one they asked for.

1. **Shareable doc** (default): the main itinerary, editable and shareable with the family.
2. **Map**: one map per trip with day-by-day stops.
3. **Word or PDF file**: for printing or emailing.

Build the content once (as structured data), then render it three ways so the three never disagree.

## Data to assemble first

For each day:
- Date, weekday, Hijri date (from the script), location, UTC offset
- Prayer times for that location (from the script); Jummah mosque and khutbah time on Fridays
- Fasting window and iftar time if in Ramadan
- Plan: morning, afternoon, evening blocks, each with place name, address, travel time, booking reference if any
- Halal food: breakfast, lunch, dinner suggestions with evidence labels
- Nearest mosque to each main stop
- Notes: dress code (for example, mosque visits), closures, heat, Eid events

Trip-level:
- Party, dates, bases, flights, accommodation with confirmation numbers and cancellation deadlines
- Halal Fit summary per property
- Emergency info: local emergency number, embassy or consulate, nearest hospital to each base
- Packing list additions: prayer mat, compass or qibla app, wudu bottle, modest swimwear, adaptor
- Sources and "last checked" date

## Doc structure

Title: "[Destination] [Month Year]: Family Itinerary" (adjust to party).

1. **Overview**: dates, who, bases, one-paragraph summary of the trip
2. **At a glance**: table of days (date, location, headline plan, Jummah or Eid flag)
3. **Bookings**: flights, stays, transfers, with references and deadlines
4. **Halal and prayer essentials**: method used for prayer times and why, qibla bearing per base, mosques for Jummah, halal food approach, Ramadan or Eid notes
5. **Day by day**: one section per day, each starting with a prayer-times line, e.g.
   `Fajr 05:41 | Dhuhr 12:45 | Asr 15:24 | Maghrib 17:57 | Isha 19:42`
   then the plan blocks, food and notes. Schedule activities so no plan block overlaps a prayer time without a stated plan for where to pray.
6. **Emergency and practical**: contacts, health, money, SIM or eSIM
7. **Packing list**
8. **Sources** with last-checked dates

Write in plain British English. No em-dashes (use commas, colons or full stops). Short sentences, easy to scan on a phone.

## Map

Use the places tools when available: search places for each stop, then display an itinerary map with one "day" per itinerary day, the stops in order, arrival times and a short note (include "pray Dhuhr at X" style notes where useful). Include mosques and halal restaurants as stops when they are part of the plan. Without places tools, build an HTML page with a map library and markers.

## Word or PDF

Use the docx or pdf skill (read its SKILL.md first). Same section order as the doc. Put the day-by-day prayer times in a small table at the top of each day. A4, readable at 11pt, page breaks between days for longer trips.

## Final checks before delivery

- Every Friday has a Jummah plan; every Eid has an Eid prayer plan.
- No activity overlaps a prayer time without a place to pray noted.
- Ramadan days show Fajr and Maghrib prominently.
- Every halal claim has an evidence label.
- Prices and times carry a "checked on" date.
- UTC offsets reflect daylight saving on the actual dates.
- No em-dashes in the text.
