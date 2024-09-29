import streamlit as st
import pandas as pd
import plotly.express as px


# Set the page configuration
st.set_page_config(layout="wide", page_title="Job Dashboard", page_icon="📊")

# Load the data
df = pd.read_parquet('job_data.parquet')
df.to_sql('job_data', 'sqlite:///job_data.db', if_exists='replace')
# Custom CSS for centering and aesthetics
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center !important;
    }
    .stPlotlyChart {
        display: flex;
        justify-content: center;
    }
    .big-font {
        font-size:30px !important;
        color: #4CAF50;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .sub-font {
        font-size:20px !important;
        color: #333333;
    }
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .stApp {
        background-color: #F7F7F7;
    }
    </style>
    """, unsafe_allow_html=True
)

# Page title
st.markdown("<h1 class='big-font centered-text'>Job Dashboard</h1>", unsafe_allow_html=True)

# Unique job-related filters
unique_jobs = ['ALL']+list(df['Job Title'].unique())
unique_exps = df['Experience'].unique()
unique_locs = df['Location'].unique()

# Center the select box
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
jobs_searched = st.selectbox(label='Select Job Title', options=unique_jobs)
st.markdown("</div>", unsafe_allow_html=True)

# Filter data based on selected job
if jobs_searched:
    if(jobs_searched!='ALL'):
        df = df[df['Job Title'] == jobs_searched]

# Helper functions
def get_ratings():
    valid_ratings=pd.to_numeric(df['Ratings'],errors='coerce').dropna()
    return int(valid_ratings.mean()) if not valid_ratings.empty else 0

def skills_counting():
    df['Skills'] = df['Skills'].fillna('').apply(lambda x: [skill.strip() for skill in x.split(',') if len(skill.strip()) <= 30])
    all_skills = df['Skills'].explode()  
    skills_counts = all_skills.value_counts()  
    return pd.DataFrame({'Skill': skills_counts.index, 'Count': skills_counts.values}).sort_values(by='Count', ascending=True)


def graduation_req():
    valid_degrees = df[df['Degree Requirements'] != 'NONE']
    return int((len(valid_degrees)/len(df))*10) if len(valid_degrees)>0 else 0


# Skills DataFrame
skills_df = skills_counting()

# Display Skill DataFrame
st.markdown("<h2 class='sub-font centered-text'>Skills Data</h2>", unsafe_allow_html=True)
# st.dataframe(skills_df)

# Create a 3-column layout for stats
left_c, mid_c, right_c = st.columns(3)

with left_c:
    st.markdown("<h3 class='sub-font centered-text'>TOTAL ANALYSED</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 class='centered-text'>{len(skills_df)}</h4>", unsafe_allow_html=True)

with mid_c:
    st.markdown("<h3 class='sub-font centered-text'>Average Ratings</h3>", unsafe_allow_html=True)
    rating = get_ratings()
    st.markdown(f"<h4 class='centered-text'>{rating} {'⭐' * rating}</h4>", unsafe_allow_html=True)

with right_c:
    st.markdown("<h3 class='sub-font centered-text'>Graduation Requirement</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 class='centered-text'>{graduation_req() * 10}%</h4>", unsafe_allow_html=True)

st.markdown('---')

# Bar Graph
max_value = skills_df['Count'].max()

# Dynamically calculate height based on the number of rows (skills) to prevent overcrowding
bar_height = 30  # Fixed bar height for each skill
height = len(skills_df) * bar_height  # Total chart height based on number of bars

fit_skills = px.bar(
    skills_df,
    x='Count',
    y='Skill',
    orientation='h',
    title='<b>Skills and Their Counts</b>',
    text='Count',
    range_x=[0, max_value],  # Set the x-axis range to maintain uniform bars
    template='plotly_white',
    height=height  # Dynamically set the height based on the number of skills
)

# Update layout to ensure bars are equal and skill names are visible
fit_skills.update_layout(
    xaxis=dict(showgrid=False),  # Hide grid lines
    yaxis=dict(
        tickfont=dict(size=12),  # Ensure skill labels are readable
        automargin=True,  # Ensure enough margin for long labels
    ),
    margin=dict(l=150, r=20, t=50, b=20),  # Adjust margins for clear visibility of skill names
    uniformtext_minsize=8,  # Ensure text doesn't become too small
    uniformtext_mode='hide',  # Prevent text from overlapping
)

# Ensure consistent bar size even with larger datasets
fit_skills.update_traces(marker_line_width=1.5, marker_line_color="black",textposition='inside',textfont_color='white')  # Add an outline for clear separation of bars

# Display the chart in the center
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.plotly_chart(fit_skills, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

