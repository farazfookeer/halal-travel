# Ramadan, Eid and the Islamic calendar

## Always check the dates first

Before suggesting dates or destinations, run:

```bash
python3 scripts/prayer_tools.py ramadan --year 2027
python3 scripts/prayer_tools.py hijri --date 2027-02-14
```

The script uses the arithmetic (tabular) calendar, so dates are estimates that can be 1 to 2 days off actual moon-sighting announcements. For anything time-critical (Eid prayer, booking around Eid), search for the official announcement for that country closer to the date and say which you used.

Flag any overlap with:
- **Ramadan** (whole month)
- **Last ten nights** (Laylat al-Qadr window), when many travellers want to be near a mosque or in Makkah or Madinah
- **Eid al-Fitr and Eid al-Adha** (public holidays in Muslim-majority countries: closures, crowds, higher prices, family travel peaks)
- **Hajj season** (around Dhu al-Hijjah): Umrah visas and Makkah hotel availability are restricted or very expensive; Gulf hubs are busy.

## If the trip falls in Ramadan

Ask whether the traveller wants Ramadan to be the point of the trip (spiritual focus) or wants to avoid disruption. Then:

**Planning**
- Compute daily Fajr (start of fast) and Maghrib (iftar) times for each location and put them on every itinerary day.
- Fasting length matters: high latitudes in summer mean very long fasts. Show the hours.
- Move tiring activities (hiking, long walks, beach days in heat) to early morning or after iftar.
- Hot destinations: avoid midday outdoor plans entirely.
- Build in rest after Dhuhr.

**Food**
- Suhoor: does the property serve it, deliver it, or provide a kitchenette? Many resorts in Muslim-majority countries run suhoor buffets; in Europe this is rare unless the property targets Muslim guests.
- Iftar: book iftar tents or restaurants in advance in popular cities. In Muslim-majority countries, restaurants may be closed during the day; in Muslim-minority countries, iftar options may be limited, so map them.

**Worship**
- Taraweeh: find a mosque with Taraweeh near the base and note the start time (often 60 to 90 minutes after Maghrib).
- Last ten nights: Qiyam/Tahajjud programmes, i'tikaf if the traveller wants it.

**Travel days**
- Travellers may choose not to fast on travel days; that is their decision. Show the timings either way.

## If the trip covers Eid

- Find the Eid prayer location and time (usually soon after sunrise; often in large open spaces in Muslim-majority countries, or in mosques and parks elsewhere).
- Expect closures of offices and some attractions for 2 to 4 days in Muslim-majority countries; restaurants and malls are usually busy and open.
- Eid al-Adha: if the traveller wants to arrange qurbani while away, note local options or suggest arranging it through a charity at home.
- Prices and crowds: domestic tourism peaks. Book early.

## Other dates worth knowing

- Day of Arafah (9 Dhu al-Hijjah): many fast; suggest a light day.
- Ashura (10 Muharram): some fast; in some countries public observances affect traffic.
- Islamic New Year: public holiday in many Muslim-majority countries.
