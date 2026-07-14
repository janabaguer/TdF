"""
linear_models.py

Classical baseline models for both tasks:
- Task A (regression): Ridge/Lasso regression on stage performance
- Task B (classification): Logistic regression on abandonment probability

This is the interpretability anchor of the comparison — coefficients here
should be directly explainable to a non-ML audience (e.g. "each additional
1000m of elevation gain is associated with X seconds of time loss").

TODO (Week 4):
- [ ] Implement fit_regression(X, y) using sklearn Ridge/Lasso with CV for alpha
- [ ] Implement fit_classification(X, y) using sklearn LogisticRegression
- [ ] Report coefficients with confidence intervals (statsmodels may be
      preferable to sklearn here for inference, not just prediction)
- [ ] Produce prediction intervals for regression (e.g. via residual
      bootstrap) so this model can be included in the calibration comparison
"""

import numpy as np
import pandas as pd


def fit_regression(X: pd.DataFrame, y: pd.Series):
    """Fit a regularized linear regression baseline for Task A.

    Returns a fitted model plus whatever's needed to generate prediction
    intervals later (e.g., residual std, or a statsmodels results object).
    """
    raise NotImplementedError


def fit_classification(X: pd.DataFrame, y: pd.Series):
    """Fit a logistic regression baseline for Task B (abandonment)."""
    raise NotImplementedError


def predict_with_interval(model, X_new: pd.DataFrame, alpha: float = 0.1):
    """Return point predictions plus (1-alpha) prediction intervals.

    Needed so this baseline can be compared on calibration/sharpness,
    not just point accuracy.
    """
    raise NotImplementedError
