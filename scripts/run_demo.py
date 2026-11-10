"""Generate synthetic data, validate it and estimate demonstration models."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.choice_model.diagnostics import retain_nearest_sites, validate_choice_data
from src.choice_model.estimation import fit_mnl, fit_nested_logit
from src.choice_model.synthetic import DEFAULT_FEATURES, generate_synthetic_choice_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--choices", type=int, default=600)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output", type=Path, default=Path("data/synthetic_choice_data.csv")
    )
    args = parser.parse_args()

    frame = generate_synthetic_choice_data(n_choices=args.choices, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)

    validation = validate_choice_data(frame)
    reduced = retain_nearest_sites(frame, max_sites=3)
    mnl = fit_mnl(reduced, DEFAULT_FEATURES)
    nested = fit_nested_logit(reduced, DEFAULT_FEATURES)

    print("Synthetic data validation")
    for key, value in validation.items():
        print(f"  {key}: {value}")
    print(f"  reduced_alternative_rows: {len(reduced)}")
    print("\nMNL")
    print(mnl.coefficients.round(4).to_string())
    print(f"  log_likelihood: {mnl.log_likelihood:.2f}")
    print(f"  converged: {mnl.success}")
    print("\nNested Logit")
    print(nested.coefficients.round(4).to_string())
    print(f"  lambda: {nested.lambda_param:.4f}")
    print(f"  log_likelihood: {nested.log_likelihood:.2f}")
    print(f"  converged: {nested.success}")
    print(f"\nWrote synthetic data to {args.output}")


if __name__ == "__main__":
    main()

