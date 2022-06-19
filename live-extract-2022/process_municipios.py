from uuid import uuid4
import xmltodict
import pandas as pd
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "extract"


def extract_municipio(res: dict) -> pd.DataFrame:
    municipio = {}
    municipio["Escrutado"] = float(res["porciento_escrutado"]) / 100
    municipio["Municipio Descargado"] = res["nombre_sitio"]
    for vote_type, vote_data in res["votos"].items():
        municipio[vote_type.capitalize()] = vote_data["cantidad"]
    return pd.DataFrame([municipio])


def extract_partidos(res: dict) -> pd.DataFrame:
    partidos = [
        {
            "Partido": party["nombre"],
            "Votos": party["votos_numero"],
            "Escrutado": float(res["porciento_escrutado"]) / 100,
            "Municipio Descargado": res["nombre_sitio"],
        }
        for party in res["resultados"]["partido"]
    ]
    return pd.DataFrame(partidos)


def add_ids(df, ids) -> pd.DataFrame:
    df = df.copy()
    # convert ids to int to remove 0-prefix
    df["ID Provincia"] = int(ids[1])
    df["ID Municipio"] = int(ids[2])
    df["Nombre Municipio"] = ids[0]
    return df


def process_municipio(path, ids) -> dict:
    with open(path, encoding="utf-8") as fd:
        results = xmltodict.parse(fd.read())["escrutinio_sitio"]

    municipio = extract_municipio(results)
    partidos = extract_partidos(results)

    municipio = add_ids(municipio, ids)
    partidos = add_ids(partidos, ids)
    return {"municipio": municipio, "partidos": partidos}


def get_sorted_extract_folders():
    return sorted([p for p in INPUT_PATH.iterdir() if p.is_dir()])


def process_municipios_from_folder(path_folder):
    processed_data = []
    for xml_path in path_folder.glob("*.xml"):
        ids = xml_path.stem.split("_")
        processed_data.append(process_municipio(xml_path, ids))
    municipio_res = pd.concat(
        [data["municipio"] for data in processed_data], axis=0, ignore_index=True
    )
    partido_res = pd.concat(
        [data["partidos"] for data in processed_data], axis=0, ignore_index=True
    )
    return municipio_res, partido_res


if __name__ == "__main__":
    res = process_municipio("Abla-04-01.xml")
    breakpoint()
