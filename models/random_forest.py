"""
random_forest.py

Tree-based nonlinear baseline for both tasks using sklearn's RandomForest.

TODO (Week 4):
- [ ] Implement fit_regression(X, y) — RandomForestRegressor with CV grid
      over n_estimators/max_depth
- [ ] Implement fit_classification(X, y) — RandomForestClassifier
- [ ] Feature importance extraction (built-in + permutation importance,
      since built-in importances are biased toward high-cardinality features)
- [ ] Prediction intervals via quantile regression forests
      (see: sklearn's experimental quantile support, or skgarden/quantile-forest)
      — needed to include RF in the calibration comparison, not just accuracy
"""

import pandas as pd


def fit_regression(X: pd.DataFrame, y: pd.Series):
    """Fit a Random Forest regressor for Task A."""
    raise NotImplementedError


def fit_classification(X: pd.DataFrame, y: pd.Series):
    """Fit a Random Forest classifier for Task B."""
    raise NotImplementedError


def predict_with_interval(model, X_new: pd.DataFrame, alpha: float = 0.1):
    """Quantile-based prediction intervals from the forest's tree distribution."""
    raise NotImplementedError


def feature_importance(model, feature_names: list):
    """Return both built-in and permutation-based importances for comparison."""
    raise NotImplementedError
