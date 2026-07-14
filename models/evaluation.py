"""
evaluation.py

Shared evaluation utilities used across all four models, so the comparison
in the final report is apples-to-apples. This module is arguably the most
important file in the repo — it's where the actual research question gets
answered.

TODO (Week 6):
- [ ] accuracy metrics: rmse(), mae() for Task A; auc(), brier_score() for Task B
- [ ] calibration_curve(): for a set of nominal coverage levels (e.g. 50%, 80%, 90%),
      compute the empirical coverage of each model's predictive intervals
- [ ] sharpness(): mean predictive interval width per model
- [ ] calibration_plot(): visualize nominal vs. empirical coverage (reliability diagram)
      across all models on one plot — this is the key comparison figure
- [ ] per_rider_calibration(): break down calibration by amount of rider history
      (few stages vs. many) — this is where H2 gets tested directly
- [ ] summary_table(): produce the final comparison table (accuracy + calibration +
      sharpness per model) for the report
"""

import numpy as np
import pandas as pd


def rmse(y_true, y_pred):
    raise NotImplementedError


def mae(y_true, y_pred):
    raise NotImplementedError


def calibration_curve(y_true, lower, upper, nominal_levels=(0.5, 0.8, 0.9)):
    """Empirical coverage of predictive intervals at each nominal level."""
    raise NotImplementedError


def sharpness(lower, upper):
    """Mean interval width — report alongside calibration, never alone."""
    raise NotImplementedError


def per_rider_calibration(y_true, lower, upper, rider_history_length):
    """Calibration broken down by how much historical data each rider had.

    This is the plot that tests H2 directly: does the Bayesian model's
    calibration advantage concentrate in low-history riders?
    """
    raise NotImplementedError


def summary_table(results: dict) -> pd.DataFrame:
    """Combine accuracy, calibration, and sharpness for all models into
    one comparison table for the final report."""
    raise NotImplementedError
