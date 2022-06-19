from bdb import Breakpoint
from re import TEMPLATE
from turtle import down
from urllib.request import urlretrieve
from urllib.error import URLError
from datetime import datetime
from pathlib import Path
import time

PATH_TEMPLATE = Path(__file__).parent / "municipios-template.csv"
PARENT_OUTPUT_PATH = Path(__file__).parent / "extract"
ELPAIS_URL = (
    "https://rsl00.epimg.net/elecciones/2018/autonomicas/01/{province}/{municipio}.xml2"
)

# PARENT_OUTPUT_PATH.mkdir(parents=True, exist_ok=False)


def add_prefix_zero_to_ids(ids: list) -> list:
    return [(id if len(id) > 1 else "0" + id) for id in ids]


def get_ids(path) -> list:
    with open(path, encoding="utf8") as fd:
        template_lines = fd.readlines()
    ids = [add_prefix_zero_to_ids(line.split(",")[:3]) for line in template_lines[1:]]
    return ids


def download_xml_from_id(output_path, ids: list) -> None:
    try:
        urlretrieve(
            ELPAIS_URL.format(**{"province": ids[0], "municipio": ids[1]}),
            output_path / f"{ids[2]}_{ids[0]}_{ids[1]}.xml",
        )
    except URLError:
        print(f"{datetime.now()}: Error downloading data for {ids}")


def download_all_municipios(limit=None) -> None:
    ids = get_ids(PATH_TEMPLATE)
    output_path = PARENT_OUTPUT_PATH / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path.mkdir(parents=False, exist_ok=False)
    for index, id in enumerate(ids):
        print(f"{datetime.now()}: Preparing download for {id}")
        if index == limit:
            return
        download_xml_from_id(output_path, id)
        time.sleep(1)
