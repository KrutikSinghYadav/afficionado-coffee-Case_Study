# ☕ Afficionado Coffee Roasters — Sales & Operational Analytics Case Study

A transaction-level data analysis of a three-location specialty coffee retail chain (Astoria, Hell's Kitchen, and Lower Manhattan), built to uncover demand patterns, staffing inefficiencies, and menu-mix opportunities — delivered as an interactive Streamlit dashboard, a formal research paper, and an executive summary.

---

## 📌 Project Overview

Afficionado Coffee Roasters operates three retail locations across New York City. This project analyzes **149,116 transaction line items** from January–June 2025 to answer core operational questions:

- When do stores experience peak customer demand, and is staffing aligned with it?
- How does purchase behavior differ between weekdays and weekends?
- Which product categories drive revenue, and where are the cross-selling opportunities?
- Are all three locations equally efficient, or should operating hours/staffing be adjusted per store?

The result is a full data analytics deliverable package — from raw transactions to boardroom-ready recommendations.

---

## 🔑 Key Findings

| Store | Revenue | Orders | Avg. Order Value |
|---|---:|---:|---:|
| Hell's Kitchen | $236,511.17 | 50,735 | $4.66 |
| Astoria | $232,243.91 | 50,599 | $4.59 |
| Lower Manhattan | $230,057.25 | 47,782 | $4.81 |

- **Total revenue:** $698,812.33 across 149,116 items
- **Universal peak hour:** 10:00 AM across all three stores (Hell's Kitchen hits 6,957 transactions in that hour alone)
- **Afternoon lull:** Demand drops ~60% after 2:00 PM network-wide
- **Commuter effect:** Lower Manhattan sees an earlier rush starting at 7:00 AM, unlike the more gradual build-up in Astoria
- **Product mix:** Coffee ($269,952) and Tea ($196,406) dominate volume; Coffee Beans have the highest average unit price ($21.92) despite low volume
- **Weekday vs. weekend:** Weekdays skew toward fast, single-item commuter purchases; weekends bring larger group orders and higher bakery/tea/bean sales

Full detail lives in the [Research Paper](Afficionado%20Coffee/Research_Paper.md), [Executive Summary](Afficionado%20Coffee/Executive_Summary.md), and the formatted [EDA Report (.docx)](Afficionado_Coffee_EDA_Report%20(1)%20(1).docx).

---

## 📊 Interactive Dashboard

The Streamlit app (`app.py`) presents the analysis across four tabs:

1. **Store Summary** — revenue, order volume, and AOV comparison across locations
2. **Hourly Demand** — hour-by-hour transaction heatmaps and peak traffic windows
3. **Shift Operations** — performance breakdown by Morning / Afternoon / Evening shifts
4. **Product & Menu Mix** — category and product-level revenue contribution

Built with a custom espresso-and-gold themed UI on top of Plotly visualizations.

---

## 🗂️ Repository Structure

```
afficionado-coffee-Case_Study/
│
├── Afficionado Coffee/
│   ├── app.py                              # Streamlit dashboard application
│   ├── afficionadocoffee - Transactions.csv # Raw transaction-level dataset (149,116 rows)
│   ├── Research_Paper.md                   # Full academic-style research paper
│   └── Executive_Summary.md                # Condensed stakeholder-facing brief
│
├── Afficionado_Coffee_EDA_Report (1) (1).docx  # Formatted EDA report (Word)
├── requirements.txt                        # Python dependencies
└── README.md
```

---

## 🧮 Dataset

The raw dataset (`afficionadocoffee - Transactions.csv`) contains the following fields:

| Column | Description |
|---|---|
| `transaction_id` | Unique ID per transaction line |
| `year` | Transaction year (2025) |
| `transaction_time` | Time of purchase (HH:MM:SS) |
| `Day_Shifts` | Pre-labeled shift window (Morning / Afternoon / Evening) |
| `transaction_qty` | Quantity purchased |
| `store_id`, `store_location` | Store identifier and location |
| `product_id`, `product_category`, `product_type`, `product_detail` | Product hierarchy |
| `unit_price` | Price per unit |
| `Revenue_generated` | Total revenue for the line item |

No external data joins were used — all insights are derived strictly from this transactional schema.

---

## 🛠️ Tech Stack

- **Python** — data processing and app logic
- **Pandas** — data cleaning, aggregation, and time-based feature extraction
- **Plotly** — interactive charts (bar, heatmap, line, treemap)
- **Streamlit** — dashboard front-end and deployment
- **Excel / openpyxl** — supplementary pivot analysis
- **Microsoft Word** — formal EDA report deliverable

---

## 🚀 Running the Dashboard Locally

```bash
# Clone the repository
git clone https://github.com/KrutikSinghYadav/afficionado-coffee-Case_Study.git
cd "afficionado-coffee-Case_Study/Afficionado Coffee"

# Install dependencies
pip install -r ../requirements.txt

# Run the app
streamlit run app.py
```

The app expects `afficionadocoffee - Transactions.csv` to be in the same folder as `app.py` (this is already the case in this repo).

---

## 📈 Strategic Recommendations (Summary)

1. **Re-align staffing** — Triple-coverage from 8:00–11:30 AM to handle the peak rush; scale down to single-staff coverage after 3:00 PM.
2. **Shift commuter start times** — Earlier barista arrivals in Lower Manhattan (6:45 AM) to capture the 7:00 AM rush.
3. **Cross-sell bakery items** during the morning rush to increase basket size.
4. **Promote tea offerings** between 1:00–4:00 PM to offset the afternoon lull.
5. **Adjust store hours** — Consider trimming Lower Manhattan's evening/weekend hours and reinvesting savings into Astoria's high-performing weekend leisure traffic.

---

## 👤 Author

**Krutik Singh Yadav**
Final-year Computer Engineering student, data analytics & data engineering enthusiast.

---

*This project was built as a self-directed portfolio case study to demonstrate end-to-end analytics workflow: data cleaning, exploratory analysis, dashboard development, and business-facing reporting.*
