"""Small-sample MNL and nested-logit estimators for the public demo."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .probabilities import mnl_probabilities, nested_logit_probabilities


@dataclass(frozen=True)
class ModelResult:
    coefficients: pd.Series
    log_likelihood: float
    success: bool
    message: str
    lambda_param: float | None = None


def _validate_estimation_data(
    frame: pd.DataFrame, features: list[str], choice_col: str, chosen_col: str
) -> None:
    required = [choice_col, chosen_col, *features]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    chosen_per_set = frame.groupby(choice_col)[chosen_col].sum()
    if not chosen_per_set.eq(1).all():
        raise ValueError("Every choice set must contain exactly one chosen alternative.")


def fit_mnl(
    frame: pd.DataFrame,
    features: list[str],
    *,
    choice_col: str = "choice_id",
    chosen_col: str = "chosen",
) -> ModelResult:
    """Estimate an MNL model by maximum likelihood."""

    _validate_estimation_data(frame, features, choice_col, chosen_col)
    design = frame[features].to_numpy(dtype=float)
    chosen = frame[chosen_col].to_numpy(dtype=bool)

    def objective(beta: np.ndarray) -> float:
        working = frame[[choice_col]].copy()
        working["utility"] = design @ beta
        probability = mnl_probabilities(working, choice_col=choice_col).to_numpy()
        return float(-np.log(np.clip(probability[chosen], 1e-15, 1)).sum())

    optimum = minimize(objective, np.zeros(len(features)), method="L-BFGS-B")
    return ModelResult(
        coefficients=pd.Series(optimum.x, index=features, name="coefficient"),
        log_likelihood=-float(optimum.fun),
        success=bool(optimum.success),
        message=str(optimum.message),
    )


def fit_nested_logit(
    frame: pd.DataFrame,
    features: list[str],
    *,
    choice_col: str = "choice_id",
    chosen_col: str = "chosen",
    nest_col: str = "site_id",
) -> ModelResult:
    """Estimate a site-nested logit with one common nesting parameter."""

    _validate_estimation_data(frame, features, choice_col, chosen_col)
    if nest_col not in frame.columns:
        raise ValueError(f"Missing required column: {nest_col}")

    design = frame[features].to_numpy(dtype=float)
    chosen = frame[chosen_col].to_numpy(dtype=bool)

    def objective(parameters: np.ndarray) -> float:
        beta = parameters[:-1]
        lambda_param = parameters[-1]
        working = frame[[choice_col, nest_col]].copy()
        working["utility"] = design @ beta
        probability = nested_logit_probabilities(
            working,
            lambda_param,
            choice_col=choice_col,
            nest_col=nest_col,
        ).to_numpy()
        return float(-np.log(np.clip(probability[chosen], 1e-15, 1)).sum())

    initial = np.r_[np.zeros(len(features)), 0.8]
    bounds = [(None, None)] * len(features) + [(0.05, 1.0)]
    optimum = minimize(objective, initial, method="L-BFGS-B", bounds=bounds)
    return ModelResult(
        coefficients=pd.Series(optimum.x[:-1], index=features, name="coefficient"),
        lambda_param=float(optimum.x[-1]),
        log_likelihood=-float(optimum.fun),
        success=bool(optimum.success),
        message=str(optimum.message),
    )

