
import streamlit as st
import pandas as pd
from google import genai

# Give the app a title and description.
st.set_page_config(page_title="Café Operations", page_icon="☕")

st.title("☕ Nordic Café Intelligence")
st.sidebar.write("Business Analytics Dashboard")
st.sidebar.divider()
st.sidebar.info("Built with Python, pandas and Streamlit.")
# Example sales data (not real customer information).
sales = {
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"],
    "coffee": [65, 72, 69, 80, 110, 135, 95],
    "tea": [22, 19, 25, 26, 32, 38, 30],
    "sandwiches": [35, 41, 39, 46, 65, 78, 49],
    "pastries": [40, 43, 42, 51, 76, 94, 60]
}

df = pd.DataFrame(sales)

# Allow users to upload their own sales data.
st.sidebar.subheader("Upload sales data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    required_columns = [
        "day", "coffee", "tea", "sandwiches", "pastries"
    ]

    if not all(col in uploaded_df.columns for col in required_columns):
        st.error("CSV must contain: day, coffee, tea, sandwiches, pastries")
        st.stop()

    if uploaded_df.empty:
        st.error("The uploaded CSV is empty.")
        st.stop()

    for product in required_columns[1:]:
        uploaded_df[product] = pd.to_numeric(
            uploaded_df[product], errors="coerce"
        )

    if uploaded_df[required_columns].isna().any().any():
        st.error("Some required values are missing or invalid.")
        st.stop()

    if (uploaded_df[required_columns[1:]] < 0).any().any():
        st.error("Sales quantities cannot be negative.")
        st.stop()

    df = uploaded_df
    st.sidebar.success("File uploaded successfully!")

# Arrange days in the correct weekly order.
day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

# Check whether all day names are recognized.
if not df["day"].isin(day_order).all():
    st.error("Please use valid weekday names.")
    st.stop()

df["day"] = pd.Categorical(
    df["day"],
    categories=day_order,
    ordered=True
)

df = df.sort_values("day").reset_index(drop=True)


# Allow café managers to customize product prices.
st.sidebar.divider()
st.sidebar.subheader("Product Prices (USD)")

prices = {
    "coffee": st.sidebar.number_input(
        "Coffee price ($)", min_value=0.0,
        value=4.50, step=0.50
    ),
    "tea": st.sidebar.number_input(
        "Tea price ($)", min_value=0.0,
        value=3.50, step=0.50
    ),
    "sandwiches": st.sidebar.number_input(
        "Sandwich price ($)", min_value=0.0,
        value=8.50, step=0.50
    ),
    "pastries": st.sidebar.number_input(
        "Pastry price ($)", min_value=0.0,
        value=4.80, step=0.50
    )
}


# Calculate total sales revenue for each day.
df["revenue"] = (
    df["coffee"] * prices["coffee"]
    + df["tea"] * prices["tea"]
    + df["sandwiches"] * prices["sandwiches"]
    + df["pastries"] * prices["pastries"]
)

# Allow the user to select a day.
selected_day = st.selectbox(
    "Choose a day",
    df["day"].tolist()
)

selected_data = df[df["day"] == selected_day].iloc[0]

# Display key information.
st.subheader(f"Results for {selected_day}")


total_items = sum(
    int(selected_data[product]) for product in prices
)

# Display business performance metrics side by side.
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=" Daily Revenue",
        value=f"${selected_data['revenue']:,.2f}"
    )

with col2:
    st.metric(
        label=" Items Sold",
        value=total_items
    )


# Chart showing revenue over the week.
st.subheader("Weekly revenue")
st.bar_chart(df.set_index("day")["revenue"])

# Display the sales data.
st.subheader("Full sales report")
st.dataframe(df, hide_index=True)

# Create simple business recommendations.
best_day = df.loc[df["revenue"].idxmax(), "day"]

st.subheader("Business insights")
st.success(f"Highest revenue day: {best_day}")

if selected_data["revenue"] > df["revenue"].mean():
    st.write("Revenue is above the weekly daily average.")
else:
    st.write("Revenue is at or below the weekly daily average.")

st.caption("Portfolio demo using fictional sales data.")

# Weekly business performance summary
st.divider()
st.header(" Weekly Business Summary")

weekly_revenue = df["revenue"].sum()
average_revenue = df["revenue"].mean()
best_day = df.loc[df["revenue"].idxmax(), "day"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"${weekly_revenue:,.2f}"
    )

with col2:
    st.metric(
        "Average Daily Revenue",
        f"${average_revenue:,.2f}"
    )

with col3:
    st.metric(
        "Best Sales Day",
        best_day
    )



# PRODUCT PERFORMANCE ANALYTICS

st.divider()
st.header(" Product Performance Analytics")

# Calculate units sold and revenue for each product.
product_data = []

