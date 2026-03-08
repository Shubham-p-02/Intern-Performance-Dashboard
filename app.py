import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page config
st.set_page_config(
    page_title="Intern Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e2d;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00d2ff;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #a0a5b1;
    }
    .stProgress .st-bo {
        background-color: #00d2ff;
    }
    h1, h2, h3 {
        color: #f1f1f1;
    }
    
    /* Hide the top right toolbar which contains 'Record Screen' and other developer options */
    [data-testid="stToolbar"] {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('intern_data.csv')
        df['Week_Start_Date'] = pd.to_datetime(df['Week_Start_Date'])
        return df
    except FileNotFoundError:
        st.error("Data file 'intern_data.csv' not found. Please run data_generator.py first.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Application Title
st.title("📊 Intern Performance Dashboard")
st.markdown("Monitor and analyze intern performance metrics across various domains.")
st.divider()

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

total_interns = df['Intern_ID'].nunique()
avg_perf_score = df['Performance_Score'].mean()
avg_attendance = (df['Days_Present'].sum() / df['Total_Working_Days'].sum()) * 100
total_tasks_completed = df['Tasks_Completed'].sum()
total_tasks_assigned = df['Tasks_Assigned'].sum()
task_completion_rate = (total_tasks_completed / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Interns</div>
            <div class="metric-value">{total_interns}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Performance</div>
            <div class="metric-value">{avg_perf_score:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Attendance Rate</div>
            <div class="metric-value">{avg_attendance:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Task Completion Rate</div>
            <div class="metric-value">{task_completion_rate:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)


st.divider()

# Main Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Weekly Task Completion")
    
    # Group by week and sum tasks
    weekly_tasks = df.groupby('Week_Number')[['Tasks_Assigned', 'Tasks_Completed']].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('none') # Transparent background
    ax.set_facecolor('none')
    
    bar_width = 0.35
    index = weekly_tasks['Week_Number']
    
    ax.bar(index - bar_width/2, weekly_tasks['Tasks_Assigned'], bar_width, label='Assigned', color='#4e54c8')
    ax.bar(index + bar_width/2, weekly_tasks['Tasks_Completed'], bar_width, label='Completed', color='#8f94fb')
    
    ax.set_xlabel('Week', color='white')
    ax.set_ylabel('Number of Tasks', color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#555555')
        
    ax.legend()
    st.pyplot(fig)

with col_right:
    st.subheader("🎯 Average Performance Score by Week")
    
    weekly_perf = df.groupby('Week_Number')['Performance_Score'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    ax.plot(weekly_perf['Week_Number'], weekly_perf['Performance_Score'], marker='o', color='#00d2ff', linewidth=3)
    ax.fill_between(weekly_perf['Week_Number'], weekly_perf['Performance_Score'], alpha=0.2, color='#00d2ff')
    
    ax.set_xlabel('Week', color='white')
    ax.set_ylabel('Performance Score (%)', color='white')
    ax.set_ylim(0, 100)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#555555')
        
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    st.pyplot(fig)


st.divider()

# Bottom section
col_bottom_left, col_bottom_right = st.columns(2)

with col_bottom_left:
    st.subheader("🏢 Domain-wise Analysis")
    
    domain_perf = df.groupby('Domain')['Performance_Score'].mean().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    y_pos = np.arange(len(domain_perf))
    ax.barh(y_pos, domain_perf.values, color='#00d2ff')
    ax.set_yticks(y_pos, labels=domain_perf.index, color='white')
    ax.set_xlabel('Average Performance Score (%)', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.set_xlim(0, 100)
    
    for spine in ax.spines.values():
        spine.set_color('#555555')
        
    st.pyplot(fig)


with col_bottom_right:
    st.subheader("📅 Attendance Analytics")
    
    # Calculate attendance distribution
    attendance_rates = (df.groupby('Name')['Days_Present'].sum() / 
                       df.groupby('Name')['Total_Working_Days'].sum()) * 100
                       
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    # Fixed explicitly passing align to hist
    ax.hist(attendance_rates, bins=10, range=(0, 100), color='#ff4b4b', edgecolor='black', alpha=0.7)
    
    ax.set_xlabel('Attendance Rate (%)', color='white')
    ax.set_ylabel('Number of Interns', color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#555555')
        
    st.pyplot(fig)

st.divider()
