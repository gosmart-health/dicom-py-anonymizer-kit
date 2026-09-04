# dicom-py-anonymizer-kit

Developed by [GoSmart.Health](https://gosmart.health)

Utilities for working with DICOM de-identification rules from PS3.15 Annex E.
The project downloads Table E.1-1, the Application Level Confidentiality Profile
Attributes table, from the official DICOM standard website and exports the
parsed rules as JSON. The normalized records include the attribute name, DICOM
tag, retirement status, Standard IOD status, basic profile action, and option
actions.

The current data-generation workflow covers these editions:

- Current publication
- 2023E
- 2021B
- 2020E
- 2019E

The `model/` package contains Pydantic models for validating anonymization
profiles. The `lib/` package contains the DICOM URL builder and HTML scraper.
`pydicom` is included as a project dependency for the DICOM processing work that
will consume these profiles.

The resulting JSON file is used in [dicom-rs-transfomer](https://github.com/gosmart-health/dicom-rs-transformer) to perfom de-identification transformation step.

## Developer setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first,
then create the project environment and install its dependencies:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Tests make live requests to the official DICOM standard website, so network
access is required. The same test command runs in GitHub Actions on an Ubuntu
runner for pull requests targeting `main`.

## Generate profiles

Run the entry point from the project root:

```bash
uv run python main.py
```

This creates the `json/` directory when necessary and writes:

```text
json/anonymization_profile.current.json
json/anonymization_profile.2023e.json
json/anonymization_profile.2021b.json
json/anonymization_profile.2020e.json
json/anonymization_profile.2019e.json
```

Generated JSON files are ignored by Git because they are reproducible from the
official source pages.

## License and intended use

This project is released under the Apache License 2.0. It is intended for
non-clinical use only. Anyone integrating this project into a clinical system
is responsible for the integration, certification, validation, and verification
required for that clinical use.

