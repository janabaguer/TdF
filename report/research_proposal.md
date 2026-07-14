# Research Proposal: Probabilistic ML for Grand Tour Performance Prediction

## 1. Research question

Can probabilistic machine learning (specifically hierarchical Bayesian modeling) improve both predictive accuracy *and* uncertainty calibration in professional Grand Tour cycling, relative to classical statistical models and tree-based ensembles?

This is deliberately a *methods* question. Cycling is the application domain; the contribution is a disciplined comparison of modeling paradigms on a real, imperfect dataset.

## 2. Hypotheses

- **H1 (accuracy):** Tree-based models (Random Forest, XGBoost) will match or exceed classical regression on point-prediction accuracy, due to their ability to capture nonlinear interactions (e.g., stage type × rider specialty).
- **H2 (calibration):** The hierarchical Bayesian model will produce better-calibrated predictive intervals than classical or tree-based models, especially for riders with sparse historical data (partial pooling borrows strength from the population).
- **H3 (sharpness trade-off):** Better calibration from the Bayesian model may come at the cost of wider intervals for genuinely unpredictable riders/stages — this trade-off itself is a finding, not a failure.
- **H4 (interpretability):** Classical regression and the Bayesian model will offer more direct, domain-communicable explanations (coefficients, partial pooling shrinkage) than tree ensembles, which require post-hoc tools (e.g., SHAP) for equivalent insight.

## 3. Prediction tasks

### Task A (main): Stage performance prediction — regression
**Target:** rider's stage result, operationalized as time gap to stage winner (or GC position change, decided during EDA depending on data quality).
**Unit of analysis:** rider-stage.

### Task B (secondary): Abandonment probability — classification
**Target:** binary indicator of whether a rider abandons on/before a given stage.
**Unit of analysis:** rider-stage, with right-censoring for riders who finish the race.
**Note:** framed as an extension reusing Task A's pipeline, not a parallel full project — this keeps scope realistic for a 1-2 month timeline.

## 4. Data plan

**Sources:**
- ProCyclingStats (rider results, historical GC standings, team, age, stage-level times)
- Official race route data (stage distance, elevation gain, stage type: flat/hilly/mountain/ITT)

**Features (planned, subject to revision after EDA):**
- Rider-level: age, years as pro, historical GC finish, specialty (climber/sprinter/GC/domestique), team
- Stage-level: distance, elevation gain, stage type, days since last rest day, stage number within race
- Race-progression: cumulative fatigue proxy (e.g., rolling average of recent stage performance)

**Known limitation:** no physiological data (power, HR) is available for professional riders in public sources. Fatigue is proxied through performance trends, not measured directly. This limitation is stated explicitly in the final report rather than glossed over.

## 5. Models to compare

1. Regularized linear regression / logistic regression (baseline)
2. Random Forest
3. XGBoost
4. Hierarchical Bayesian model (PyMC), with partial pooling over riders (and possibly teams)

All four models are run on Task A. Models 1, 2 (as classifier), and 4 (as a survival/censored extension) are run on Task B.

## 6. Metrics

| Category | Metric | Why it matters |
|---|---|---|
| Accuracy | RMSE, MAE (Task A); AUC, Brier score (Task B) | Standard predictive performance |
| Calibration | Predictive interval coverage (e.g., 50%/90% intervals) | Do stated uncertainties match observed frequencies? |
| Sharpness | Mean interval width | Calibration without sharpness is not useful in practice |
| Interpretability | Qualitative comparison | What can each model tell a sports scientist, and how easily? |

## 7. What would count as a real finding

- If the Bayesian model's advantage is concentrated in riders with sparse history, that's a clean, explainable story about partial pooling.
- If tree-based models dominate on accuracy but are poorly calibrated, that's a genuine and useful trade-off finding for practitioners.
- Negative or mixed results are acceptable and worth reporting honestly — the goal is a rigorous comparison, not confirming a preferred method.

## 8. Timeline (6-8 weeks)

See main README for the week-by-week plan.
