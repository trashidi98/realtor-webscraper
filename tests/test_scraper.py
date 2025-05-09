from unittest.mock import Mock, PropertyMock, patch, mock_open
import pytest
from src.final_scraper import (
    collect_realtor_data_from_page,
    initialize_csv,
    main,
    render_page,
    sanitize,
    check_input_pages,
    DEFAULT_PAGES_TO_SCRAPE,
    check_input_filename,
    DEFAULT_FILENAME,
    RealtorData,
    provision_webdriver,
    scrape_pages,
    write_to_csv,
)
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException


@patch("src.final_scraper.Chrome")
@patch("src.final_scraper.ChromeOptions")
@patch("src.final_scraper.ChromeService")
def test_provision_webdriver(mock_service, mock_options, mock_chrome):
    # mock Service(), means mocking the Service/Options object
    # Then set the objects return value (mocks instantiation of Service/Options object)

    mock_service_instance = mock_service.return_value
    mock_options_instance = mock_options.return_value
    mock_options_add_argument_call = mock_options_instance.add_argument

    provision_webdriver()

    assert mock_service.called
    assert mock_options.called
    assert mock_options_add_argument_call.called

    assert mock_chrome.call_args[1]["service"] == mock_service_instance
    assert mock_chrome.call_args[1]["options"] == mock_options_instance


@patch("src.final_scraper.LOGGER.critical")
@patch("src.final_scraper.Chrome")
@patch("src.final_scraper.ChromeOptions")
@patch("src.final_scraper.ChromeService")
def test_provision_webdriver_throws_exception_and_exits(
    mock_service, mock_options, mock_chrome, logger
):
    mock_chrome.side_effect = WebDriverException("mock exception msg")

    with pytest.raises(SystemExit):
        provision_webdriver()

    assert (
        logger.call_args_list[0][0][0]
        == "Something went wrong with Webdriver setup: Message: mock exception msg\n"
    )


def test_sanitize():
    text_data = "  \n\n  REALTOR TEXT DATA   \n"
    good_data = "GOOD REALTOR DATA"

    assert sanitize(text_data) == "REALTOR TEXT DATA"
    assert sanitize(good_data) == "GOOD REALTOR DATA"


# TODO Write tests that deal with exception path of below 2 tests
@patch("src.final_scraper.writer")
def test_initialize_csv(csv_writer):
    csv_writer_obj = csv_writer.return_value

    with patch("builtins.open", mock_open()) as open_mock:
        filename = "myfile"
        created_csv_filename = initialize_csv(filename)

        assert open_mock.called
        assert open_mock.call_args_list[0][0] == ("myfile.csv", "w")
        assert csv_writer_obj.writerow.call_args_list[0][0][0] == [
            "name",
            "role",
            "company",
            "address",
            "number",
        ]
        assert created_csv_filename == "myfile.csv"


@patch("src.final_scraper.writer")
def test_write_to_csv(csv_writer):
    csv_writer_obj = csv_writer.return_value

    with patch("builtins.open", mock_open()) as open_mock:
        filename = "myfile.csv"
        pages_data = [["page_data1"], ["page_data2"]]
        write_to_csv(filename, pages_data)

        assert open_mock.called
        assert open_mock.call_args_list[0][0] == ("myfile.csv", "a")
        assert csv_writer_obj.writerows.call_count == 2
        assert csv_writer_obj.writerows.call_args_list[0][0][0] == ["page_data1"]
        assert csv_writer_obj.writerows.call_args_list[1][0][0] == ["page_data2"]


def test_check_input_pages():
    bad_input = "BAD"
    bad_input_2 = "-1"
    good_input = "6"

    assert check_input_pages(bad_input) == DEFAULT_PAGES_TO_SCRAPE
    assert check_input_pages(bad_input_2) == DEFAULT_PAGES_TO_SCRAPE
    assert check_input_pages(good_input) == 6


def test_check_input_filename():
    bad_input = "{this is a ba&dda{}[]sd filename"
    good_input = "good_file_name_1"

    assert check_input_filename(bad_input) == DEFAULT_FILENAME
    assert check_input_filename(good_input) == "good_file_name_1"


