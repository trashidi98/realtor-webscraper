import pytest
from src.final_scraper import RealtorData, main
from unittest.mock import patch
from csv import reader
import os

TEST_FILENAME = "test_filename"


@pytest.fixture(autouse=True)
def cleanup_test_csv_file():
    yield
    os.remove(f"{TEST_FILENAME}.csv")


# Run a test with batching
# We already tested that batching works via unit tests
# Now just need to ensure we get expected results for batching
@patch("src.final_scraper.BATCH_SIZE", 2)
def test_scraper_e2e_with_batching():
    with patch("sys.argv", ["scraper_file.py", "3", TEST_FILENAME]):
        main()

    with open(f"{TEST_FILENAME}.csv", "r") as file:
        csv_reader = reader(file)

        expected_field_names = next(csv_reader)

        assert expected_field_names == list(RealtorData._fields)

        # There is no real way to deterministically check if
        # The data is a name or role etc
        # The browser just populates divs with info
        # As long as we've scraped the right divs, which unit tests check
        # Then this kind of check is enough
        for row in csv_reader:
            assert len(row) == 5
            assert all(isinstance(item, str) for item in row)


def test_scraper_e2e_no_batching():
    with patch("sys.argv", ["scraper_file.py", "2", TEST_FILENAME]):
        main()

    with open(f"{TEST_FILENAME}.csv", "r") as file:
        csv_reader = reader(file)

        expected_field_names = next(csv_reader)

        assert expected_field_names == list(RealtorData._fields)

        for row in csv_reader:
            assert len(row) == 5
            assert all(isinstance(item, str) for item in row)
