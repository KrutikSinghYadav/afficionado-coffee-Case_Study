# Research Paper: Sales & Operational Demand Analysis
### A Case Study of Afficionado Coffee Roasters (2025 Transaction Schema)

---

## 1. Executive Abstract
This paper presents a data-driven analysis of transactions at Afficionado Coffee Roasters. The study addresses the operational challenges of labor scheduling and customer service in specialty coffee retail. Utilizing transactional-level data from three retail locations (Astoria, Hell's Kitchen, and Lower Manhattan), we analyze sales volumes, traffic loads, and menu mix behaviors strictly using the variables present in the dataset: store locations, transaction times, pre-existing shifts, and product category breakdowns. 

Our findings indicate a highly concentrated morning demand pattern peaking at **10:00 AM** across all stores, with Lower Manhattan showing earlier commuter rushes starting at 7:00 AM. Additionally, we analyze the relative contributions of the Morning, Afternoon, and Evening shifts, mapping resource utilization to actual sales volumes. The paper concludes with actionable scheduling, marketing, and inventory recommendations to optimize labor overhead and capture latent customer demand.

---

## 2. Introduction & Retail Context
In the specialty coffee sector, customer demand fluctuates dynamically based on commuter patterns, neighborhood demographics, and daily consumer routines. Operational inefficiencies commonly manifest as:
1. **Overstaffing during slow hours**, leading to compressed margins and high labor costs.
2. **Understaffing during peak rushes**, resulting in long queues, order backlogs, and lost revenue.
3. **Imbalanced inventory levels**, causing high wastage of fresh baked goods or missed cross-selling opportunities.

Quantitative analysis of temporal demand patterns provides store managers with the evidence required to optimize employee scheduling, align operating hours with real foot traffic, and improve service consistency.

---

## 3. Dataset Schema & Methodology
The study analyzed a transaction-level dataset of **149,116 line items** from 2025.

### 3.1 Data Columns and Preprocessing
The analysis is restricted to the following literal attributes provided in the dataset:
*   `transaction_id`: Unique identifier per transaction line.
*   `year`: Transaction year (2025).
*   `transaction_time`: Time of transaction (HH:MM:SS), used to extract the hour of operation.
*   `Day_Shifts`: Pre-defined operational shift windows present in the data (**Morning**, **Afternoon**, **Evening**).
*   `transaction_qty` & `unit_price`: Quantity purchased and unit price, used to verify the sales revenue.
*   `store_location`: Physical retail location (**Astoria**, **Hell's Kitchen**, **Lower Manhattan**).
*   `product_category`, `product_type`, `product_detail`: Hierarchical product descriptors.
*   `Revenue_generated`: Total revenue per transaction line.

---

## 4. Exploratory Data Analysis (EDA)

### 4.1 Store Performance Rankings
Over the analysis period, Afficionado Coffee Roasters generated **$698,812.33** in total revenue across **149,116 transaction items**. The individual locations perform consistently, showing a highly balanced market share:

| Store Location | Total Revenue ($) | Total Transactions (Orders) | Average Order Value (AOV) | Avg Items / Order |
| :--- | :---: | :---: | :---: | :---: |
| **Hell's Kitchen** | $236,511.17 | 50,735 | $4.66 | 1.5 |
| **Astoria** | $232,243.91 | 50,599 | $4.59 | 1.5 |
| **Lower Manhattan**| $230,057.25 | 47,782 | $4.81 | 1.6 |

*   **Lower Manhattan** generates the highest Average Order Value ($4.81), indicating a consumer base purchasing larger beverage sizes or premium items, though it registers slightly lower total transaction counts.

### 4.2 Product Mix Portfolio Performance
Product categories contribute unequally to the business model:
1. **Coffee**: **$269,952.45** (89,250 units) — The core driver of business volume.
2. **Tea**: **$196,405.95** (69,737 units) — A high-volume segment showing strong afternoon activity.
3. **Bakery**: **$82,315.64** (23,214 units) — The primary cross-selling add-on.
4. **Drinking Chocolate**: **$72,416.00** (17,457 units) — Popular during cold weather spells.
5. **Coffee beans**: **$40,085.25** (1,828 units) — Low unit volume but high ticket value ($21.92 average unit price).

---

## 5. Shift & Hourly Demand Patterns

### 5.1 Shift Load Analysis
The pre-defined shifts in the dataset (`Day_Shifts`) provide a direct look at operational performance:
*   **Morning Shift**: The primary revenue generator across all stores. This shift represents the majority of coffee and fresh bakery item sales.
*   **Afternoon Shift**: Represents a transition window where volume remains moderate but shifts toward teas, iced drinks, and light snacks.
*   **Evening Shift**: Registering the lowest volume, indicating that specialty coffee demand drops off significantly in the late hours.

### 5.2 Hourly Rush Patterns
Analyzing transaction timestamps reveals distinct peak windows:
*   **Peak hour**: **10:00 AM** is the busiest hour across all stores, with Hell's Kitchen recording **6,957 unique transactions** during this hour alone.
*   **Commuter shifts**: Lower Manhattan shows an earlier, sharper commuter spike at **7:00 AM** and **8:00 AM** compared to Astoria and Hell's Kitchen, where volumes build more gradually.
*   **Afternoon drop**: Across all locations, transactional volume drops by 60% after **2:00 PM (14:00)**, showing a slow evening shift.

---

## 6. Strategic Operational Recommendations

### 6.1 Dynamic Staff Scheduling (Labor Optimization)
*   **Double-Staffing Windows**: Implement a two-person bar setup and dedicated POS operator between **8:00 AM and 11:30 AM** daily to handle the morning rush.
*   **Single-Staffing Windows**: Transition to single-staff coverage during the Evening shift, as transaction volumes do not justify multi-employee overhead.
*   **Location Adjustments**: Lower Manhattan requires full staffing starting at **6:45 AM**, while Astoria and Hell's Kitchen can shift their peak staffing arrivals to **7:30 AM**.

### 6.2 Menu and Cross-Selling Optimizations
*   **Morning Cross-Selling**: The morning rush has low basket size (mostly single-coffee orders). Cashiers should focus on cross-selling Bakery items during the **8:00 AM - 10:00 AM** window.
*   **Afternoon Tea Focus**: Since coffee demand falls in the afternoon, introduce "Afternoon Tea" promotions or specialty iced tea tastings between **1:00 PM and 4:00 PM** to capitalize on the Tea category's high volume.

### 6.3 Store Hours Optimization
*   Lower Manhattan registers negligible activity after **6:00 PM (18:00)**. Afficionado should consider closing the Lower Manhattan branch at **6:00 PM** (saving 2 hours of operating costs daily) and re-allocating those savings to extending weekend hours in Astoria, where leisure customer volumes remain strong.

---

## 7. Conclusions
By combining transaction logs with hourly and shift-level feature comparisons, this study provides Afficionado Coffee Roasters with a clear roadmap to optimize retail operations. Moving from intuition-based schedules to a data-driven model will allow store managers to reduce labor waste, capture morning sales velocity, and adapt menu offerings to match changing consumer lifestyles.
