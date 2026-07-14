"""
bayesian_model.py

Hierarchical Bayesian model (PyMC) — the core methodological contribution
of this project. Partial pooling across riders lets riders with sparse
history borrow statistical strength from the population, which is the
mechanism behind H2 (better calibration, especially for sparse-data riders).

Suggested model sketch for Task A (regression), to refine after EDA:

    stage_result[i] ~ Normal(mu[i], sigma)
    mu[i] = alpha[rider[i]] + beta_stage_features . X_stage[i]
    alpha[rider] ~ Normal(alpha_pop, sigma_rider)     # partial pooling
    alpha_pop ~ Normal(0, 10)                          # population prior
    sigma_rider ~ HalfNormal(5)
    sigma ~ HalfNormal(5)

Consider also pooling by team, or a nested rider-within-team structure,
if EDA suggests meaningful team-level effects (e.g., domestiques vs. leaders).

For Task B (abandonment), a natural extension is a discrete-time survival
model: model hazard of abandoning at each stage as a function of race
progression and rider features, again with partial pooling over riders.

TODO (Week 5):
- [ ] Build model in PyMC, starting simple (pooled model, no hierarchy)
      as a sanity check before adding partial pooling
- [ ] Prior predictive checks before fitting
- [ ] Fit with NUTS, check convergence (r_hat, ESS, trace plots)
- [ ] Posterior predictive checks
- [ ] Extract posterior predictive intervals for the calibration comparison
- [ ] (Week 7) Extend to discrete-time survival model for Task B
"""

import pandas as pd


def build_hierarchical_model(X: pd.DataFrame, y: pd.Series, rider_idx):
    """Build and return an unfit PyMC model object.

    rider_idx: array mapping each row to an integer rider index, needed
    for the partial-pooling hierarchy.
    """
    raise NotImplementedError


def fit_model(model, draws: int = 1000, tune: int = 1000, chains: int = 4):
    """Fit via NUTS and return the InferenceData trace.

    Always check r_hat and ESS before trusting the posterior — don't skip
    this step even though it's tempting to jump straight to predictions.
    """
    raise NotImplementedError


def posterior_predictive_intervals(model, trace, X_new: pd.DataFrame, alpha: float = 0.1):
    """Generate posterior predictive samples and summarize as intervals."""
    raise NotImplementedError
