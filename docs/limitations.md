# Limitations and Responsible Use

## Completed bookings only

The case-study sample contained completed bookings. It did not observe customers
who searched and left without booking, so it modelled allocation among available
products rather than total market demand or purchase incidence.

## Constructed choice sets

The products considered by each customer were not directly observed. Geographic
and full-stay availability rules therefore approximated feasible competition.
Sensitivity analysis supported the main coefficient directions, but no
constructed set can fully recover an unobserved consideration process.

## Price endogeneity

Prices can reflect site quality, seasonality, expected demand and the pricing
process. The positive observational coefficient must not be interpreted as
evidence that increasing price causes demand to rise. The public app therefore
uses illustrative coefficients and carries no pricing recommendation.

## Synthetic public data

Synthetic records reproduce only the shape of a choice problem. They cannot be
used to reproduce the empirical estimates, evaluate the original client or draw
conclusions about real customers.

## Production scale

The public Python implementation uses readable group-wise calculations. The
industry workflow required separate memory and performance engineering for tens
of millions of rows.

