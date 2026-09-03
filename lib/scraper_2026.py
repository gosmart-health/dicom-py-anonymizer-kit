import json
import re
import requests
from bs4 import BeautifulSoup

def extract_table_e1_1(url: str) -> list[dict]:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Locate table E.1-1
    table = soup.find("table", {"id": "table_E.1-1"})
    if table is None:
        anchor = soup.find(id="table_E.1-1")
        if anchor is not None:
            table_container = anchor.find_parent("div", class_="table")
            if table_container is not None:
                table = table_container.find("table")

    if table is None:
        caption = soup.find(
            "caption", string=re.compile(r"Table\s+E\.1-1", re.IGNORECASE)
        )
        if caption is None:
            raise ValueError("Could not find Table E.1-1 in the DICOM document")
        table = caption.find_parent("table")

    if table is None:
        raise ValueError("Table E.1-1 caption is not inside a table")

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")

    records = []
    for tr in rows:
        cells = [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])]
        if not cells or all(cell.name == "th" for cell in tr.find_all(["td", "th"])):
            continue
        cells.extend([""] * (15 - len(cells)))

        record = {
            "attribute_name": cells[0],
            "tag": cells[1],
            "retired": cells[2].upper() == "Y",
            "in_std_comp_iod": cells[3].upper() == "Y",
            "basic_profile": cells[4],
            "options": {
                "retain_safe_private": cells[5] or None,
                "retain_uids": cells[6] or None,
                "retain_dev_id": cells[7] or None,
                "retain_inst_id": cells[8] or None,
                "retain_pat_chars": cells[9] or None,
                "retain_long_full_dates": cells[10] or None,
                "retain_long_mod_dates": cells[11] or None,
                "clean_desc": cells[12] or None,
                "clean_struct_cont": cells[13] or None,
                "clean_graph": cells[14] or None,
            }
        }
        records.append(record)

    return records

