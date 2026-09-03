from urllib.request import urlopen

import pytest

from lib.dicom_standard_url import dicom_standard_url


EDITIONS = (
    (2026, "c"),
    (2023, "e"),
    (2021, "b"),
    (2020, "e"),
    (2019, "e"),
)

PUBLISHED_EDITIONS = EDITIONS[1:]


@pytest.mark.parametrize(("year", "revision_letter"), EDITIONS)
def test_dicom_standard_url_generates_expected_url(year: int, revision_letter: str):
    expected_url = (
        "https://dicom.nema.org/medical/Dicom/"
        f"{year}{revision_letter.upper()}/output/chtml/part15/chapter_E.html"
    )

    assert dicom_standard_url(year, revision_letter) == expected_url


@pytest.mark.parametrize(("year", "revision_letter"), PUBLISHED_EDITIONS)
def test_dicom_standard_url_fetches_html(year: int, revision_letter: str):
    url = dicom_standard_url(year, revision_letter)

    with urlopen(url, timeout=30) as response:
        html = response.read()

    assert response.status == 200
    assert html