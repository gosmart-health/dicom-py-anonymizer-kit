def dicom_standard_url(
        year: int | str = "current",
        revision_letter: str = "",
        part_number: int = 15,
        chapter_letter_or_number: str = "E"
):
    """
    Returns the URL of the DICOM standard for the specified year, revision letter, part number, and chapter letter or number.
    Tested with years 2013, 2016, 2019, 2020, 2021, 2023, and "current" (latest published version).
    """
    dicom = "dicom" if year == "current" else "Dicom"
    return f"https://dicom.nema.org/medical/{dicom}/{year}{revision_letter.upper()}/output/chtml/part{part_number}/chapter_{chapter_letter_or_number}.html"

