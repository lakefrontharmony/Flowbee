import pytest


@pytest.fixture()
def input_json_pipeline_file():
	return open('../Files/UnitTestFiles/pipeline_example.json')   # pragma: no cover


@pytest.fixture()
def input_release_csv_file():
	return open('../Files/UnitTestFiles/fix_versions_unit_test.csv')   # pragma: no cover