for product, price in prices.items():
    units_sold = df[product].sum()
    product_revenue = units_sold * price

    product_data.append({
        "Product": product.capitalize(),
        "Units Sold": units_sold,
        "Revenue": product_revenue
    })

product_df = pd.DataFrame(product_data)

# Identify best-selling and highest-revenue products.
best_selling = product_df.loc[
    product_df["Units Sold"].idxmax(), "Product"
]

top_revenue_product = product_df.loc[
    product_df["Revenue"].idxmax(), "Product"
]

# SMART BUSINESS RECOMMENDATIONS

st.divider()
st.header(" Smart Business Recommendations")

# Identify the strongest sales day.
highest_day = df.loc[df["revenue"].idxmax(), "day"]

# Identify the weakest sales day.
lowest_day = df.loc[df["revenue"].idxmin(), "day"]

# Identify the top revenue-generating product.
top_product = product_df.loc[
    product_df["Revenue"].idxmax(), "Product"
]

# DOWNLOADABLE BUSINESS REPORT

st.divider()
st.header(" Download Business Report")

st.write(
    "Download your sales data and calculated revenue "
    "as a CSV file for further analysis."
)


# AI-POWERED MANAGEMENT ASSISTANT

st.divider()
st.header("AI Management Assistant")

st.write(
    "Generate an AI-powered management report "
    "based on your café's sales performance."
)

st.caption(
    "AI reports are generated using Google Gemini. "
    "Always verify recommendations before acting on them."
)

ai_enabled = bool(st.secrets.get("GEMINI_API_KEY", ""))

if st.button("Generate AI Management Report", disabled=not ai_enabled):


    with st.spinner("Gemini is analyzing your sales data..."):

        try:
            # Retrieve the API key from Streamlit secrets.
            api_key = st.secrets["GEMINI_API_KEY"]

            # Connect to Google Gemini.
            client = genai.Client(api_key=api_key)

            # Create a concise summary of the business data.
            sales_summary = df[
                ["day", "coffee", "tea",
                 "sandwiches", "pastries", "revenue"]
            ].to_csv(index=False)

            product_summary = product_df.to_csv(index=False)

            # Tell Gemini what kind of report to produce.
            prompt = f"""
You are a professional café business analyst.

Analyze the following fictional café sales data.

Daily sales:
{sales_summary}

Product performance:
{product_summary}

Current product prices (USD):
{prices}

Total revenue: ${weekly_revenue:,.2f}
Average daily revenue: ${average_revenue:,.2f}

Write a professional management report with:

1. Executive Summary
2. Sales Performance Analysis
3. Product Performance Analysis
4. Three Actionable Business Recommendations
5. Potential Risks or Limitations

Important rules:
- Use only the supplied data.
- Do not invent figures or business facts.
- All amounts are in USD.
- Do not confuse revenue with profit.
- Present recommendations as suggestions,
  not guaranteed outcomes.
- Use clear headings and concise explanations.
"""

            # Generate the report using Gemini.
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            if response.text:
                st.success("AI report generated successfully!")
                st.markdown(response.text)
            else:
                st.warning(
                    "Gemini did not return a text report. "
                    "Please try again."
                )

        except Exception as e:
            st.error(
                "The AI report could not be generated. "
                "Please check your API key, model access, "
                "and API usage limits."
            )
            st.caption(f"Technical details: {type(e).__name__}")


# Convert the sales report into CSV format.
csv_report = df.to_csv(index=False).encode("utf-8")

# Create a download button.
st.download_button(
    label=" Download Sales Report",
    data=csv_report,
    file_name="nordic_cafe_sales_report.csv",
    mime="text/csv"
)


# Calculate the contribution of the top product.
total_revenue = product_df["Revenue"].sum()

if total_revenue > 0:
    top_product_revenue = product_df["Revenue"].max()
    contribution = (top_product_revenue / total_revenue) * 100
else:
    contribution = 0

st.success(
    f" {highest_day} is your highest-revenue day. "
    "Review staffing and inventory to ensure sufficient capacity."
)

st.info(
    f" {lowest_day} is your lowest-revenue day. "
    "Investigate demand patterns before making scheduling changes."
)

st.info(
    f" {top_product} generates approximately "
    f"{contribution:.1f}% of total revenue."
)

st.caption(
    "Recommendations are rule-based and use the uploaded sales data."
)


# Display product performance.
col1, col2 = st.columns(2)

with col1:
    st.metric(" Best-Selling Product", best_selling)

with col2:
    st.metric(" Top Revenue Product", top_revenue_product)

# Show revenue by product.
st.subheader("Revenue by Product")

st.bar_chart(
    product_df.set_index("Product")["Revenue"]
)

# Show units sold by product.
st.subheader("Units Sold by Product")

st.bar_chart(
    product_df.set_index("Product")["Units Sold"]
)

# Show the complete product analysis.
st.subheader("Product Performance Report")

st.dataframe(
    product_df,
    hide_index=True
)
