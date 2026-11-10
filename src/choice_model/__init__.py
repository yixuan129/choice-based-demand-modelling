"""Public demonstration utilities for booking-level choice modelling."""

from .estimation import fit_mnl, fit_nested_logit
from .probabilities import mnl_probabilities, nested_logit_probabilities
from .synthetic import DEFAULT_FEATURES, generate_synthetic_choice_data

__all__ = [
    "DEFAULT_FEATURES",
    "fit_mnl",
    "fit_nested_logit",
    "generate_synthetic_choice_data",
    "mnl_probabilities",
    "nested_logit_probabilities",
]

