import datetime as dt
import unittest

import prayer_tools as pt


def minutes(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


class PrayerToolsTest(unittest.TestCase):
    def test_london_sunrise_sunset(self):
        times, _ = pt.PrayerCalculator(51.5072, -0.1276, 1, "MWL").compute(dt.date(2026, 10, 20))
        # Published sunrise about 07:32 and sunset about 17:57 BST
        self.assertLessEqual(abs(minutes(pt.fmt(times["sunrise"])) - minutes("07:32")), 3)
        self.assertLessEqual(abs(minutes(pt.fmt(times["maghrib"])) - minutes("17:57")), 3)

    def test_hanafi_asr_is_later(self):
        d = dt.date(2027, 4, 10)
        std, _ = pt.PrayerCalculator(41.0, 29.0, 3, "Diyanet", "standard").compute(d)
        han, _ = pt.PrayerCalculator(41.0, 29.0, 3, "Diyanet", "hanafi").compute(d)
        self.assertGreater(han["asr"], std["asr"])

    def test_makkah_isha_is_90_minutes_after_maghrib(self):
        t, _ = pt.PrayerCalculator(21.4225, 39.8262, 3, "Makkah").compute(dt.date(2025, 3, 1))
        self.assertAlmostEqual((t["isha"] - t["maghrib"]) * 60, 90, delta=0.5)

    def test_high_latitude_produces_times(self):
        t, notes = pt.PrayerCalculator(64.1466, -21.9426, 0, "MWL").compute(dt.date(2026, 6, 21))
        self.assertNotEqual(pt.fmt(t["fajr"]), "--:--")
        self.assertNotEqual(pt.fmt(t["isha"]), "--:--")
        self.assertTrue(notes)

    def test_qibla_bearings(self):
        self.assertAlmostEqual(pt.qibla(51.5072, -0.1276)[0], 119.0, delta=0.5)   # London
        self.assertAlmostEqual(pt.qibla(40.7128, -74.006)[0], 58.5, delta=0.5)    # New York
        self.assertAlmostEqual(pt.qibla(3.139, 101.6869)[0], 292.5, delta=1.0)   # Kuala Lumpur

    def test_hijri_known_ramadan_starts(self):
        # Within 1 day of announced starts
        for greg in [dt.date(2024, 3, 11), dt.date(2025, 3, 1), dt.date(2026, 2, 18)]:
            found = False
            for off in (-1, 0, 1):
                y, m, d = pt.gregorian_to_hijri(greg + dt.timedelta(days=off))
                if m == 9 and d == 1:
                    found = True
            self.assertTrue(found, greg)

    def test_round_trip(self):
        d = dt.date(2027, 2, 8)
        self.assertEqual(pt.hijri_to_gregorian(*pt.gregorian_to_hijri(d)), d)


if __name__ == "__main__":
    unittest.main()