REALTOR_DATA_FULL = """
<div class="realtorCardCon card" data-binding="id=RealtorCard-{IndividualId}"
    id="RealtorCard-2030322">
    <div class="realtorCardBody">
        <div class="realtorCardTop">
            <div class="realtorCardInnerTop">
                <div class="realtorCardTopCenter">
                    <a class="realtorCardDetailsLink realtorDetailsLink"
                        data-binding="href=DetailsURL"
                        href="example.com">
                        <div class>
                            <span data-binding="visible=ShowRealtorName">
                                <span class="realtorCardName"
                                    data-binding="innertext=RealtorName">JOKER JOKINGTON</span>
                                <span class="realtorCardEducation"
                                    data-binding="innertext=RealtorEducationalCredentials"></span>
                            </span>
                        </div>
                        <div class="realtorCardTitle"
                            data-binding="innertext=RealtorPosition">
                            HEAD GOOFER \n
                        </div>
                        <div class="realtorCardAddress"
                            data-binding="visible=ShowRealtorAddress,innertext=Address">
                        </div>
                        <div class="realtorCardOfficeInfo"
                            data-binding="visible=ShowOfficeInfo">
                            <img alt="GOOFY IMAGE"
                                class="realtorCardOfficeLogo"
                                data-binding="src=OfficeLogoImageURL,visible=ShowOfficeLogo,alt=OfficeAltText"
                                src="Nope" />
                            <div class="realtorCardOfficeName"
                                data-binding="innertext=OfficeName">
                                GOOFY OFFICE \n
                            </div>
                            <div class="realtorCardOfficeDesignation"
                                data-binding="innertext=OfficeDesignationName">
                                Brokerage
                            </div>
                            <div class="realtorCardOfficeAddress"
                                data-binding="innertext=OfficeAddress">
                                GOOFEY GOOBER ST, OMAHA, NEBRASKA
                            </div>
                        </div>
                    </a>
                </div>
                <div class="realtorCardTopRight">
                </div>
            </div>
        </div>
        <div class="realtorCardBottom">
            <div class="realtorCardInnerBottom">
                <div class="realtorCardBottomLeft">
                    <div class="realtorCardPhone" data-type="Telephone"><span
                            class="realtorCardContactIcon"><i
                                class="fa fa-phone"></i></span><span
                            class="realtorCardContactNumber TelephoneNumber">000-000-9898</span></div>
                </div>
                <div class="realtorCardBottomRight">
                    <div class="realtorCardSocialIcons"
                        data-binding="SocialIcons,visible=ShowSocialIcons">
                    </div>
                    <a class="lnkEmailRealtor blueRoundedBtn btn"
                        data-binding="visible=ShowEmailButton" href="#"><span
                            class="fa fa-envelope"></span><span
                            class="realtorCardFooterLinkText">Email</span></a>
                </div>
            </div>
        </div>
    </div>
</div>
"""


def test_collect_realtor_data_from_page():
    soup = BeautifulSoup(REALTOR_DATA_FULL, "html.parser")
    data = collect_realtor_data_from_page(soup)

    assert len(data) == 1
    assert isinstance(data[0], RealtorData)
    assert data[0].name == "JOKER JOKINGTON"
    assert data[0].address == "GOOFEY GOOBER ST, OMAHA, NEBRASKA"
    assert data[0].company == "GOOFY OFFICE"
    assert data[0].number == "000-000-9898"
    assert data[0].role == "HEAD GOOFER"


VALID_RESULTS = RealtorData(
    name="JOKER JOKINGTON",
    role="HEAD GOOFER",
    company="GOOFY OFFICE",
    address="GOOFEY GOOBER ST, OMAHA, NEBRASKA",
    number="000-000-9898",
)


@patch("src.final_scraper.BeautifulSoup")
def test_collect_realtor_data_from_page_missing_name(bs_patch):
    for i, _ in enumerate(RealtorData._fields):
        realtor_data_key_errors = list(VALID_RESULTS).copy()
        expected_values = list(VALID_RESULTS).copy()

        # For each place in VALID_RESULTS, replace it with a TypeError
        # This simulates an error being thrown when bs4 method .find() happens

        # When an error is thrown for a particular field, we should default to ""
        # This is what expected_values array is checking for

        # We want to do this for each field in RealtorData
        realtor_data_key_errors[i] = TypeError
        expected_values[i] = ""

        mock_card = Mock(spec=BeautifulSoup)
        mock_card_obj = mock_card.return_value
        type(mock_card_obj.find.return_value).text = PropertyMock(
            side_effect=realtor_data_key_errors
        )

        mock_realtor_card_divs_obj = bs_patch.return_value
        mock_realtor_card_divs_obj.find_all.return_value = [mock_card_obj]

        data = collect_realtor_data_from_page(mock_realtor_card_divs_obj)

        assert len(data) == 1
        assert isinstance(data[0], RealtorData)
        assert data[0].name == expected_values[0]
        assert data[0].role == expected_values[1]
        assert data[0].company == expected_values[2]
        assert data[0].address == expected_values[3]
        assert data[0].number == expected_values[4]


