# Case-Study Findings

## Product attributes

Awning permission was positively associated with observed choice, while the
minimum availability ratio was negatively associated. Pitch-category estimates
also differed relative to the Hardstanding reference category. These are
conditional associations within completed bookings.

## Within-site substitution

The site-based Nested Logit model fitted the observed choices better than MNL.
Its estimated nesting parameter was `0.4367` with a 95% confidence interval of
`[0.4355, 0.4378]`. The MNL restriction `lambda = 1` was rejected, supporting
closer substitution among pitch products at the same site.

## Choice-set robustness

The distance-based model contained 18,417,523 alternative rows; the matched
regional model contained 52,510,003. The distance rule reduced rows by 64.9%
while retaining the same 1,655,567 booking decisions. Twelve of thirteen
coefficient directions remained unchanged.

## Price diagnostic

The main price coefficient was positive. Adding site fixed effects in a matched
diagnostic sample reduced the estimate from `0.0926` to `0.0371`, a 59.9%
decrease. This is consistent with price capturing part of the effect of stable,
unobserved differences in location, facilities or general site appeal.

The diagnostic did not establish a causal price effect. Site fixed effects do
not remove time-varying demand, occupancy-period, booking-lead-time or dynamic
pricing factors.

## Business interpretation

The NL framework provides an interpretable basis for allocating forecast demand
across available products and examining redistribution when availability or
product mix changes. Pricing applications require additional data and a separate
identification strategy.

