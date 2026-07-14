"""
xgboost_model.py

Gradient boosting benchmark — typically the strongest point-prediction
model in the comparison. Included specifically to test H1 (accuracy) and
to see whether its accuracy advantage, if any, survives the calibration
check (H2/H3).

TODO (Week 4):
- [ ] Implement fit_regression(X, y) using xgboost.XGBRegressor
- [ ] Implement fit_classification(X, y) using xgboost.XGBClassifier
- [ ] Hyperparameter search (small grid or Optuna — keep it modest, this
      isn't a Kaggle leaderboard project)
- [ ] Prediction intervals via quantile loss objective (XGBoost supports
      quantile regression natively) — fit separate models for e.g. the
      5th/50th/95th percentiles
"""

import pandas as pd


def fit_regression(X: pd.DataFrame, y: pd.Series):
    """Fit an XGBoost regressor for Task A."""
    raise NotImplementedError


def fit_classification(X: pd.DataFrame, y: pd.Series):
    """Fit an XGBoost classifier for Task B."""
    raise NotImplementedError


def predict_with_interval(X_new: pd.DataFrame, alpha: float = 0.1):
    """Prediction intervals via separately-trained quantile regressors."""
    raise NotImplementedError
