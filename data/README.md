# Data

The operational booking data used in the original case study are confidential
and are **not included** in this repository.

Run the following command from the repository root to generate a completely
synthetic dataset with a similar *choice-set structure*:

```bash
python scripts/run_demo.py --choices 600
```

The generated file, `synthetic_choice_data.csv`, is ignored by Git. Synthetic
site identifiers, prices, availability values and choices have no relationship
to any real customer, campsite or booking.

## Synthetic schema

| Field | Meaning |
|---|---|
| `choice_id` | Synthetic booking-level choice occasion |
| `alternative_id` | Alternative within a choice occasion |
| `site_id` | Synthetic site and NL nest |
| `pitch_category` | Illustrative product category |
| `price_per_10` | Synthetic full-stay price divided by ten |
| `awning` | Illustrative binary product attribute |
| `minimum_availability_ratio` | Synthetic remaining-capacity measure |
| `distance_km` | Synthetic distance used to demonstrate choice-set reduction |
| `chosen` | One for the simulated selected alternative |

