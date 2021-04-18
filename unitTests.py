import unittest
from textFunc import rivers_func
from weatherScrapper import weatherInfo


class TestTextAnalysis(unittest.TestCase):

    def test_nature(self):
        self.assertEqual(['Nature'], rivers_func("nature"))
        self.assertEqual(['Nature'], rivers_func("water trees ocean beach air forest walk park dirt earth plants"))

    def test_vision(self):
        self.assertEqual(['Visual Hallucinations'], rivers_func("hallucin"))
        self.assertEqual(['Visual Hallucinations'], rivers_func("geometry seeing colors aura shine shimmer"))

    def test_audio(self):
        self.assertEqual(['Audio Hallucinations'], rivers_func("music"))
        self.assertEqual(['Audio Hallucinations'], rivers_func("hear imagine voices sounds loud quiet whisper"))

    def test_ego(self):
        self.assertEqual(['Ego Death'], rivers_func("anxiety"))
        self.assertEqual(['Ego Death'], rivers_func("identity self consciousness insignificant personal trance"))

    def test_time(self):
        self.assertEqual(['Time Perception'], rivers_func("time"))
        self.assertEqual(['Time Perception'], rivers_func("quick short clock percept race speed"))

    def test_combinations(self):
        self.assertEqual(['Time Perception', 'Nature'], rivers_func("time clock tree"))
        self.assertEqual(['Visual Hallucinations', 'Audio Hallucinations', 'Ego Death'],
                         rivers_func("geometry seeing colors hear imagine identity"))

    def test_blank(self):
        self.assertEqual([], rivers_func(""))


class WeatherTests(unittest.TestCase):

    def test_format(self):
        self.assertTrue("Sunset is at" in weatherInfo())
        self.assertFalse("Sunset is at" == weatherInfo())
        self.assertTrue("Sunrise is at" in weatherInfo())
        self.assertFalse("Sunrise is at" == weatherInfo())
        self.assertTrue("Weather today is" in weatherInfo())
        self.assertFalse("Weather today is" == weatherInfo())


if __name__ == '__main__':
    unittest.main()
