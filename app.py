import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Pakistan Job Market Insights", layout="wide", page_icon="🇵🇰")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading Function
@st.cache_data
def load_data():
    try:
        # Load the cleaned dataset
        df = pd.read_csv("data/processed/all_pakistan_jobs.csv")
        
        # Safety: Check if 'City' column exists, if not, create from 'Location'
        if 'City' not in df.columns and 'Location' in df.columns:
            df['City'] = df['Location'].apply(lambda x: str(x).split(',')[0].strip())
        elif 'City' not in df.columns:
            df['City'] = "Unknown"

        # Ensure Salary_Numeric is float for calculations
        if 'Salary_Numeric' in df.columns:
            df['Salary_Numeric'] = pd.to_numeric(df['Salary_Numeric'], errors='coerce')
        else:
            df['Salary_Numeric'] = None

        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # 3. Sidebar Filters
    st.sidebar.header("🔍 Filters")
    
    # --- Category Filter ---
    cat_col = 'Category' if 'Category' in df.columns else 'Title'
    all_fields = df[cat_col].unique().tolist()
    selected_fields = st.sidebar.multiselect("Select Job Field", options=all_fields, default=all_fields[:5])

    # --- City Filter (With Robust Check) ---
    all_cities = df['City'].unique().tolist()
    selected_cities = st.sidebar.multiselect("Select City", options=all_cities, default=all_cities)

    # --- Source Filter ---
    all_sources = df['Source'].unique().tolist()
    selected_sources = st.sidebar.multiselect("Select Source", options=all_sources, default=all_sources)

    # Apply Filters (Masking)
    mask = (df['City'].isin(selected_cities)) & \
           (df['Source'].isin(selected_sources)) & \
           (df[cat_col].isin(selected_fields))
    
    filtered_df = df[mask]

    # 4. Header & Metrics
    st.title("🇵🇰 Pakistan Job Market Analysis Dashboard")
    st.markdown(f"Currently analyzing **{len(filtered_df)}** job postings across various sectors.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Jobs", f"{len(filtered_df)}")
    
    avg_sal = filtered_df['Salary_Numeric'].mean() if 'Salary_Numeric' in filtered_df.columns else None
    m2.metric("Avg Salary (PKR)", f"{avg_sal:,.0f}" if pd.notna(avg_sal) else "N/A")
    
    top_city = filtered_df['City'].mode()[0] if not filtered_df.empty else "N/A"
    m3.metric("Top Hiring City", top_city)
    
    m4.metric("Sources Scraped", len(selected_sources))

    st.divider()

    # 5. FIELD ANALYSIS SECTION
    st.header("📊 Field & Category Analysis")
    col_a, col_b = st.columns(2)

    with col_a:
        st.write("### Top Job Categories by Volume")
        field_counts = filtered_df[cat_col].value_counts().nlargest(10).reset_index()
        field_counts.columns = [cat_col, 'Count']
        
        fig_fields = px.bar(field_counts, x='Count', y=cat_col, orientation='h',
                           color='Count', color_continuous_scale='Viridis',
                           template='plotly_white')
        st.plotly_chart(fig_fields, use_container_width=True)

    with col_b:
        st.write("### Salary Comparison by Field")
        if 'Salary_Numeric' in filtered_df.columns and not filtered_df['Salary_Numeric'].dropna().empty:
            sal_by_field = filtered_df.groupby(cat_col)['Salary_Numeric'].mean().sort_values(ascending=False).nlargest(10).reset_index()
            fig_sal = px.bar(sal_by_field, x=cat_col, y='Salary_Numeric',
                            color='Salary_Numeric', template='plotly_white',
                            labels={'Salary_Numeric': 'Avg Salary (PKR)'})
            st.plotly_chart(fig_sal, use_container_width=True)
        else:
            st.info("Salary data (Numeric) not available for these filters.")

    # 6. GEOGRAPHIC & SOURCE ANALYSIS
    st.divider()
    st.header("📍 Geographic Distribution")
    c1, c2 = st.columns([1, 1])

    with c1:
        st.write("### Job Openings by City")
        city_counts = filtered_df['City'].value_counts().reset_index()
        city_counts.columns = ['CityName', 'Jobs']
        fig_city = px.pie(city_counts, names='CityName', values='Jobs', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_city, use_container_width=True)

    with c2:
        st.write("### Source Distribution")
        source_counts = filtered_df['Source'].value_counts().reset_index()
        source_counts.columns = ['Platform', 'JobsFound']
        fig_source = px.bar(source_counts, x='Platform', y='JobsFound', 
                           color='Platform', template='plotly_white')
        st.plotly_chart(fig_source, use_container_width=True)

    # 7. RAW DATA TABLE
    st.divider()
    st.write("### 📋 Detailed Job Listings")
    # Show only columns that exist
    available_cols = [c for c in ['Title', 'Company', 'City', 'Salary', 'Source'] if c in filtered_df.columns]
    st.dataframe(filtered_df[available_cols], use_container_width=True)

else:
    st.error("⚠️ Data file not found or empty! Please run 'python main.py' first.")