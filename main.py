import json
from pathlib import Path

from lib.dicom_standard_url import dicom_standard_url
from lib.scraper_2026 import extract_table_e1_1


def main():
    editions = (
        ("current", ""),
        (2023, "e"),
        (2021, "b"),
        (2020, "e"),
        (2019, "e"),
    )
    output_dir = Path("json")
    output_dir.mkdir(parents=True, exist_ok=True)

    for year, revision_letter in editions:
        data = extract_table_e1_1(dicom_standard_url(year, revision_letter))
        version = f"{year}{revision_letter}"
        output_path = output_dir / f"anonymization_profile.{version}.json"
        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(data, output_file, indent=2, ensure_ascii=False)
        print(f"Extracted {len(data)} tags into {output_path}")



if __name__ == "__main__":
    main()