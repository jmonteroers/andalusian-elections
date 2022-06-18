import pandas as pd
from pandas import DataFrame


def concatenate(dfs: list[DataFrame]) -> DataFrame:
    complete_df = dfs[0]
    for df in dfs[1:]:
        complete_df = pd.concat([complete_df, df], axis=0, ignore_index=True)
    return complete_df


def create_municipio_results(results: DataFrame) -> DataFrame:
    municipios = results.copy()
    municipios = municipios.loc[
        :,
        [
            "Codcir",
            "Codmun",
            "Municipio",
            "Censo Total",
            "Votos Totales",
            "Votos Nulos",
            "Votos Blancos",
        ],
    ]
    return municipios


def create_party_results(results: DataFrame) -> DataFrame:
    parties: DataFrame = results.copy()
    parties = parties.iloc[
        :, [0, 1, 2] + list(range(13, len(parties.columns)))
    ]
    parties = parties.melt(id_vars=["Codcir", "Codmun", "Municipio"], var_name="Party", value_name="Votes")
    parties["Votes"].fillna("0", inplace=True)
    return parties


if __name__ == "__main__":
    from pathlib import Path

    INPUT_PATH = Path(__file__).parent / "input" / "2018"
    OUTPUT_PATH = Path(__file__).parent / "processed" / "2018"
    dfs = [pd.read_csv(filepath, sep=";", dtype="object") for filepath in INPUT_PATH.glob("*.csv")]
    results = concatenate(dfs)
    results = results.loc[results["Codcir"] != "Total"]
    municipio_res = create_municipio_results(results)
    party_res = create_party_results(results)

    # saving
    municipio_res.to_csv(OUTPUT_PATH / "municipios-2018.csv", index=False)
    party_res.to_csv(OUTPUT_PATH / "parties-2018.csv", index=False)