import unittest
from utils.weather_requester import call_weather

class MyTestCase(unittest.TestCase):
    def test_something(self):
        s=call_weather("Moscow")
        print(s.json())
        self.assertEqual(s.status_code, 200)  # add assertion here


if __name__ == '__main__':
    unittest.main()
