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
**Target:** rider's stage result, operationalized as the log time gap to the stage winner, $\log(1 + \text{gap in seconds})$ (decided during EDA, see `notebooks/01_eda.ipynb`, section 8).
**Reference choice:** the gap is measured from the stage winner, not the median finisher. When a breakaway stays away (≥ 1 min ahead of the median finisher on 34% of flat stages since 1970), every rider's gap is inflated by the breakaway's margin. This is handled by a per-stage random effect, which absorbs the shift, rather than by changing the reference.

**Alternative tested and rejected: the median finisher as reference.** Measuring each rider's gap from the stage's median finisher would remove the breakaway effect directly. Because this gap is negative for half the riders, it was combined with three transforms that allow negative values: a signed log, $\text{sign}(x)\log(1+|x|)$, and $\text{asinh}(x/c)$ with $c$ = 60 s and $c$ = 300 s (1970+ finishers, EDA section 8.5). It made the target worse:
- **More zeros:** on flat stages the median finisher sits in the bunch, so **72%** of flat-stage finishers get a gap of exactly zero (vs 38% with the winner as reference). Over all stage types, that's **44%** of rows (vs 20.5%).
- **Two humps under every transform:** on hilly and mountain stages the median rider usually rides in a large group of dropped riders. Faster riders are minutes below it and slower riders minutes above, with almost nobody in between, so the distribution splits into two humps.

Because these shapes come from the reference, not the transform, no choice of transform fixes them. They would also require a far more complex likelihood (a spike at zero plus a two-component mixture). The winner reference with a per-stage effect solves the breakaway problem without these side effects.

**Unit of analysis:** rider-stage.

### Task B (secondary): Abandonment probability — classification
**Target:** binary indicator of whether a rider abandons on/before a given stage.
**Unit of analysis:** rider-stage, with right-censoring for riders who finish the race.
**Note:** framed as an extension reusing Task A's pipeline, not a parallel full project — this keeps scope realistic for a 1-2 month timeline.

## 4. Data plan

**Sources:**
- TidyTuesday "Tour de France" dataset (2020-04-07): stage distance and stage type (1903–2017), overall winners
- `tdf` R package (A. Rushworth): rider-stage results with full stage times, rank, team, age (1903–2019)

See the README for full citations. No elevation data is available in these sources.

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
