"""Choice-probability functions used by the public demonstration.

The implementation favours clarity over production-scale performance. The
original case study used a separate workflow designed for tens of millions of
alternative rows; that operational code and data are not included here.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import logsumexp


def _validate_columns(frame: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def mnl_probabilities(
    frame: pd.DataFrame,
    *,
    utility_col: str = "utility",
    choice_col: str = "choice_id",
) -> pd.Series:
    """Return stable multinomial-logit probabilities for each choice set."""

    _validate_columns(frame, [utility_col, choice_col])
    probabilities = pd.Series(index=frame.index, dtype=float, name="probability")

    for _, group in frame.groupby(choice_col, sort=False):
        utility = group[utility_col].to_numpy(dtype=float)
        log_prob = utility - logsumexp(utility)
        probabilities.loc[group.index] = np.exp(log_prob)

    return probabilities


def nested_logit_probabilities(
    frame: pd.DataFrame,
    lambda_param: float,
    *,
    utility_col: str = "utility",
    choice_col: str = "choice_id",
    nest_col: str = "site_id",
) -> pd.Series:
    """Return nested-logit probabilities with one common nesting parameter.

    Alternatives within a site form a nest. ``lambda_param=1`` reproduces MNL;
    values below one allow stronger dependence among alternatives in a nest.
    """

    _validate_columns(frame, [utility_col, choice_col, nest_col])
    if not 0 < lambda_param <= 1:
        raise ValueError("lambda_param must be in the interval (0, 1].")

    probabilities = pd.Series(index=frame.index, dtype=float, name="probability")

    for _, choice_set in frame.groupby(choice_col, sort=False):
        nest_log_sums: dict[object, float] = {}
        conditional_logs: dict[object, np.ndarray] = {}

        for nest_id, nest in choice_set.groupby(nest_col, sort=False):
            scaled_utility = nest[utility_col].to_numpy(dtype=float) / lambda_param
            nest_log_sum = logsumexp(scaled_utility)
            nest_log_sums[nest_id] = nest_log_sum
            conditional_logs[nest_id] = scaled_utility - nest_log_sum

        nest_ids = list(nest_log_sums)
        inclusive_utilities = np.array(
            [lambda_param * nest_log_sums[nest_id] for nest_id in nest_ids]
        )
        nest_log_probabilities = inclusive_utilities - logsumexp(inclusive_utilities)
        nest_log_probability = dict(zip(nest_ids, nest_log_probabilities, strict=True))

        for nest_id, nest in choice_set.groupby(nest_col, sort=False):
            joint_log_probability = (
                nest_log_probability[nest_id] + conditional_logs[nest_id]
            )
            probabilities.loc[nest.index] = np.exp(joint_log_probability)

    return probabilities

