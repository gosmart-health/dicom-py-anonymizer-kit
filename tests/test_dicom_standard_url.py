from urllib.request import urlopen

import pytest
import requests

from lib.dicom_standard_url import dicom_standard_url
from lib.scraper_2026 import extract_table_e1_1


EDITIONS = (
    ("current", ""),
    (2023, "e"),
    (2021, "b"),
    (2020, "e"),
    (2019, "e"),
)


@pytest.mark.parametrize(("year", "revision_letter"), EDITIONS)
def test_dicom_standard_url_generates_expected_url(
    year: int | str, revision_letter: str
):
    dicom = "dicom" if year == "current" else "Dicom"
    expected_url = (
        f"https://dicom.nema.org/medical/{dicom}/"
        f"{year}{revision_letter.upper()}/output/chtml/part15/chapter_E.html"
    )

    assert dicom_standard_url(year, revision_letter) == expected_url


@pytest.mark.parametrize(("year", "revision_letter"), EDITIONS)
def test_dicom_standard_url_fetches_html(year: int | str, revision_letter: str):
    url = dicom_standard_url(year, revision_letter)

    with urlopen(url, timeout=30) as response:
        html = response.read()

    assert response.status == 200
    assert html


@pytest.mark.parametrize(("year", "revision_letter"), EDITIONS)
def test_extract_table_e1_1_parses_each_published_edition(
    year: int | str, revision_letter: str
):
    records = extract_table_e1_1(dicom_standard_url(year, revision_letter))

    assert records
    assert all(
        {
            "attribute_name",
            "tag",
            "retired",
            "in_std_comp_iod",
            "basic_profile",
            "options",
        }
        <= record.keys()
        for record in records
    )


def test_extract_table_e1_1_does_not_drop_short_rows(monkeypatch):
    html = """
    <table id="table_E.1-1">
      <tr><th>Attribute Name</th><th>Tag</th></tr>
      <tr><td>First Attribute</td><td>(0008,0005)</td></tr>
      <tr><td>Second Attribute</td></tr>
    </table>
    """

    class Response:
        content = html.encode()

        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda url: Response())

    records = extract_table_e1_1("https://example.test/dicom.html")

    assert [record["attribute_name"] for record in records] == [
        "First Attribute",
        "Second Attribute",
    ]