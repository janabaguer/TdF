"""
load_data.py

Downloads the raw data and rebuilds rider-stage results with full stage
times. Two sources, both pinned to a commit:

- TidyTuesday 2020-04-07 "Tour de France"
  (github.com/rfordatascience/tidytuesday, data/2020/2020-04-07):
  tdf_stages.csv, tdf_winners.csv, stage_data.csv -> data/raw/
- The `tdf` R package (github.com/alastairrushworth/tdf), which the
  TidyTuesday stage_data.csv was derived from: data/editions.rda
  -> data/raw/tdf_editions.rda

Why: in the TidyTuesday `stage_data.csv`, `time` and `elapsed` were R
`lubridate::period` objects and only their seconds component survived the
CSV export (see notebooks/01_eda.ipynb, section 5). The package's .rda file
still holds the full periods, so we read it directly. No R install needed.

Usage (from the repo root):
    python src/load_data.py

Output: data/processed/stage_results.csv, one row per rider x stage, with
    time_s     gap to the stage winner in seconds (for the winner: own stage time)
    elapsed_s  rider's total stage time in seconds
"""

from pathlib import Path
import urllib.request

import numpy as np
import pandas as pd
import rdata

# Pinned to commits so the raw data can't silently change under us
TIDYTUESDAY_COMMIT = "302efe5e2953e75b63ceb9787c2f4f823a93171e"
TIDYTUESDAY_URL = ("https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
                   f"{TIDYTUESDAY_COMMIT}/data/2020/2020-04-07/{{name}}")
TIDYTUESDAY_FILES = ["tdf_stages.csv", "tdf_winners.csv", "stage_data.csv"]

TDF_COMMIT = "20d3b2e8300dfad3ec21ade8a1d332a3dfba9fcf"
TDF_URL = f"https://raw.githubusercontent.com/alastairrushworth/tdf/{TDF_COMMIT}/data/editions.rda"

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_PATH = RAW_DIR / "tdf_editions.rda"
OUT_PATH = ROOT / "data" / "processed" / "stage_results.csv"

R_NA_INT = -2147483648  # R stores integer/logical NA as INT_MIN
T = rdata.parser.RObjectType


# --- Minimal helpers for walking the raw R object tree -----------------------
# rdata's automatic conversion mangles the nested list-of-dataframes column and
# doesn't know lubridate's Period class, so we read the parse tree ourselves.

def _symbol(obj) -> str:
    while obj.info.type == T.REF:
        obj = obj.referenced_object
    return obj.value.value.decode()


def _attributes(obj) -> dict:
    out, node = {}, obj.attributes
    while node is not None and node.info.type == T.LIST:
        out[_symbol(node.tag)] = node.value[0]
        node = node.value[1]
    return out


def _strings(obj) -> list:
    return [None if x.value is None else x.value.decode("utf8") for x in obj.value]


def _names(obj) -> list:
    return _strings(_attributes(obj)["names"])


def _column(obj) -> np.ndarray | list:
    """Convert one R vector to Python values, handling NA and Period."""
    attrs = _attributes(obj)
    if "class" in attrs and _strings(attrs["class"]) == ["Period"]:
        # A Period stores each unit in its own slot; the vector itself holds seconds
        with np.errstate(invalid="ignore"):  # NA (NaN) slots just propagate
            return (obj.value
                    + 60 * attrs["minute"].value
                    + 3600 * attrs["hour"].value
                    + 86400 * attrs["day"].value)
    if obj.info.type == T.STR:
        return _strings(obj)
    if obj.info.type in (T.INT, T.LGL):
        values = obj.value.astype(float)
        values[obj.value == R_NA_INT] = np.nan
        return values
    return obj.value


# --- Main pipeline ------------------------------------------------------------

def _download(url: str, path: Path, force: bool) -> None:
    if force or not path.exists():
        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, path)


def download_raw(force: bool = False) -> None:
    for name in TIDYTUESDAY_FILES:
        _download(TIDYTUESDAY_URL.format(name=name), RAW_DIR / name, force)
    _download(TDF_URL, RAW_PATH, force)


def load_stage_results(path: Path = RAW_PATH) -> pd.DataFrame:
    editions = rdata.parser.parse_file(path).object.value[0]
    ed_cols = dict(zip(_names(editions), editions.value))
    edition_ids = _column(ed_cols["edition"])
    start_days = _column(ed_cols["start_date"])  # R Date: days since 1970-01-01
    years = pd.to_datetime(start_days, unit="D").year

    frames = []
    for edition, year, stages in zip(edition_ids, years, ed_cols["stage_results"].value):
        for stage_id, table in zip(_names(stages), stages.value):
            df = pd.DataFrame({c: _column(v) for c, v in zip(_names(table), table.value)})
            df.insert(0, "stage_results_id", stage_id)
            df.insert(0, "year", year)
            df.insert(0, "edition", int(edition))
            frames.append(df)

    out = pd.concat(frames, ignore_index=True)
    out = out.rename(columns={"time": "time_s", "elapsed": "elapsed_s"})
    # rank mixes positions and codes (DNF, DNS, ...) across tables -> keep as string
    out["rank"] = out["rank"].map(lambda r: None if r is None or r != r
                                  else str(int(r)) if isinstance(r, float) else r)
    for col in ["age", "bib_number", "points"]:
        out[col] = out[col].astype("Int64")
    cols = ["edition", "year", "stage_results_id", "rank", "rider", "age", "team",
            "bib_number", "points", "time_s", "elapsed_s"]
    return out[cols]


if __name__ == "__main__":
    download_raw()
    results = load_stage_results()
    results.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(results):,} rows to {OUT_PATH.relative_to(ROOT)}")
