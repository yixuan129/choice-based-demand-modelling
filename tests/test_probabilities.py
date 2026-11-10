import numpy as np
import pandas as pd

from src.choice_model.probabilities import (
    mnl_probabilities,
    nested_logit_probabilities,
)


def example_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "choice_id": [1, 1, 1, 1, 2, 2, 2],
            "site_id": ["A", "A", "B", "B", "A", "A", "C"],
            "utility": [0.2, 0.7, -0.1, 0.4, 0.0, 0.3, 0.8],
        }
    )


def test_mnl_probabilities_sum_to_one() -> None:
    frame = example_frame()
    probability = mnl_probabilities(frame)
    sums = probability.groupby(frame["choice_id"]).sum()
    assert np.allclose(sums, 1.0)


def test_nested_probabilities_sum_to_one() -> None:
    frame = example_frame()
    probability = nested_logit_probabilities(frame, lambda_param=0.55)
    sums = probability.groupby(frame["choice_id"]).sum()
    assert np.allclose(sums, 1.0)


def test_nested_logit_reduces_to_mnl_at_lambda_one() -> None:
    frame = example_frame()
    mnl = mnl_probabilities(frame)
    nested = nested_logit_probabilities(frame, lambda_param=1.0)
    assert np.allclose(mnl, nested)

