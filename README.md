# Grand Tour ML: A Probabilistic Analysis of Performance Prediction in Cycling

**Research question:** Can probabilistic machine learning improve performance prediction and uncertainty quantification in professional Grand Tour cycling, compared to classical and tree-based approaches?

This is a personal research project comparing four modeling paradigms — classical regression, tree-based ensembles, and hierarchical Bayesian models — on two prediction tasks in professional cycling. The goal isn't just point-prediction accuracy, but understanding *when* each modeling approach is actually useful to a sports scientist: what it gets right, where it's overconfident, and what it costs in interpretability.

## Why this project

I wanted a project that let me practice building and honestly comparing statistical and ML methods on real, messy data — not a toy dataset — and that reflects something I'd want to talk about in a master's application or a sports-science interview: not "I took a Bayesian statistics course," but "I built a framework to compare how different models handle uncertainty in a real forecasting problem."

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

- [ProCyclingStats](https://www.procyclingstats.com) — rider results, stage profiles, startlists
- Official Grand Tour race data (stage profiles, categorization)

Data acquisition respects each source's terms of service; no proprietary team data is used.

## License

MIT (see `LICENSE`)
