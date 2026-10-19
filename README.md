# Grand Tour ML: A Probabilistic Analysis of Performance Prediction in Cycling

**Research question:** Can probabilistic machine learning improve performance prediction and uncertainty quantification in professional Grand Tour cycling, compared to classical and tree-based approaches?

This is a personal research project comparing four modeling paradigms — classical regression, tree-based ensembles, and hierarchical Bayesian models — on two prediction tasks in professional cycling. The goal isn't just point-prediction accuracy, but understanding *when* each modeling approach is actually useful to a sports scientist: what it gets right, where it's overconfident, and what it costs in interpretability.


## Tasks

1. **Stage performance prediction (main task, regression):** predict a rider's stage-level performance (finish time relative to stage winner / GC position change) using rider history and stage characteristics.
2. **Abandonment probability (secondary task, classification/survival):** predict the probability a rider abandons the race, given race progression, reusing most of the same feature pipeline.

## Models compared

| Model | Role |
|---|---|
| Linear / logistic regression (regularized) | Classical, interpretable baseline |
| Random Forest | Nonlinear baseline |
| Gradient Boosting (XGBoost) | Strong point-prediction benchmark |
| Hierarchical Bayesian model (PyMC) | Partial pooling across riders, calibrated uncertainty |

## Evaluation criteria

Point accuracy alone doesn't answer the research question. Each model is evaluated on:
- **Accuracy:** RMSE/MAE (regression), AUC/Brier score (classification)
- **Calibration:** do X% posterior/predictive intervals actually contain the outcome X% of the time?
- **Sharpness:** how wide are those intervals? (calibrated but useless if enormous)
- **Interpretability:** qualitative comparison of what each model can/can't explain to a domain expert

See [`report/research_proposal.md`](report/research_proposal.md) for the full research design.

## Repo structure

```
grand-tour-ml/
├── data/
│   ├── raw/            # untouched source data
│   └── processed/      # cleaned, feature-engineered datasets
├── notebooks/           # EDA and exploratory analysis
├── src/                 # data loading, cleaning, feature engineering code
├── models/
│   ├── linear_models.py
│   ├── random_forest.py
│   ├── xgboost_model.py
│   ├── bayesian_model.py
│   └── evaluation.py
├── report/
│   ├── research_proposal.md
│   └── findings.md      # final write-up (added at project end)
├── tests/
├── requirements.txt
└── README.md
```

## Status

🚧 In progress — see [`report/research_proposal.md`](report/research_proposal.md) for current phase and [PROGRESS.md](PROGRESS.md) for the running log.

## Data sources

The project uses the **TidyTuesday "Tour de France" dataset** (week of 2020-04-07), plus the R package it was built from. `python src/load_data.py` downloads all raw files into `data/raw/` (pinned to the commits below) and builds `data/processed/stage_results.csv`.

| Dataset | Files used | Content | License |
|---|---|---|---|
| **TidyTuesday: Tour de France** ([`rfordatascience/tidytuesday`](https://github.com/rfordatascience/tidytuesday/tree/302efe5e2953e75b63ceb9787c2f4f823a93171e/data/2020/2020-04-07), `data/2020/2020-04-07`, commit `302efe5`) | `tdf_stages.csv`, `tdf_winners.csv`, `stage_data.csv` | Stage distance and type, 1903–2017 (originally from [Kaggle](https://www.kaggle.com/jaminliu/a-brief-tour-of-tour-de-france-in-numbers/data)); overall winners; rider-stage results 1903–2019 | CC0 1.0 |
| **`tdf` R package** ([`alastairrushworth/tdf`](https://github.com/alastairrushworth/tdf), commit `20d3b2e`) | `data/editions.rda` | Same rider-stage results, with **full** stage times (originally scraped from Wikipedia) | GPL-2 |

**Why both:** in the TidyTuesday `stage_data.csv`, the `time` and `elapsed` columns lost their hours and minutes when exported to CSV (only the seconds survived; see `notebooks/01_eda.ipynb`, section 5). Rider results and times therefore come from the `tdf` package; stage characteristics come from TidyTuesday.

**References**

- R for Data Science Online Learning Community (2020). *TidyTuesday: Tour de France* (2020-04-07). https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-04-07
- Rushworth, A. (2020). *tdf: Tour de France data* (R package, version 0.0.1). https://github.com/alastairrushworth/tdf
- Liu, J. *A brief tour of Tour de France in numbers* (Kaggle dataset). https://www.kaggle.com/jaminliu/a-brief-tour-of-tour-de-france-in-numbers

All sources are public; no proprietary team data is used.

## License

MIT (see `LICENSE`)
