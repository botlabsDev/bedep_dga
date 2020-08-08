from src.common import get_dgarchive_dga_name, cache_file


def test_create_dgarchive_name():
    test_config = {"value1": 0x1,
                   "value2": 0x2,
                   "value3": 0x3,
                   "table": "table0.suffix",
                   "max_currencies": 100,
                   }

    assert get_dgarchive_dga_name(test_config) == "bedep_dga_0x1_0x2_0x3_table0_100"


def test_cache_file(tmp_path, mocker):
    class FakeResponse:
        text = "TEST_DATA"

    mocker.patch('requests.get', return_value=FakeResponse())

    file = cache_file("URL", tmp_path)

    assert file.exists()
    assert tmp_path / file.name == file
    assert file.read_text() == "TEST_DATA"
