from src.choice_model.diagnostics import retain_nearest_sites, validate_choice_data
from src.choice_model.synthetic import generate_synthetic_choice_data


def test_synthetic_data_are_valid_choice_sets() -> None:
    frame = generate_synthetic_choice_data(n_choices=25, seed=7)
    result = validate_choice_data(frame)
    assert result["booking_decisions"] == 25
    assert result["exactly_one_chosen"]
    assert result["minimum_alternatives"] >= 2
    assert result["duplicate_choice_alternative_pairs"] == 0


def test_reduced_sets_retain_every_choice_and_chosen_alternative() -> None:
    frame = generate_synthetic_choice_data(n_choices=25, seed=8)
    reduced = retain_nearest_sites(frame, max_sites=3)
    assert reduced["choice_id"].nunique() == frame["choice_id"].nunique()
    assert reduced.groupby("choice_id")["chosen"].sum().eq(1).all()
    assert reduced.groupby("choice_id")["site_id"].nunique().le(3).all()

