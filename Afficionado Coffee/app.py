import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# PAGE CONFIGURATION
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Afficionado Coffee Roasters Analytics",
    layout="wide",
    page_icon="☕"
)

# ──────────────────────────────────────────────
# CUSTOM CSS — Espresso & Gold Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');

html, body, [class*="st-"] {
    font-family: 'Outfit', sans-serif !important;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif !important;
}

/* ── Main background ── */
.stApp { background-color: #1A120B; }

/* ── Title banner ── */
.title-container {
    background: linear-gradient(135deg, #271E15 0%, #1A120B 100%);
    padding: 32px 36px;
    border-radius: 18px;
    border: 1px solid #3A2E2B;
    margin-bottom: 28px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
}

/* ── KPI cards ── */
.kpi-card {
    background: linear-gradient(145deg, #2B1F14, #1E1610);
    border: 1px solid #3A2E2B;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 32px rgba(0,0,0,0.45);
    border-color: #D4AF37;
}
.kpi-icon  { font-size: 28px; margin-bottom: 8px; }
.kpi-label { font-size: 11px; font-weight: 600; color: #C5A880;
             text-transform: uppercase; letter-spacing: 1.8px; margin-bottom: 6px; }
.kpi-value { font-size: 30px; font-weight: 700; color: #F5EBE6; line-height: 1.1; }
.kpi-sub   { font-size: 12px; color: #8D6E63; margin-top: 4px; }

/* ── Divider ── */
.section-divider { border-top: 1px solid #3A2E2B; margin: 28px 0; }

/* ── Insight box ── */
.insight-box {
    background: #271E15;
    border-left: 4px solid #D4AF37;
    border-radius: 0 10px 10px 0;
    padding: 18px 22px;
    margin: 12px 0;
    font-size: 14px;
    color: #F5EBE6;
    line-height: 1.7;
}
.insight-box b { color: #D4AF37; }

/* ── Footer ── */
.footer {
    background: #271E15;
    border: 1px solid #3A2E2B;
    border-radius: 12px;
    padding: 20px 28px;
    margin-top: 40px;
    text-align: center;
    font-size: 13px;
    color: #8D6E63;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0F0906 !important;
    border-right: 1px solid #271E15;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid #3A2E2B; }
.stTabs [data-baseweb="tab"] {
    background-color: #271E15; border: 1px solid #3A2E2B;
    border-radius: 8px 8px 0 0; padding: 12px 26px;
    color: #C5A880; font-weight: 600; transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover { color: #D4AF37; border-color: #D4AF37; }
.stTabs [aria-selected="true"] {
    background-color: #D4AF37 !important;
    color: #1A120B !important;
    border-color: #D4AF37 !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HELPER — KPI card
# ──────────────────────────────────────────────
def kpi_card(icon, label, value, sub=""):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA LOADING — strictly from literal columns
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    paths = [
        "afficionadocoffee - Transactions.csv",
        "Transactions.csv",
    ]
    df = None
    for p in paths:
        try:
            df = pd.read_csv(p)
            break
        except Exception:
            continue
    if df is None:
        raise FileNotFoundError("Dataset not found. Please place 'afficionadocoffee - Transactions.csv' in the app folder.")

    df.columns = [c.strip() for c in df.columns]
    df = df[(df['transaction_qty'] > 0) & (df['unit_price'] >= 0)].copy()

    # Revenue column (use existing if present)
    df['revenue'] = df['Revenue_generated'] if 'Revenue_generated' in df.columns \
                    else df['transaction_qty'] * df['unit_price']

    # Hour extracted from time string — NO date inference
    t = pd.to_datetime(df['transaction_time'].astype(str), format='%H:%M:%S', errors='coerce')
    df['hour'] = t.dt.hour

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ {e}")
    st.stop()

# ──────────────────────────────────────────────
# COLOUR SYSTEM
# ──────────────────────────────────────────────
C_GOLD   = '#D4AF37'
C_BROWN  = '#8D6E63'
C_SLATE  = '#4A6B82'
C_CREAM  = '#E0D4C3'
C_MUTED  = '#A1887F'

PALETTE  = [C_GOLD, C_BROWN, C_SLATE, C_CREAM, C_MUTED, '#C5A880']
SHIFT_PAL= {
    'Morning':   C_GOLD,
    'Afternoon': C_BROWN,
    'Evening':   C_SLATE,
    'Late hours': C_CREAM,
}
HEAT_SCALE = ['#1A120B', '#3E2723', '#8D6E63', '#D4AF37', '#F5EBE6']
SHIFT_ORDER= ['Morning', 'Afternoon', 'Evening', 'Late hours']

def style_fig(fig, height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Outfit, sans-serif',
        font_color='#F5EBE6',
        title_font_family='Playfair Display, serif',
        title_font_color=C_GOLD,
        title_font_size=18,
        xaxis=dict(gridcolor='#3A2E2B', zerolinecolor='#3A2E2B',
                   linecolor='#3A2E2B', tickfont=dict(size=11)),
        yaxis=dict(gridcolor='#3A2E2B', zerolinecolor='#3A2E2B',
                   linecolor='#3A2E2B', tickfont=dict(size=11)),
        legend=dict(bgcolor='rgba(39,30,21,0.85)', bordercolor='#3A2E2B',
                    borderwidth=1, font=dict(size=11)),
        margin=dict(t=55, b=35, l=35, r=20),
    )
    return fig

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div class="title-container">
  <h1 style="color:#D4AF37;margin:0;font-size:36px;">☕ Afficionado Coffee Roasters</h1>
  <h3 style="color:#C5A880;margin:6px 0 0;font-weight:400;font-size:17px;">
      Sales Trend &amp; Time-Based Performance Analytics Dashboard
  </h3>
  <p style="color:#A1887F;margin:10px 0 0;font-size:13px;line-height:1.6;max-width:820px;">
      An evidence-based operations tool for specialty coffee retail. Explore transaction volumes,
      peak hourly demand, shift-level staff alignment, and menu mix performance across
      <b style="color:#C5A880;">Astoria</b>, <b style="color:#C5A880;">Hell's Kitchen</b>,
      and <b style="color:#C5A880;">Lower Manhattan</b>.
  </p>
</div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR CONTROLS
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 6px'>
        <span style='font-size:48px;'>☕</span>
        <h2 style='margin:4px 0 2px;font-family:"Playfair Display",serif;color:#D4AF37;'>Afficionado</h2>
        <p style='font-size:10px;color:#C5A880;text-transform:uppercase;letter-spacing:2.5px;margin:0;'>
            Dashboard Controls</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    # Metric toggle
    st.markdown("#### 📈 Primary KPI")
    metric_choice = st.radio("Analyze by:", ("Revenue ($)", "Quantity (Items Sold)"), index=0)
    is_rev   = metric_choice == "Revenue ($)"
    m_col    = 'revenue' if is_rev else 'transaction_qty'
    m_label  = 'Revenue ($)' if is_rev else 'Items Sold'

    st.markdown("---")

    # Location filter
    st.markdown("#### 🏬 Store Location")
    stores   = sorted(df['store_location'].unique().tolist())
    store_sel= st.selectbox("Select location:", ["All Stores"] + stores)

    st.markdown("---")

    # Hour range slider
    st.markdown("#### 🕒 Operating Hours")
    h_min, h_max = int(df['hour'].min()), int(df['hour'].max())
    h_range = st.slider("Hour range:", h_min, h_max, (h_min, h_max), format="%d:00")

    st.markdown("---")

    # Shift filter
    st.markdown("#### 🌅 Shift Filter")
    avail_shifts = [s for s in SHIFT_ORDER if s in df['Day_Shifts'].unique()]
    shift_sel    = st.multiselect("Select shifts:", avail_shifts, default=avail_shifts)

    st.markdown("---")
    st.markdown("""<p style='font-size:11px;color:#5C4033;text-align:center;line-height:1.6;'>
        Data: 2025 transactions<br>Locations: Astoria · Hell's Kitchen · Lower Manhattan
    </p>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# APPLY FILTERS
# ──────────────────────────────────────────────
fdf = df.copy()
if store_sel != "All Stores":
    fdf = fdf[fdf['store_location'] == store_sel]
fdf = fdf[(fdf['hour'] >= h_range[0]) & (fdf['hour'] <= h_range[1])]
if shift_sel:
    fdf = fdf[fdf['Day_Shifts'].isin(shift_sel)]

if fdf.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust the controls in the sidebar.")
    st.stop()

# ──────────────────────────────────────────────
# GLOBAL KPI ROW
# ──────────────────────────────────────────────
total_val  = fdf[m_col].sum()
total_tx   = fdf['transaction_id'].nunique()
avg_ticket = total_val / total_tx if total_tx else 0
top_cat    = fdf.groupby('product_category')[m_col].sum().idxmax()
top_store  = fdf.groupby('store_location')[m_col].sum().idxmax()

v_total  = f"${total_val:,.2f}"  if is_rev else f"{total_val:,.0f}"
v_avg    = f"${avg_ticket:,.2f}" if is_rev else f"{avg_ticket:,.2f}"

k1, k2, k3, k4, k5 = st.columns(5)
with k1: kpi_card("💰", f"Total {m_label}", v_total)
with k2: kpi_card("🧾", "Total Orders",    f"{total_tx:,}", "Unique transactions")
with k3: kpi_card("☕", "Avg Ticket Size", v_avg, "Per order")
with k4: kpi_card("🏆", "Top Category",    top_cat)
with k5: kpi_card("🏬", "Top Location",    top_store)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Store Summary",
    "🕒  Hourly Demand",
    "🌅  Shift Operations",
    "📦  Product & Menu Mix",
])

# ══════════════════════════════════════════════
# TAB 1 — STORE PERFORMANCE SUMMARY
# ══════════════════════════════════════════════
with tab1:
    st.markdown("### 📊 Store Performance & Market Share")
    st.markdown("Side-by-side comparison of revenue, volume, and average order value across the three retail locations.")

    store_agg = fdf.groupby('store_location').agg(
        total_rev  = ('revenue',        'sum'),
        total_qty  = ('transaction_qty','sum'),
        total_tx   = ('transaction_id', 'nunique'),
    ).reset_index()
    store_agg['aov']     = store_agg['total_rev'] / store_agg['total_tx']
    store_agg['avg_qty'] = store_agg['total_qty'] / store_agg['total_tx']
    y_col = 'total_rev' if is_rev else 'total_qty'

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            store_agg, x='store_location', y=y_col,
            color='store_location', color_discrete_sequence=PALETTE,
            title=f"Total {m_label} by Location",
            labels={'store_location': 'Store', y_col: m_label},
            text_auto='.3s'
        )
        fig.update_traces(marker_line_width=0, textfont_size=12)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(
            store_agg, values=y_col, names='store_location',
            hole=0.45, color_discrete_sequence=PALETTE,
            title=f"Market Share — {m_label}"
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label',
                           pull=[0.04]*len(store_agg))
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # AOV comparison
    st.markdown("#### ⚖️ Average Order Value (AOV) per Location")
    fig3 = px.bar(
        store_agg, x='store_location', y='aov',
        color='store_location', color_discrete_sequence=PALETTE,
        title="Average Order Value (AOV) — Revenue per Unique Transaction",
        labels={'aov': 'AOV ($)', 'store_location': 'Store'},
        text_auto='.2f'
    )
    fig3.update_traces(marker_line_width=0)
    style_fig(fig3, height=350)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Summary table
    st.markdown("#### 📋 Operational Metrics Summary Table")
    tbl = store_agg.copy()
    tbl['Total Revenue']           = tbl['total_rev'].map("${:,.2f}".format)
    tbl['Items Sold']              = tbl['total_qty'].map("{:,.0f}".format)
    tbl['Total Orders']            = tbl['total_tx'].map("{:,.0f}".format)
    tbl['Avg Order Value (AOV)']   = tbl['aov'].map("${:,.2f}".format)
    tbl['Avg Items / Order']       = tbl['avg_qty'].map("{:,.2f}".format)
    tbl = tbl.rename(columns={'store_location': 'Store Location'})
    st.dataframe(
        tbl[['Store Location','Total Revenue','Items Sold','Total Orders',
             'Avg Order Value (AOV)','Avg Items / Order']],
        use_container_width=True, hide_index=True
    )

    insight("💡 <b>Lower Manhattan</b> achieves the highest Average Order Value, suggesting a corporate "
            "or premium consumer base, while <b>Hell's Kitchen</b> leads in total transaction count "
            "and overall revenue volume.")

# ══════════════════════════════════════════════
# TAB 2 — HOURLY DEMAND PROFILE
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### 🕒 Hourly Customer Demand Profile")
    st.markdown("Pinpoint exactly when customers arrive and how sales are distributed across the operating day.")

    hourly = fdf.groupby(['hour', 'store_location']).agg(
        val    = (m_col, 'sum'),
        orders = ('transaction_id', 'nunique'),
    ).reset_index()

    # Revenue / Qty curve
    fig_h1 = px.line(
        hourly, x='hour', y='val', color='store_location',
        title=f"Hourly {m_label} Curve per Location",
        markers=True, color_discrete_sequence=[C_GOLD, C_BROWN, C_SLATE],
        labels={'val': m_label, 'hour': 'Hour of Day', 'store_location': 'Location'}
    )
    fig_h1.update_traces(line_width=2.5)
    fig_h1.update_layout(xaxis=dict(tickmode='linear', dtick=1), hovermode='x unified')
    style_fig(fig_h1, height=400)
    st.plotly_chart(fig_h1, use_container_width=True)

    # Foot traffic orders curve
    fig_h2 = px.line(
        hourly, x='hour', y='orders', color='store_location',
        title="Hourly Foot Traffic — Unique Orders per Hour",
        markers=True, color_discrete_sequence=[C_GOLD, C_BROWN, C_SLATE],
        labels={'orders': 'Unique Orders', 'hour': 'Hour of Day', 'store_location': 'Location'}
    )
    fig_h2.update_traces(line_width=2.5)
    fig_h2.update_layout(xaxis=dict(tickmode='linear', dtick=1), hovermode='x unified')
    style_fig(fig_h2, height=400)
    st.plotly_chart(fig_h2, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Heatmap: Hour vs Store
    st.markdown("#### 🔥 Heatmap — Transaction Volume by Hour × Store")
    heat_data = fdf.groupby(['store_location', 'hour'])['transaction_id'].nunique().reset_index()
    heat_pivot = heat_data.pivot(index='store_location', columns='hour', values='transaction_id').fillna(0)

    fig_heat = px.imshow(
        heat_pivot,
        color_continuous_scale=HEAT_SCALE,
        labels=dict(x="Hour of Day", y="Store Location", color="Orders"),
        title="Transaction Density Heatmap (Store × Hour)",
        aspect='auto'
    )
    # ── FIXED: replaced deprecated titlefont with title=dict(font=...) ──
    fig_heat.update_layout(coloraxis_colorbar=dict(
        title=dict(text="Orders", font=dict(color='#F5EBE6')),
        tickfont=dict(color='#F5EBE6')
    ))
    style_fig(fig_heat, height=300)
    st.plotly_chart(fig_heat, use_container_width=True)

    peak_hour = fdf.groupby('hour')['transaction_id'].nunique().idxmax()
    insight(f"💡 Across all locations, <b>{peak_hour}:00</b> is the single busiest operational hour. "
            "Staffing should be at maximum capacity from <b>8:00 – 11:00</b> to handle the morning "
            "rush efficiently and minimise queue times.")

# ══════════════════════════════════════════════
# TAB 3 — SHIFT OPERATIONS
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### 🌅 Shift Operations & Labour Alignment")
    st.markdown("Analyse business volume across the three operational shifts defined in the dataset.")

    shift_agg = fdf.groupby(['store_location', 'Day_Shifts']).agg(
        val    = (m_col, 'sum'),
        orders = ('transaction_id', 'nunique'),
    ).reset_index()
    shift_agg['Day_Shifts'] = pd.Categorical(
        shift_agg['Day_Shifts'], categories=SHIFT_ORDER, ordered=True
    )
    shift_agg = shift_agg.sort_values('Day_Shifts')
    shift_colors = [SHIFT_PAL.get(s, C_CREAM) for s in shift_agg['Day_Shifts'].cat.categories
                    if s in shift_agg['Day_Shifts'].values]

    c3a, c3b = st.columns(2)
    with c3a:
        fig_sg = px.bar(
            shift_agg, x='store_location', y='val',
            color='Day_Shifts', barmode='group',
            title=f"{m_label} by Store & Shift (Grouped)",
            labels={'val': m_label, 'store_location': 'Store', 'Day_Shifts': 'Shift'},
            color_discrete_sequence=[C_GOLD, C_BROWN, C_SLATE, C_CREAM],
            category_orders={'Day_Shifts': SHIFT_ORDER}
        )
        style_fig(fig_sg)
        st.plotly_chart(fig_sg, use_container_width=True)

    with c3b:
        fig_ss = px.bar(
            shift_agg, x='store_location', y='val',
            color='Day_Shifts', barmode='relative',
            title=f"Shift Share of {m_label} per Location (Stacked %)",
            labels={'val': m_label, 'store_location': 'Store', 'Day_Shifts': 'Shift'},
            color_discrete_sequence=[C_GOLD, C_BROWN, C_SLATE, C_CREAM],
            category_orders={'Day_Shifts': SHIFT_ORDER}
        )
        style_fig(fig_ss)
        st.plotly_chart(fig_ss, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Shift foot traffic
    st.markdown("#### 🧾 Order Count (Foot Traffic) by Shift")
    fig_st = px.bar(
        shift_agg, x='store_location', y='orders',
        color='Day_Shifts', barmode='group',
        title="Unique Orders per Shift & Location",
        labels={'orders': 'Unique Orders', 'store_location': 'Store', 'Day_Shifts': 'Shift'},
        color_discrete_sequence=[C_GOLD, C_BROWN, C_SLATE, C_CREAM],
        category_orders={'Day_Shifts': SHIFT_ORDER}
    )
    style_fig(fig_st, height=380)
    st.plotly_chart(fig_st, use_container_width=True)

    # Shift-level summary table
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 📋 Shift-Level Summary Table")
    shift_tbl = shift_agg.copy()
    shift_tbl['avg_order'] = shift_agg['val'] / shift_agg['orders'].replace(0, 1)
    shift_tbl[m_label]         = shift_tbl['val'].map(("${:,.2f}" if is_rev else "{:,.0f}").format)
    shift_tbl['Unique Orders']  = shift_tbl['orders'].map("{:,.0f}".format)
    shift_tbl['Avg per Order']  = shift_tbl['avg_order'].map("${:,.2f}".format)
    shift_tbl = shift_tbl.rename(columns={
        'store_location': 'Store Location',
        'Day_Shifts':     'Shift Window'
    })
    st.dataframe(
        shift_tbl[['Store Location', 'Shift Window', m_label, 'Unique Orders', 'Avg per Order']],
        use_container_width=True, hide_index=True
    )

    best_shift = fdf.groupby('Day_Shifts')[m_col].sum().idxmax()
    insight(f"💡 The <b>{best_shift}</b> shift is the highest-revenue window. "
            "Scheduling two baristas plus a dedicated POS operator during this shift "
            "would directly maximise throughput and minimise service drop-offs.")

# ══════════════════════════════════════════════
# TAB 4 — PRODUCT & MENU MIX
# ══════════════════════════════════════════════
with tab4:
    st.markdown("### 📦 Product Categories & Menu Mix Analysis")
    st.markdown("Deep-dive into which categories and individual menu items drive the most volume.")

    # Category summary
    cat_agg = fdf.groupby('product_category').agg(
        revenue = ('revenue',        'sum'),
        qty     = ('transaction_qty','sum'),
        orders  = ('transaction_id', 'nunique'),
    ).reset_index().sort_values('revenue' if is_rev else 'qty', ascending=True)

    fig_cat = px.bar(
        cat_agg, x='revenue' if is_rev else 'qty', y='product_category',
        orientation='h', color='revenue' if is_rev else 'qty',
        color_continuous_scale=HEAT_SCALE, text_auto='.3s',
        title=f"Product Category Contribution — {m_label}",
        labels={'revenue': 'Revenue ($)', 'qty': 'Items Sold', 'product_category': ''}
    )
    fig_cat.update_layout(coloraxis_showscale=False, yaxis_title="")
    fig_cat.update_traces(textfont_size=11)
    style_fig(fig_cat, height=380)
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    c4a, c4b = st.columns(2)
    with c4a:
        # Category donut
        fig_donut = px.pie(
            cat_agg, values='revenue' if is_rev else 'qty',
            names='product_category', hole=0.42,
            color_discrete_sequence=PALETTE,
            title=f"Portfolio Share — {m_label}"
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', pull=[0.03]*len(cat_agg))
        style_fig(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True)

    with c4b:
        # Product type breakdown by category
        type_agg = fdf.groupby(['product_category', 'product_type'])[m_col].sum().reset_index()
        type_agg = type_agg.sort_values(m_col, ascending=False).head(12)
        fig_type = px.bar(
            type_agg, x=m_col, y='product_type',
            color='product_category', orientation='h',
            color_discrete_sequence=PALETTE, text_auto='.2s',
            title=f"Top 12 Product Types — {m_label}",
            labels={m_col: m_label, 'product_type': 'Product Type', 'product_category': 'Category'}
        )
        fig_type.update_layout(yaxis=dict(autorange='reversed'), yaxis_title="")
        style_fig(fig_type)
        st.plotly_chart(fig_type, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Top 10 individual items
    st.markdown("#### 🏆 Top 10 Best-Selling Menu Items")
    item_agg = fdf.groupby(['product_detail', 'product_category'])[m_col].sum().reset_index()
    item_agg = item_agg.sort_values(m_col, ascending=False).head(10)

    fig_items = px.bar(
        item_agg, x=m_col, y='product_detail',
        color='product_category', orientation='h',
        color_discrete_sequence=PALETTE, text_auto='.3s',
        title=f"Top 10 Menu Items — {m_label}",
        labels={m_col: m_label, 'product_detail': '', 'product_category': 'Category'}
    )
    fig_items.update_layout(yaxis=dict(autorange='reversed'), yaxis_title="")
    style_fig(fig_items, height=420)
    st.plotly_chart(fig_items, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Revenue vs Quantity scatter by product type
    st.markdown("#### 📐 Revenue vs. Quantity — Product Type Matrix")
    scatter_agg = fdf.groupby(['product_type', 'product_category']).agg(
        rev = ('revenue',        'sum'),
        qty = ('transaction_qty','sum'),
        txn = ('transaction_id', 'nunique'),
    ).reset_index()

    fig_scatter = px.scatter(
        scatter_agg, x='qty', y='rev',
        color='product_category', size='txn',
        hover_name='product_type',
        color_discrete_sequence=PALETTE,
        title="Revenue vs. Quantity Sold — Bubble = Order Count",
        labels={'qty': 'Items Sold', 'rev': 'Total Revenue ($)', 'product_category': 'Category'}
    )
    fig_scatter.update_traces(marker=dict(opacity=0.85, line=dict(width=0.5, color='#D4AF37')))
    style_fig(fig_scatter, height=440)
    st.plotly_chart(fig_scatter, use_container_width=True)

    top_item = item_agg.iloc[0]['product_detail']
    insight(f"💡 <b>{top_item}</b> is the single best-performing menu item by {m_label.lower()}. "
            "Items with high revenue but relatively low quantity (upper-left quadrant) "
            "represent high-margin premium offerings ideal for upselling campaigns.")

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ☕ <b>Afficionado Coffee Roasters</b> — Sales &amp; Operational Demand Analytics Dashboard<br>
    Data: 2025 Transactions | Locations: Astoria · Hell's Kitchen · Lower Manhattan<br>
    <span style="font-size:11px;">Built with Streamlit &amp; Plotly · Columns used: transaction_id, transaction_time,
    Day_Shifts, transaction_qty, unit_price, Revenue_generated, store_location, product_category,
    product_type, product_detail</span>
</div>""", unsafe_allow_html=True)