@patch("src.final_scraper.time.sleep")
@patch("src.final_scraper.collect_realtor_data_from_page")
@patch("src.final_scraper.BeautifulSoup")
def test_render_page(mock_soup, mock_collect, mock_time_sleep):
    mock_time_sleep.return_value = None

    driver = Mock()
    driver.page_source = "mock html via beautifulsoup"

    render_page(driver, "mock_url")

    assert driver.get.call_args_list[0][0][0] == "mock_url"

    assert mock_soup.call_args_list[0][0][0] == "mock html via beautifulsoup"
    assert mock_soup.call_args_list[0][0][1] == "html.parser"

    assert mock_collect.call_args_list[0][0][0] == mock_soup.return_value


@patch("src.final_scraper.time.sleep")
@patch("src.final_scraper.LOGGER.error")
def test_render_page_throws_error_and_logs(logger, mock_time_sleep):
    mock_time_sleep.return_value = None

    driver = Mock()
    driver.get.side_effect = Exception("EXCEPTION INFO")

    with pytest.raises(Exception):
        render_page(driver, "mock_url")

    assert (
        logger.call_args_list[0][0][0]
        == "Could not load page, more info EXCEPTION INFO"
    )


@patch("src.final_scraper.write_to_csv")
@patch("src.final_scraper.render_page")
def test_scrape_pages(mock_render, mock_write_csv):
    BATCH_SIZE = 2
    fake_driver = Mock()
    fake_filename = "fake_file.csv"
    pages = 4
    expected_data = [
        # Each item represents a page
        ["fake1", "data1"],
        ["fake2", "data2"],
        ["fake3", "data3"],
        ["fake4", "data4"],
    ]

    mock_render.side_effect = expected_data

    scrape_pages(fake_driver, fake_filename, pages, BATCH_SIZE)

    assert mock_write_csv.call_args_list[0][0][0] == fake_filename
    assert mock_write_csv.call_args_list[0][0][1] == expected_data[0:2]

    assert mock_write_csv.call_args_list[1][0][0] == fake_filename
    assert mock_write_csv.call_args_list[1][0][1] == expected_data[2:]


@patch("src.final_scraper.scrape_pages")
@patch("src.final_scraper.initialize_csv")
@patch("src.final_scraper.provision_webdriver")
def test_main_one_arg(mock_prov_driver, mock_init_csv, mock_scrape_pages):
    with patch("sys.argv", ["scraper_file.py"]):
        main()

    assert mock_prov_driver.called

    assert mock_init_csv.called
    assert mock_init_csv.call_args_list[0][0][0] == DEFAULT_FILENAME

    assert mock_scrape_pages.called
    assert mock_scrape_pages.call_args_list[0][0][0] == mock_prov_driver.return_value
    assert mock_scrape_pages.call_args_list[0][0][1] == mock_init_csv.return_value
    assert mock_scrape_pages.call_args_list[0][0][2] == DEFAULT_PAGES_TO_SCRAPE


@patch("src.final_scraper.scrape_pages")
@patch("src.final_scraper.initialize_csv")
@patch("src.final_scraper.provision_webdriver")
def test_main_two_arg(mock_prov_driver, mock_init_csv, mock_scrape_pages):
    with patch("sys.argv", ["scraper_file.py", "3"]):
        main()

    assert mock_prov_driver.called

    assert mock_init_csv.called
    assert mock_init_csv.call_args_list[0][0][0] == DEFAULT_FILENAME

    assert mock_scrape_pages.called
    assert mock_scrape_pages.call_args_list[0][0][0] == mock_prov_driver.return_value
    assert mock_scrape_pages.call_args_list[0][0][1] == mock_init_csv.return_value
    assert mock_scrape_pages.call_args_list[0][0][2] == 3


@patch("src.final_scraper.scrape_pages")
@patch("src.final_scraper.initialize_csv")
@patch("src.final_scraper.provision_webdriver")
def test_main_three_arg(mock_prov_driver, mock_init_csv, mock_scrape_pages):
    with patch("sys.argv", ["scraper_file.py", "3", "test_filename"]):
        main()

    assert mock_prov_driver.called

    assert mock_init_csv.called
    assert mock_init_csv.call_args_list[0][0][0] == "test_filename"

    assert mock_scrape_pages.called
    assert mock_scrape_pages.call_args_list[0][0][0] == mock_prov_driver.return_value
    assert mock_scrape_pages.call_args_list[0][0][1] == mock_init_csv.return_value
    assert mock_scrape_pages.call_args_list[0][0][2] == 3


@patch("src.final_scraper.LOGGER.critical")
def test_main_too_many_args(logger):
    with pytest.raises(SystemExit):
        with patch(
            "sys.argv", ["scraper_file.py", "3", "test_filename", "too", "many", "args"]
        ):
            main()

    assert (
        logger.call_args_list[0][0][0]
        == "Looks like more than 3 arguments were supplied.\
            The first is number of pages to scrape, \
            second argument should be the name of the file you want to save to e.g myfile, data_file"
    )
