"""Validation helpers for synthetic choice-set demonstrations."""

from __future__ import annotations

import pandas as pd


def validate_choice_data(frame: pd.DataFrame) -> dict[str, float | int | bool]:
    """Return core choice-set validation checks."""

    chosen_per_choice = frame.groupby("choice_id")["chosen"].sum()
    alternatives_per_choice = frame.groupby("choice_id").size()
    duplicate_pairs = frame.duplicated(["choice_id", "alternative_id"]).sum()
    return {
        "booking_decisions": int(frame["choice_id"].nunique()),
        "alternative_rows": int(len(frame)),
        "exactly_one_chosen": bool(chosen_per_choice.eq(1).all()),
        "minimum_alternatives": int(alternatives_per_choice.min()),
        "duplicate_choice_alternative_pairs": int(duplicate_pairs),
    }


def retain_nearest_sites(frame: pd.DataFrame, max_sites: int = 3) -> pd.DataFrame:
    """Keep the chosen site and the nearest sites in each synthetic choice set."""

    if max_sites < 1:
        raise ValueError("max_sites must be positive.")

    retained_indices: list[int] = []
    for _, choice_set in frame.groupby("choice_id", sort=False):
        site_distance = choice_set.groupby("site_id")["distance_km"].min().sort_values()
        chosen_site = choice_set.loc[choice_set["chosen"].eq(1), "site_id"].iloc[0]
        retained_sites = [chosen_site]
        retained_sites.extend(
            site for site in site_distance.index if site != chosen_site
        )
        retained_sites = retained_sites[:max_sites]
        retained_indices.extend(choice_set.index[choice_set["site_id"].isin(retained_sites)])

    return frame.loc[retained_indices].copy().reset_index(drop=True)

