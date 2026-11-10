# Choice-Based Demand Modelling

[![tests](https://github.com/Yixuan129/choice-based-demand-modelling/actions/workflows/tests.yml/badge.svg)](https://github.com/Yixuan129/choice-based-demand-modelling/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Open the interactive Streamlit demonstration](https://choice-based-demand-modelling.streamlit.app/)**

A privacy-safe, reproducible demonstration of booking-level customer choice
modelling. The project shows how feasible alternatives can be constructed for
each booking, how Multinomial Logit (MNL) and site-based Nested Logit (NL)
models allocate demand, and how product availability changes substitution.

> **Public demonstration:** the original case study used confidential
> operational data. This repository contains synthetic data and a reconstructed
> educational implementation only. It includes no customer-level records,
> proprietary tables, credentials or operational code.

## Why this project matters

Traditional demand models often forecast products independently. In practice,
customers may move to another pitch, another site or leave when their preferred
option is unavailable. Choice modelling treats demand as an allocation across
the alternatives available on each booking occasion.

The original industry project was completed with **Align-Alytics UK Ltd** for a
major UK leisure organisation. It combined large-scale data engineering,
interpretable statistical modelling and business communication.

## Case-study highlights

These figures describe the completed industry analysis; they are not generated
from the synthetic demo:

- **1,655,567** completed booking decisions and **18,417,523** feasible
  site-pitch alternative rows.
- A site-based NL model provided a better fit than MNL. The estimated nesting
  parameter was **0.4367**, supporting closer substitution among products at
  the same site.
- Under a broader geographical choice-set definition, **12 of 13 coefficient
  directions** remained unchanged.
- The main distance-based definition retained every booking decision while
  reducing alternative rows by **64.9%** relative to the regional definition.
- Adding site fixed effects reduced the estimated price coefficient by
  **59.9%**, indicating that unobserved site characteristics explained an
  important part of the positive price association.

The price result is treated as an association, not a causal response. The
framework supports demand allocation and forecasting; causal pricing would
require an additional identification strategy and richer search/no-booking
data.

## Repository contents

```text
.
├── app.py                         # Interactive substitution demo
├── data/README.md                 # Synthetic data schema and privacy note
├── docs/
│   ├── findings.md                # Industry findings and interpretation
│   ├── limitations.md             # Scope and responsible use
│   └── methodology.md             # MNL, NL and choice-set construction
├── notebooks/
│   └── choice_modelling_demo.ipynb
├── scripts/run_demo.py            # End-to-end synthetic workflow
├── src/choice_model/
│   ├── diagnostics.py
│   ├── estimation.py
│   ├── probabilities.py
│   └── synthetic.py
└── tests/                         # Probability and data-validation tests
```

## Quick start

```bash
git clone https://github.com/Yixuan129/choice-based-demand-modelling.git
cd choice-based-demand-modelling
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Generate synthetic data and estimate both models:

```bash
python scripts/run_demo.py --choices 600
```

Run the tests:

```bash
pytest -q
```

Launch the interactive demonstration:

```bash
streamlit run app.py
```

## Interactive scenario

The Streamlit app lets a user:

1. change the price of one synthetic product;
2. remove that product from the available choice set;
3. compare probability redistribution under MNL and Nested Logit; and
4. explore how the nesting parameter changes within-site substitution.

The coefficients in the app are illustrative and intentionally different from
the empirical estimates. The app is not a pricing tool.

## Methodological scope

- **Choice sets:** feasible products associated with each booking occasion.
- **MNL:** an interpretable baseline with IIA substitution.
- **Nested Logit:** products at the same site share a nest and may be closer
  substitutes.
- **Sensitivity analysis:** compare results under different geographical
  definitions of competition.
- **Site fixed effects:** diagnose whether stable site differences contribute
  to the observed price association.

See [Methodology](docs/methodology.md), [Findings](docs/findings.md) and
[Limitations](docs/limitations.md) for more detail.

## Responsible disclosure

Do not add real booking extracts, internal SQL, credentials, customer
identifiers, proprietary table names or company-only documentation to this
repository. The synthetic generator is the only supported data source for the
public demonstration.

## Author

**Yixuan Zhang**

MSc Operational Research and Data Science, University of Southampton

## Licence

The public demonstration code is available under the [MIT License](LICENSE).
Third-party publications and operational datasets are not included or licensed.

