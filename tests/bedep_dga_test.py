import datetime
from pathlib import Path

import pytest

from src.bedep_dga import calculate_bedep_domains, BedepDGA, BedepError
from src.common import next_wednesday, next_thursday


class TestClass:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, monkeypatch):
        self.current_fake_time = None

        class patched_datetime(datetime.datetime):
            pass

        def fake_datetime_now():
            return self.current_fake_time

        def fake_datetime_today():
            return self.current_fake_time

        class FakeResponse:
            text = "TEST_DATA"

            def __init__(self, *args):
                pass

            def raise_for_status(self):
                pass

        monkeypatch.setattr(patched_datetime, "now", fake_datetime_now)
        monkeypatch.setattr(patched_datetime, "today", fake_datetime_today)
        datetime.datetime = patched_datetime

        monkeypatch.setattr("requests.get", FakeResponse)


class Test_domain_calculation():
    def test_first_test(self):
        from_date = datetime.datetime(2020, 1, 1)
        till_date = datetime.datetime(2020, 1, 1)
        config = [{"value1": 0x9be6851a,
                   "value2": 0xd666e1f3,
                   "value3": 0x2666ca48,
                   "table": "table1.json",
                   "max_currencies": 48,
                   }]
        results = calculate_bedep_domains(from_date, till_date, config)
        first_result = next(results)
        assert first_result == ('bedep_dga_0x9be6851a_0xd666e1f3_0x2666ca48_table1_48',
                                datetime.datetime(2019, 12, 26, 0, 0),
                                datetime.datetime(2020, 1, 1, 23, 59, 59),
                                'bclcbaadsueo89.com')


class Test_determine_next_days(TestClass):
    def test_next_wednesday_today_is_tuesday(self):
        today_is_tuesday = datetime.datetime(2020, 1, 7)
        self.current_fake_time = today_is_tuesday

        assert next_wednesday(today_is_tuesday) == datetime.datetime(2020, 1, 8, 0, 0, 0, 0)

    def test_next_wednesday_today_is_wednesday(self):
        today_is_wednesday = datetime.datetime(2020, 1, 8)
        self.current_fake_time = today_is_wednesday

        assert next_wednesday(today_is_wednesday) == datetime.datetime(2020, 1, 8, 0, 0, 0, 0)

    def test_next_wednesday_today_is_thursday(self):
        today_is_thursday = datetime.datetime(2020, 1, 9)
        self.current_fake_time = today_is_thursday

        assert next_wednesday(today_is_thursday) == datetime.datetime(2020, 1, 15, 0, 0, 0, 0)

    def test_next_thursday_today_is_wednesday(self):
        today_is_wednesday = datetime.datetime(2020, 1, 8)
        self.current_fake_time = today_is_wednesday

        assert next_thursday(today_is_wednesday) == datetime.datetime(2020, 1, 9, 0, 0, 0, 0)

    def test_next_thursday_today_is_thursday(self):
        today_is_thursday = datetime.datetime(2020, 1, 9)
        self.current_fake_time = today_is_thursday

        assert next_thursday(today_is_thursday) == datetime.datetime(2020, 1, 9, 0, 0, 0, 0)

    def test_next_thursday_today_is_friday(self):
        today_is_friday = datetime.datetime(2020, 1, 10)
        self.current_fake_time = today_is_friday

        assert next_thursday(today_is_friday) == datetime.datetime(2020, 1, 16, 0, 0, 0, 0)


class Test_Bedep_dga(TestClass):
    # domains for the upcoming week can be generated earliest on wednesday
    config = {"value1": 0x9be6851a,
              "value2": 0xd666e1f3,
              "value3": 0x2666ca48,
              "table": "table1.json",
              "max_currencies": 48,
              }

    def test_execption_if_requested_date_is_after_next_wednesday_and_not_requedst_on_wednesday(self):
        today_is_tuesday = datetime.datetime(2020, 1, 7)
        self.current_fake_time = today_is_tuesday

        next_thursday = datetime.datetime(2020, 1, 9)
        with pytest.raises(BedepError):
            BedepDGA(self.config, next_thursday)

    def test_execption_request_on_wednesday_for_next_thursday(self):
        today_is_wednesday = datetime.datetime(2020, 1, 8)
        self.current_fake_time = today_is_wednesday

        next_thursday = datetime.datetime(2020, 1, 9)
        assert BedepDGA(self.config, next_thursday)

    def test_calculate_domains_for_current_week(self):
        today_is_wednesday = datetime.datetime(2020, 1, 8)
        self.current_fake_time = today_is_wednesday

        dga = BedepDGA(self.config, today_is_wednesday)
        dga.cache_path = Path(__file__).parent / "test_cache"

        number_of_domains_calculated = len(list(dga.run()))
        assert number_of_domains_calculated == 22

        assert next(dga.run()) == ('bedep_dga_0x9be6851a_0xd666e1f3_0x2666ca48_table1_48',
                                   datetime.datetime(2020, 1, 2, 0, 0),
                                   datetime.datetime(2020, 1, 8, 23, 59, 59),
                                   'beqmoixbtlchmbtb.com')

    def test_calculate_domains_for_upcoming_week(self):
        today_is_thursday = datetime.datetime(2020, 1, 9)
        self.current_fake_time = today_is_thursday

        dga = BedepDGA(self.config, today_is_thursday)
        dga.cache_path = Path(__file__).parent / "test_cache"

        number_of_domains_calculated = len(list(dga.run()))
        assert number_of_domains_calculated == 28

        assert next(dga.run()) == ('bedep_dga_0x9be6851a_0xd666e1f3_0x2666ca48_table1_48',
                                   datetime.datetime(2020, 1, 9, 0, 0),
                                   datetime.datetime(2020, 1, 15, 23, 59, 59),
                                   'ajqyqjqrbijgyg.com')
