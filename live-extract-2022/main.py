from extract import download_all_municipios
from process_municipios import get_sorted_extract_folders, process_municipios_from_folder
from datetime import datetime
from pathlib import Path


def friendly_format_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


if __name__ == "__main__":
    

    LIMIT_DOWNLOAD = None
    OUTPUT_PATH = Path(__file__).parents[1] / "processed" / "2022"

    download_all_municipios(LIMIT_DOWNLOAD)

    last_extract_path = get_sorted_extract_folders()[-1]
    municipio_res, partido_res = process_municipios_from_folder(last_extract_path)
    save_strdate  = friendly_format_datetime()
    municipio_res.to_csv(OUTPUT_PATH / f"municipios-2022-{save_strdate}.csv", index=False)
    partido_res.to_csv(OUTPUT_PATH / f"partidos-2022-{save_strdate}.csv", index=False)

    process_municipios_from_folder()
    breakpoint()