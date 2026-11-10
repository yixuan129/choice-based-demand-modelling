# Methodology

## 1. Booking-level choice data

Each row represents one feasible product within one booking decision. A valid
choice set contains at least two alternatives and exactly one selected product.
In the industry case study, an alternative was a site-pitch combination that was
available for the complete stay.

The public generator creates only synthetic alternatives. A distance field is
included so the demo can retain the chosen site and a limited number of nearby
competitors.

## 2. Utility specification

The demonstration uses a linear observed-utility function:

```text
V_ij = beta_price * price_ij
     + beta_awning * awning_ij
     + beta_availability * availability_ij
     + beta_category * category_ij
```

The synthetic generator also includes latent site quality to illustrate why
observational price coefficients may be confounded. Demo coefficients are not
the empirical case-study estimates.

## 3. Multinomial Logit

For booking decision `i`, the MNL probability of alternative `j` is:

```text
P_ij = exp(V_ij) / sum_k exp(V_ik)
```

MNL is transparent and computationally convenient, but its IIA property can
produce unrealistic substitution when several products share unobserved
features.

## 4. Site-based Nested Logit

The NL model groups pitch products offered by the same site. Alternatives in a
site nest may share unobserved utility. A common nesting parameter `lambda`
controls the relationship:

- `lambda = 1`: NL reduces to MNL;
- `0 < lambda < 1`: stronger dependence within site nests.

The implementation calculates conditional product probabilities within each
site and site probabilities across the available nests.

## 5. Estimation and validation

The demo estimates parameters by maximum likelihood using L-BFGS-B. It checks:

- exactly one chosen alternative per choice set;
- no duplicate decision-alternative pairs;
- probabilities sum to one within each choice set;
- NL matches MNL when `lambda = 1`; and
- optimisation convergence.

The public implementation is designed for explanation and testing on synthetic
samples, not for production-scale estimation.

