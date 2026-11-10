"""Generate a fully synthetic campsite-choice dataset.

The generator reflects only the structure of a booking-level choice problem.
It does not reproduce or approximate any customer record from the case study.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .probabilities import nested_logit_probabilities

DEFAULT_FEATURES = [
    "price_per_10",
    "awning",
    "minimum_availability_ratio",
    "is_grass",
    "is_serviced",
]


def generate_synthetic_choice_data(
    n_choices: int = 1_500,
    n_sites: int = 18,
    sites_per_choice: int = 4,
    seed: int = 42,
) -> pd.DataFrame:
    """Create synthetic alternatives and one simulated choice per booking."""

    if n_choices < 1:
        raise ValueError("n_choices must be positive.")
    if n_sites < sites_per_choice:
        raise ValueError("n_sites must be at least sites_per_choice.")

    rng = np.random.default_rng(seed)
    site_ids = np.array([f"S{site:03d}" for site in range(1, n_sites + 1)])
    site_quality = dict(zip(site_ids, rng.normal(0, 0.9, n_sites), strict=True))
    site_base_price = {
        site: 28 + 7.5 * site_quality[site] + rng.normal(0, 2.5)
        for site in site_ids
    }
    categories = ("Hardstanding", "Standard Grass", "Serviced")
    category_price = {"Hardstanding": 0.0, "Standard Grass": -3.0, "Serviced": 8.0}
    category_utility = {"Hardstanding": 0.0, "Standard Grass": -0.5, "Serviced": 0.35}

    rows: list[dict[str, object]] = []
    for choice_id in range(1, n_choices + 1):
        season = rng.uniform(-1, 1)
        candidate_sites = rng.choice(site_ids, size=sites_per_choice, replace=False)
        distances = rng.uniform(2, 120, sites_per_choice)

        for site_id, distance_km in zip(candidate_sites, distances, strict=True):
            available_categories = rng.choice(
                categories,
                size=int(rng.integers(2, len(categories) + 1)),
                replace=False,
            )
            for category in available_categories:
                awning = int(rng.random() < (0.72 if category != "Standard Grass" else 0.55))
                availability = np.clip(
                    rng.beta(3.5, 2.2) - 0.08 * season - 0.04 * site_quality[site_id],
                    0.02,
                    1.0,
                )
                full_stay_price = max(
                    12.0,
                    site_base_price[site_id]
                    + category_price[category]
                    + 5.5 * season
                    + rng.normal(0, 2.0),
                )
                systematic_utility = (
                    -0.11 * (full_stay_price / 10)
                    + 0.75 * awning
                    - 0.45 * availability
                    - 0.012 * distance_km
                    + category_utility[category]
                    + 1.0 * site_quality[site_id]
                )
                rows.append(
                    {
                        "choice_id": choice_id,
                        "site_id": site_id,
                        "pitch_category": category,
                        "price_per_10": full_stay_price / 10,
                        "awning": awning,
                        "minimum_availability_ratio": availability,
                        "distance_km": distance_km,
                        "is_grass": int(category == "Standard Grass"),
                        "is_serviced": int(category == "Serviced"),
                        "utility": systematic_utility,
                    }
                )

    frame = pd.DataFrame(rows)
    frame.insert(
        1,
        "alternative_id",
        frame.groupby("choice_id").cumcount().add(1).map(lambda value: f"A{value:02d}"),
    )
    probabilities = nested_logit_probabilities(frame, 0.55)
    frame["chosen"] = 0

    for _, choice_set in frame.groupby("choice_id", sort=False):
        probability = probabilities.loc[choice_set.index].to_numpy()
        chosen_index = rng.choice(choice_set.index.to_numpy(), p=probability)
        frame.loc[chosen_index, "chosen"] = 1

    return frame.drop(columns="utility")

