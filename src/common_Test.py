import datetime

import pytest

from src.common import get_dgarchive_dga_name, cache_file_from_url, url_to_file_name


class Test_create_dgarchive_name:
    test_config = {"value1": 0x1,
                   "value2": 0x2,
                   "value3": 0x3,
                   "table": "table0.suffix",
                   "max_currencies": 100,
                   }

    def test_name_structure(self):
        assert get_dgarchive_dga_name(self.test_config) == "bedep_dga_0x1_0x2_0x3_table0_100"


class Test_cache_file:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, monkeypatch):
        self.fake_times = [datetime.datetime(2020, 1, 1),
                           datetime.datetime(2020, 1, 2)]

        class FakeTime:
            @classmethod
            def now(cls):
                return self.fake_times.pop(0)

        class FakeResponse:
            text = "TEST_DATA"

            def __init__(self, *args):
                pass

            def raise_for_status(self):
                pass

        monkeypatch.setattr(datetime, 'datetime', FakeTime)
        monkeypatch.setattr("requests.get", FakeResponse)

    def test_cache_file(self, tmp_path):
        file = cache_file_from_url("URL", tmp_path)

        assert f"{tmp_path}/VVJM_2020-01-01" == str(file)
        assert file.read_text() == "TEST_DATA"

    def test_read_cached_file_if_already_exist(self, tmp_path):
        existing_cache_file = tmp_path / "VVJM_2020-01-01"
        existing_cache_file.write_text("NEW_TEST_DATA")

        file = cache_file_from_url("URL", tmp_path)

        assert file == existing_cache_file
        assert file.read_text() == "NEW_TEST_DATA"

    def test_cache_file_each_day(self, tmp_path):
        fileA = cache_file_from_url("URL", tmp_path)
        fileB = cache_file_from_url("URL", tmp_path)

        assert str(fileA) == f"{tmp_path}/VVJM_2020-01-01"
        assert str(fileB) == f"{tmp_path}/VVJM_2020-01-02"

    def test_convert_url_to_filename(self):
        assert url_to_file_name("URL") == f"VVJM_2020-01-01"

    def test_change_date_in_filename_each_day(self):
        assert url_to_file_name("URL") == f"VVJM_2020-01-01"
        # new day
        assert url_to_file_name("URL") == f"VVJM_2020-01-02"
