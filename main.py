import streamlit as st
import numpy as np
import pandas as pd

# Configure page
st.set_page_config(
    page_title="K-Factor Calculator",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        color: #2E86AB;
        text-align: center;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 15px 0;
    }
    .result-box {
        background-color: #e8f5e8;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Material properties database
MATERIALS = {
    "Aluminum 1100": {"description": "Soft aluminum", "typical_k": 0.33},
    "Aluminum 6061": {"description": "Medium strength aluminum", "typical_k": 0.35},
    "Steel - Mild": {"description": "Low carbon steel", "typical_k": 0.42},
    "Steel - Stainless 304": {"description": "Austenitic stainless", "typical_k": 0.45},
    "Steel - Spring": {"description": "High carbon steel", "typical_k": 0.48},
    "Copper": {"description": "Pure copper", "typical_k": 0.35},
    "Brass": {"description": "Copper-zinc alloy", "typical_k": 0.38},
}

# Logistic function for K-factor
@st.cache_data
def calculate_k_factor(r_s):
    """Calculate K-factor using logistic function"""
    a = 0.277833218
    b = 1.056058295
    c = 0.608320238
    d = 0.502506534
    return d + (a - d) / (1 + (r_s / c) ** b)

# Bend allowance calculation
def calculate_bend_allowance(k_factor, bend_angle_deg, inner_radius, thickness):
    """Calculate bend allowance"""
    bend_angle_rad = np.radians(bend_angle_deg)
    return bend_angle_rad * (inner_radius + k_factor * thickness)

def calculate_bend_deduction(bend_allowance, inner_radius, thickness, bend_angle_deg):
    """Calculate bend deduction"""
    bend_angle_rad = np.radians(bend_angle_deg)
    outside_setback = np.tan(bend_angle_rad / 2) * (inner_radius + thickness)
    return 2 * outside_setback - bend_allowance

# Approximation table data
table_data = {
    'r/s': [0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 25.0],
    'k': [0.33, 0.37, 0.385, 0.405, 0.42, 0.44, 0.455, 0.46, 0.47, 0.475, 0.48, 0.485, 0.49, 0.495, 0.5]
}

# App header
st.markdown('<h1 class="main-header">🔧 K-Factor Calculator for Sheet Metal Bending</h1>', unsafe_allow_html=True)

# Information section
with st.expander("ℹ️ What is K-Factor?", expanded=False):
    st.markdown("""
    <div class="info-box">
    <strong>K-Factor</strong> represents the location of the neutral axis in a bent sheet metal part. 
    It's crucial for calculating accurate bend allowances and flat pattern dimensions.
    
    <ul>
    <li><strong>K-Factor = 0.5</strong>: Neutral axis at the center of material thickness</li>
    <li><strong>K-Factor < 0.5</strong>: Neutral axis closer to inside radius (typical for most materials)</li>
    <li><strong>r/s ratio</strong>: Inner bend radius divided by sheet thickness</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Main input section
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("📏 Basic Parameters")
    r = st.number_input("Inner Bend Radius (r)", min_value=0.0, value=1.0, step=0.1, format="%.2f", help="The inner radius of the bend")
    s = st.number_input("Sheet Thickness (s)", min_value=0.01, value=1.0, step=0.1, format="%.2f", help="Thickness of the sheet material")
    
    # Unit selection
    unit = st.selectbox("Units", ["mm", "inches"], help="Select measurement units")

with col2:
    st.subheader("🔨 Material Properties")
    material = st.selectbox("Material Type (Reference)", 
                           ["Custom"] + list(MATERIALS.keys()),
                           help="Select material for reference K-factor values")
    
    if material != "Custom":
        st.info(f"**{material}**: {MATERIALS[material]['description']}\n\nTypical K-factor: {MATERIALS[material]['typical_k']}")
    
    # Advanced calculations toggle
    show_advanced = st.checkbox("Show Bend Calculations", help="Calculate bend allowance and deduction")

with col3:
    if show_advanced:
        st.subheader("📐 Bend Parameters")
        bend_angle = st.number_input("Bend Angle (degrees)", min_value=0.1, max_value=180.0, value=90.0, step=5.0)
        
        # Multiple bend calculations
        multiple_bends = st.checkbox("Multiple Bends")
        if multiple_bends:
            num_bends = st.number_input("Number of Bends", min_value=1, max_value=10, value=1, step=1)

# Calculations
if s > 0:
    r_s = r / s
    k_factor = calculate_k_factor(r_s)
    
    # Results display
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("r/s Ratio", f"{r_s:.3f}")
    
    with col2:
        st.metric("K-Factor", f"{k_factor:.4f}")
    
    if show_advanced:
        bend_allowance = calculate_bend_allowance(k_factor, bend_angle, r, s)
        bend_deduction = calculate_bend_deduction(bend_allowance, r, s, bend_angle)
        
        with col3:
            st.metric("Bend Allowance", f"{bend_allowance:.3f} {unit}")
        
        with col4:
            st.metric("Bend Deduction", f"{bend_deduction:.3f} {unit}")
        
        if multiple_bends and 'num_bends' in locals():
            st.info(f"**Total Bend Allowance for {num_bends} bends**: {bend_allowance * num_bends:.3f} {unit}")

else:
    st.error("⚠️ Sheet thickness must be greater than 0")
    k_factor = None
    r_s = None

# K-Factor Analysis section
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 K-Factor Analysis")
    
    # Generate sample data for tabular visualization
    sample_r_s = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0]
    sample_k = [calculate_k_factor(rs) for rs in sample_r_s]
    
    # Create analysis dataframe
    analysis_df = pd.DataFrame({
        'r/s Ratio': sample_r_s,
        'K-Factor': sample_k,
        'Difference from 0.5': [0.5 - k for k in sample_k],
        'Material Behavior': ['Soft' if k < 0.35 else 'Medium' if k < 0.45 else 'Hard' for k in sample_k]
    })
    
    # Highlight user's calculation
    if r_s is not None and k_factor is not None:
        # Add user's calculation to the dataframe
        user_row = {
            'r/s Ratio': r_s,
            'K-Factor': k_factor,
            'Difference from 0.5': 0.5 - k_factor,
            'Material Behavior': 'Your Input ⭐'
        }
        
        # Insert user row in appropriate position
        insert_pos = 0
        for i, rs_val in enumerate(sample_r_s):
            if r_s <= rs_val:
                insert_pos = i
                break
            insert_pos = i + 1
        
        # Create new dataframe with user's data inserted
        analysis_list = analysis_df.to_dict('records')
        analysis_list.insert(insert_pos, user_row)
        analysis_df = pd.DataFrame(analysis_list)
    
    # Display the analysis table
    st.dataframe(
        analysis_df.style.format({
            'r/s Ratio': '{:.2f}',
            'K-Factor': '{:.4f}',
            'Difference from 0.5': '{:.4f}'
        }).highlight_max(subset=['K-Factor'], color='lightgreen')
        .highlight_min(subset=['K-Factor'], color='lightcoral'),
        use_container_width=True
    )
    
    # K-Factor trends explanation
    st.markdown("### 📈 K-Factor Trends")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric(
            "Low r/s (< 1.0)",
            "K ≈ 0.33-0.42",
            "Sharp bends"
        )
    
    with col_b:
        st.metric(
            "Medium r/s (1.0-5.0)",
            "K ≈ 0.42-0.48",
            "Gradual transition"
        )
    
    with col_c:
        st.metric(
            "High r/s (> 5.0)",
            "K ≈ 0.48-0.50",
            "Large radius bends"
        )

with col2:
    st.subheader("📋 Quick Reference")
    
    # Material comparison
    if st.button("Compare Materials"):
        comparison_data = []
        for mat, props in MATERIALS.items():
            comparison_data.append({
                'Material': mat,
                'Typical K-Factor': props['typical_k'],
                'Description': props['description']
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
    
    # Export functionality
    st.markdown("### 💾 Export Options")
    
    if st.button("Generate Report"):
        report_data = {
            'Parameter': ['Inner Radius (r)', 'Sheet Thickness (s)', 'r/s Ratio', 'K-Factor'],
            'Value': [f'{r:.3f} {unit}', f'{s:.3f} {unit}', f'{r_s:.3f}', f'{k_factor:.4f}'],
        }
        
        if show_advanced and 'bend_allowance' in locals():
            report_data['Parameter'].extend(['Bend Angle', 'Bend Allowance', 'Bend Deduction'])
            report_data['Value'].extend([f'{bend_angle:.1f}°', f'{bend_allowance:.3f} {unit}', f'{bend_deduction:.3f} {unit}'])
        
        report_df = pd.DataFrame(report_data)
        st.dataframe(report_df, use_container_width=True)
        
        # CSV download
        csv = report_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"k_factor_calculation_{r}x{s}.csv",
            mime="text/csv"
        )

# Reference table
st.markdown("---")
st.subheader("📚 K-Factor Reference Table")

# Convert to DataFrame for better display
df = pd.DataFrame(table_data)
df.columns = ['r/s Ratio', 'K-Factor']

# Add comparison with calculated values
if r_s is not None:
    # Find closest r/s value in table
    closest_idx = np.argmin(np.abs(np.array(table_data['r/s']) - r_s))
    closest_r_s = table_data['r/s'][closest_idx]
    closest_k = table_data['k'][closest_idx]
    
    st.info(f"**Closest table value**: r/s = {closest_r_s}, K-factor = {closest_k}")
    st.info(f"**Your calculation**: r/s = {r_s:.3f}, K-factor = {k_factor:.4f}")
    st.info(f"**Difference**: {abs(k_factor - closest_k):.4f}")

# Display table with highlighting
styled_df = df.style.format({'r/s Ratio': '{:.1f}', 'K-Factor': '{:.3f}'})
st.dataframe(styled_df, use_container_width=True)

# Footer with tips
st.markdown("---")
with st.expander("💡 Tips for Better Accuracy"):
    st.markdown("""
    - **Material Selection**: Different materials have different K-factors even at the same r/s ratio
    - **Grain Direction**: Bending perpendicular to grain direction typically results in lower K-factors
    - **Tooling**: V-die opening and punch radius affect the final K-factor
    - **Quality**: For critical applications, always validate with test bends
    - **Software Integration**: These values can be imported into CAD software for flat pattern development
    """)
