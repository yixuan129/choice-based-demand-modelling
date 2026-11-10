"""Interactive public demonstration of product substitution."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from src.choice_model.probabilities import (
    mnl_probabilities,
    nested_logit_probabilities,
)

st.set_page_config(page_title="Choice-Based Demand Modelling", page_icon="🏕️", layout="wide")

st.title("Choice-Based Demand Modelling")
st.caption(
    "A synthetic demonstration of how customer choice probabilities can move "
    "across related products. No operational or customer data are used."
)

with st.sidebar:
    st.header("Scenario controls")
    price_change = st.slider(
        "Price change for Site A – Serviced (£)", -15.0, 20.0, 0.0, 1.0
    )
    serviced_available = st.toggle("Site A – Serviced available", value=True)
    lambda_param = st.slider(
        "Within-site nesting parameter", 0.20, 1.00, 0.55, 0.05,
        help="Lower values represent stronger dependence between products at the same site.",
    )

alternatives = pd.DataFrame(
    [
        {"alternative": "Site A – Hardstanding", "site_id": "Site A", "price": 34.0, "awning": 1, "availability": 0.55, "serviced": 0},
        {"alternative": "Site A – Serviced", "site_id": "Site A", "price": 45.0 + price_change, "awning": 1, "availability": 0.42, "serviced": 1},
        {"alternative": "Site B – Hardstanding", "site_id": "Site B", "price": 31.0, "awning": 0, "availability": 0.68, "serviced": 0},
        {"alternative": "Site B – Serviced", "site_id": "Site B", "price": 42.0, "awning": 1, "availability": 0.60, "serviced": 1},
    ]
)

if not serviced_available:
    alternatives = alternatives[alternatives["alternative"] != "Site A – Serviced"].copy()

# Illustrative coefficients, intentionally distinct from the empirical estimates.
alternatives["choice_id"] = 1
alternatives["utility"] = (
    -0.09 * (alternatives["price"] / 10)
    + 0.70 * alternatives["awning"]
    - 0.35 * alternatives["availability"]
    + 0.25 * alternatives["serviced"]
)
alternatives["MNL"] = mnl_probabilities(alternatives)
alternatives["Nested Logit"] = nested_logit_probabilities(
    alternatives, lambda_param=lambda_param
)

st.subheader("Predicted allocation of demand")
chart_data = alternatives.set_index("alternative")[["MNL", "Nested Logit"]]
plot_data = chart_data.reset_index().melt(
    id_vars="alternative",
    var_name="Model",
    value_name="Choice probability",
)
chart = (
    alt.Chart(plot_data)
    .mark_bar()
    .encode(
        x=alt.X(
            "alternative:N",
            title=None,
            sort=alternatives["alternative"].tolist(),
            axis=alt.Axis(labelAngle=-20),
        ),
        xOffset=alt.XOffset("Model:N"),
        y=alt.Y(
            "Choice probability:Q",
            axis=alt.Axis(format="%"),
            scale=alt.Scale(domain=[0, 0.55]),
        ),
        color=alt.Color(
            "Model:N",
            scale=alt.Scale(
                domain=["MNL", "Nested Logit"],
                range=["#2563EB", "#0F766E"],
            ),
        ),
        tooltip=[
            alt.Tooltip("alternative:N", title="Alternative"),
            alt.Tooltip("Model:N"),
            alt.Tooltip("Choice probability:Q", format=".1%"),
        ],
    )
    .properties(height=360)
)
st.altair_chart(chart, use_container_width=True)

display = alternatives[
    ["alternative", "site_id", "price", "awning", "availability", "MNL", "Nested Logit"]
].copy()
display["MNL"] = display["MNL"].map(lambda value: f"{value:.1%}")
display["Nested Logit"] = display["Nested Logit"].map(lambda value: f"{value:.1%}")
st.dataframe(display, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.markdown(
        """
        **How to use the demo**

        - Change the price of one product.
        - Remove that product from the available set.
        - Compare how MNL and Nested Logit redistribute probability.
        """
    )
with right:
    st.markdown(
        """
        **Important interpretation**

        This is an educational scenario using synthetic alternatives and
        illustrative coefficients. It is not a pricing recommendation and does
        not estimate a causal price response.
        """
    )

