# Prayer and worship while travelling

## Prayer times: use the script

`scripts/prayer_tools.py` computes prayer times offline. It needs no network.

```bash
# A week of times in Istanbul, Turkish default method
python3 scripts/prayer_tools.py times --lat 41.0082 --lon 28.9784 --tz 3 --start 2027-04-10 --days 7 --country TR

# Hanafi Asr (later Asr time), JSON for building the itinerary
python3 scripts/prayer_tools.py times --lat 3.139 --lon 101.6869 --tz 8 --start 2027-04-10 --days 7 --country MY --asr hanafi --json
```

Rules for using it:
- `--tz` must be the UTC offset **at the destination on the travel dates**, including daylight saving. Look it up if unsure; Europe and North America change clocks in late March and late October.
- Pick the method with `--country` (local default) unless the traveller follows a specific method. Run `methods` to list them.
- Use `--asr hanafi` for travellers who follow the Hanafi school, which many South Asian and Turkish Muslims do. Ask during intake.
- Above roughly 48 degrees latitude in summer, Fajr and Isha may need high-latitude rules. The script applies the angle-based rule and adds a note. Tell the traveller and point them to the local mosque timetable.
- Always label times as planning estimates and recommend confirming with the local mosque, which may also publish separate jamaah (congregation) times.

## Qibla

```bash
python3 scripts/prayer_tools.py qibla --lat 36.51 --lon -4.88
```
Gives the bearing from true north. Phone compasses use magnetic north, which can differ by several degrees in some regions; a qibla app or the hotel's marker is better in the room.

## Jummah

- For every Friday in the trip, find a mosque near where the traveller will be at midday, not just near the hotel. Day trips often clash.
- Khutbah times vary widely: in many countries Jummah follows Dhuhr time, but in the UK, Europe and North America mosques often hold fixed or multiple sessions. Check the mosque's own page or social media.
- Plan no tours, check-outs or transfers from about 30 minutes before to 90 minutes after the expected khutbah.
- Women's prayer space: note whether the mosque has a women's section if women in the party want to attend.

## Travel concessions (present neutrally, never rule)

Schools of thought differ on shortening (qasr) and combining (jam') prayers while travelling. Summarise the traveller's own school if they state it, and suggest confirming with their scholar. Do not issue rulings.

Commonly cited positions, for orientation only:
- **Shortening**: four-unit prayers (Dhuhr, Asr, Isha) shortened to two. The qualifying distance is commonly cited as roughly 80 to 90 km.
- **Hanafi**: shortening is required while travelling; combining is generally not permitted except at Arafah and Muzdalifah during Hajj. Traveller status ends with an intention to stay 15 days or more.
- **Shafi'i, Maliki, Hanbali**: shortening is permitted; combining Dhuhr with Asr and Maghrib with Isha is permitted while travelling. Traveller status commonly ends with an intention to stay more than 4 days (counted differently between schools).

In the itinerary, if the traveller says they combine, show the combined windows; otherwise show all five times.

## On planes and in transit

- Long-haul: add the prayer times at origin, any layover airport and destination, and flag which prayers fall in the air.
- Many airlines on Gulf and South-East Asian routes show qibla on the seat map or have a prayer area; check the airline's site.
- Airport prayer rooms: search "[airport name] prayer room" or "multi-faith room" and note the terminal. Most major hubs have one.
- Wudu: suggest a small travel bottle; note where airports provide wudu facilities.

## Finding mosques and halal food on the ground

- Search maps for "mosque" or "masjid" near each day's main stop. Check opening times; some smaller masjids open only for prayer times.
- For halal food, search maps for "halal restaurant" and then check certification or the restaurant's own statement. Zabihah-style directories and HalalTrip-style apps are useful leads; treat their listings as Claimed until checked.
