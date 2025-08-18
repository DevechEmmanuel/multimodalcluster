# dashboard_app.py - Mobile-Responsive with Welcome Interface
# ------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
import os
import re

# --- Custom CSS ONLY for "Click to Discover Cluster" button ---
st.markdown("""
<style>
/* Match only the specific button by its label text */
div.stButton:has(button:contains("Click to Discover Cluster")) button {
    background-color: white !important;
    color: #dc3545 !important;  /* red text */
    border: 2px solid #dc3545 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}

/* Hover effect */
div.stButton:has(button:contains("Click to Discover Cluster")) button:hover {
    background-color: #dc3545 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# --- Page config ---
st.set_page_config(
    page_title="Student Engagement Clustering Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Mobile-Responsive CSS theme ---
st.markdown("""
<style>
:root{
  --brand-primary:#1e88e5;
  --brand-primary-strong:#1565c0;
  --brand-soft:#eaf2ff;
  --text-dark:#1f2a44;
  --text-on-primary:#ffffff;
  --surface:#ffffff;
  --muted:#6b7a90;
}

/* Mobile-first responsive design */
* {
  box-sizing: border-box;
}

/* App background */
.stApp {
  background: linear-gradient(135deg, #f7fbff, #eef4fb 45%, #f7fbff);
}

/* Mobile responsive adjustments */
@media (max-width: 768px) {
  .main .block-container {
    padding: 1rem;
    max-width: 100%;
  }
  
  /* Make columns stack on mobile */
  div[data-testid="column"] {
    width: 100% !important;
    flex: 1 1 100% !important;
    min-width: 100% !important;
  }
  
  /* Adjust font sizes for mobile */
  h1 { font-size: 1.5rem !important; }
  h2 { font-size: 1.3rem !important; }
  h3 { font-size: 1.1rem !important; }
  
  /* Mobile-friendly buttons */
  .stButton > button {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
  }
  
  /* Mobile input fields */
  .stTextInput > div > div > input {
    font-size: 16px;
  }
}

/* Welcome Section Styles */
.welcome-container {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 50%, #0d47a1 100%);
  color: white;
  border-radius: 20px;
  padding: 2.5rem 2.5rem 0.5rem 2.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 20px 60px rgba(21,101,192,0.25);
  text-align: center;
  position: relative;
}

.welcome-title {
  font-size: 3rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.welcome-subtitle {
  font-size: 1.4rem;
  margin: 0 0 0.75rem 0;
  opacity: 0.95;
  line-height: 1.4;
}

/* Enhanced Discover Button Container */
.discover-button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0.25rem 0 1.5rem 0;
  padding: 0.25rem;
}

/* Custom styling for the discover button with floating animation */
.stButton > button[data-testid="baseButton-primary"] {
  background: linear-gradient(135deg, #ff6b35, #f7931e) !important;
  border: none !important;
  color: white !important;
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  padding: 1.2rem 3rem !important;
  border-radius: 50px !important;
  box-shadow: 0 8px 25px rgba(255,107,53,0.4) !important;
  transition: all 0.3s ease !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  min-height: 65px !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton > button[data-testid="baseButton-primary"]:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 35px rgba(255,107,53,0.5) !important;
  background: linear-gradient(135deg, #ff8a65, #ffb74d) !important;
}

.stButton > button[data-testid="baseButton-primary"]:active {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(255,107,53,0.4) !important;
}

/* Enhanced floating animation - combination of pulse and gentle float */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
    box-shadow: 0 8px 25px rgba(255,107,53,0.4);
  }
  25% {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(255,107,53,0.5);
  }
  50% {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(255,107,53,0.6), 0 0 0 10px rgba(255,107,53,0.1);
  }
  75% {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(255,107,53,0.5);
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 8px 25px rgba(255,107,53,0.4);
  }
  50% {
    box-shadow: 0 8px 25px rgba(255,107,53,0.6), 0 0 0 15px rgba(255,107,53,0.1);
  }
}

.stButton > button[data-testid="baseButton-primary"] {
  animation: float 3s ease-in-out infinite, glow 2s ease-in-out infinite;
}

/* Mobile responsive button */
@media (max-width: 768px) {
  .welcome-container {
    padding: 1.5rem 1.5rem 0.5rem 1.5rem;
  }
  
  .welcome-title {
    font-size: 2.2rem;
  }
  
  .welcome-subtitle {
    font-size: 1.1rem;
  }
  
  .stButton > button[data-testid="baseButton-primary"] {
    font-size: 1.2rem !important;
    padding: 1rem 2.5rem !important;
    min-height: 60px !important;
  }
  
  .discover-button-container {
    margin: 0.25rem 0 1rem 0;
    padding: 0.25rem;
  }
}

/* Cards */
.blue-card {
  background: var(--brand-soft);
  border: 1px solid #c7ddff;
  border-radius: 18px;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(17,69,158,0.08);
  margin-bottom: 1.5rem;
}

.chart-card {
  background: var(--surface);
  border: 2px solid var(--brand-primary-strong);
  border-radius: 18px;
  padding: 1rem;
  box-shadow: 0 8px 24px rgba(17,69,158,0.10);
  margin-bottom: 1.5rem;
}

/* Stat cards */
.stat-card {
  background: linear-gradient(180deg,#eaf2ff,#dfeaff);
  border: 1px solid #c7ddff;
  border-radius: 14px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 6px 16px rgba(17,69,158,0.08);
  margin-bottom: 1rem;
}

.stat-title { 
  font-weight:700; 
  font-size:0.95rem; 
  color:var(--text-dark); 
  margin-bottom:6px; 
}

.stat-number { 
  font-weight:800; 
  font-size:1.4rem; 
  color:var(--brand-primary-strong); 
  margin:0; 
}

.stat-pct { 
  font-weight:700; 
  color:#365a9c; 
}

/* Hero */
.hero {
  background: linear-gradient(120deg,var(--brand-primary),var(--brand-primary-strong));
  color: var(--text-on-primary);
  border-radius: 22px;
  padding: 1.5rem;
  box-shadow: 0 14px 36px rgba(21,101,192,0.20);
  margin-bottom: 1.5rem;
}

.hero h1 { 
  margin:0; 
  font-size:1.7rem; 
  font-weight:700; 
}

/* Section chip */
.section-chip {
  display:inline-flex; 
  align-items:center; 
  gap:8px; 
  background:var(--brand-soft);
  border:1px solid #c7ddff; 
  border-radius:999px; 
  padding:6px 12px; 
  font-weight:600; 
  color:var(--text-dark);
  margin-bottom:10px;
}

.section-chip .icon { 
  background: var(--brand-primary); 
  color:var(--text-on-primary); 
  border-radius:999px; 
  width:22px; 
  height:22px; 
  display:inline-flex; 
  align-items:center; 
  justify-content:center; 
  font-size:12px;
}

/* Callout */
.callout {
  background: linear-gradient(180deg,#f3f9ff,#edf6ff);
  border:1px solid #cfe2ff;
  border-left:6px solid var(--brand-primary-strong);
  border-radius:14px; 
  padding:14px;
  box-shadow: 0 8px 20px rgba(17,69,158,0.08);
  color:var(--text-dark);
  margin: 1rem 0;
}

/* Recommendation cards */
.rec-grid { 
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .rec-grid {
    grid-template-columns: 1fr;
  }
}

.rec-card {
  background:var(--surface);
  border:1px solid #d9e5ff;
  border-radius:14px;
  padding:1rem;
  box-shadow:0 8px 22px rgba(17,69,158,0.06);
}

/* Login card */
.login-wrapper { 
  display:flex; 
  justify-content:center; 
  margin: 1.5rem 0; 
}

.login-card {
  background: linear-gradient(180deg,#eaf2ff,#dfeaff);
  border:1px solid #c7ddff;
  border-radius:18px;
  padding:1.5rem;
  width: 100%;
  max-width: 420px;
  box-shadow:0 12px 36px rgba(17,69,158,0.12);
}

.login-card h3 { 
  margin-top:0; 
  color:var(--text-dark); 
}

/* Utility classes */
.m-0 { margin:0; }
.mb-8 { margin-bottom:8px; }
.text-center { text-align: center; }

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Hardcoded credentials
# ------------------------------------------------------------
HARDCODED_USERNAME = "educator"
HARDCODED_PASSWORD = "1234"

# ------------------------------------------------------------
# Session state initialization
# ------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = "All"
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

# ------------------------------------------------------------
# Welcome Page Function
# ------------------------------------------------------------
def show_welcome_page():
    # Hero section with enhanced styling
    st.markdown("""
    <div class="welcome-container">
        <h1 class="welcome-title">🎓 Student Engagement Clustering Dashboard</h1>
        <p class="welcome-subtitle">Unlock insights into student learning patterns with advanced clustering analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced centered discover button with better visibility
    st.markdown('<div class="discover-button-container">', unsafe_allow_html=True)
    
    # Use three columns for perfect centering
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Click to Discover Clusters", 
                    key="discover_btn", 
                    help="Access the clustering dashboard and explore student engagement patterns", 
                    type="primary",
                    use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Use streamlit components instead of pure HTML
    st.markdown("## What is Student Engagement Clustering?")
    
    # Create cards using streamlit columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔍 Pattern Recognition
        Our advanced clustering algorithm analyzes student behavior patterns including video engagement, pause frequency, likes, and forum participation to identify distinct learning groups.
        """)
        
        st.markdown("""
        ### 📈 Engagement Metrics
        **Analysis based on:**
        - Video play frequency
        - Pause patterns  
        - Like interactions
        - Forum participation
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Data-Driven Insights
        Transform raw engagement metrics into actionable insights. Understand how different student groups interact with course materials and identify areas for improvement.
        """)
        
        st.markdown("""
        ### 💡 Educator Benefits
        - Identify at-risk students early
        - Customize intervention strategies
        - Improve course effectiveness
        - Enhance student outcomes
        """)
    
    with col3:
        st.markdown("""
        ### 🎯 Personalized Learning
        Enable targeted interventions by understanding the unique characteristics of each student cluster. Tailor your teaching approach to meet diverse learning needs.
        """)
        
        st.markdown("""
        ### 👥 Student Groups Identified
        **The Enthusiasts:** Highly engaged students  
        **Steady Learners:** Consistent participants  
        **Silent Observers:** Passive but present  
        **Disengaged:** Need extra support
        """)
    
    st.markdown("---")
    
    # About section
    st.markdown("""
    <div style="text-align: center; color: #6b7a90; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin: 1rem 0;">
        <p><strong>About This Tool:</strong> This dashboard uses machine learning clustering techniques to group students based on their engagement patterns. The insights help educators understand diverse learning behaviors and implement targeted teaching strategies.</p>
        <p style="margin-top: 1rem;"><em>Developed by Oluwatudimu Emmanuel Tobi - IFS/19/0622</em></p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# Main Dashboard Function
# ------------------------------------------------------------
def show_dashboard():
    # Back to welcome button
    col1, col2 = st.columns([2, 10])
    with col1:
        if st.button("← Welcome", key="back_welcome", help="Back to welcome page"):
            st.session_state.show_dashboard = False
            st.rerun()
    
    # Load data
    try:
        df = pd.read_csv("clustered_students.csv")
    except FileNotFoundError:
        st.error("clustered_students.csv not found in the app folder. Put it next to this file and rerun.")
        st.stop()

    # Normalize cluster column name
    cluster_col = "Cluster Name" if "Cluster Name" in df.columns else ("Cluster" if "Cluster" in df.columns else None)
    if cluster_col is None:
        st.error("No 'Cluster' or 'Cluster Name' column found in the CSV.")
        st.stop()

    # Ensure friendly applicant column
    applicant_col = "ApplicantName" if "ApplicantName" in df.columns else ("Applicant Name" if "Applicant Name" in df.columns else None)

    # Determine which numeric features are available
    expected_features = ['Played', 'Paused', 'Likes', 'Segment']
    feature_cols = [c for c in expected_features if c in df.columns]

    # Helpful derived values
    total_students = len(df)
    cluster_counts = df[cluster_col].value_counts().sort_index()
    cluster_pct = (cluster_counts / total_students * 100).round(1)

    # HERO + OVERVIEW + CLUSTER CHART
    st.markdown(f"""
    <div class="hero">
      <h1>🎓 Student Engagement Clustering Dashboard</h1>
      <p class="m-0">Group students by engagement and get educator-ready recommendations. (Login required to view personal details)</p>
    </div>
    """, unsafe_allow_html=True)

    # Overview cards
    with st.container():
        st.markdown('<div class="blue-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-chip"><span class="icon">📌</span>Overview</div>', unsafe_allow_html=True)

        # Metric row: responsive layout
        cols = st.columns([1] + [1]*min(4, len(cluster_counts)))  # Limit columns for mobile
        
        # First column: total
        with cols[0]:
            st.metric("Total students", total_students)
        
        # Rest: per-cluster (limit to prevent overflow on mobile)
        for i, (name, cnt) in enumerate(list(cluster_counts.items())[:min(4, len(cols)-1)]):
            with cols[i+1]:
                pct = cluster_pct[name]
                st.markdown(
                    f"""
                    <div class="stat-card">
                      <div class="stat-title">{name}</div>
                      <div class="stat-number">{int(cnt)}</div>
                      <div class="stat-pct">{pct}%</div>
                    </div>
                    """, unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # Cluster distribution chart
    cluster_counts_df = cluster_counts.reset_index()
    cluster_counts_df.columns = [cluster_col, 'Number of Students']
    fig = px.bar(
        cluster_counts_df,
        x=cluster_col,
        y='Number of Students',
        color=cluster_col,
        text='Number of Students',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        height=360, 
        margin=dict(l=10, r=10, t=40, b=20), 
        showlegend=False,
        font=dict(size=10)  # Smaller font for mobile
    )
    fig.update_traces(textposition='outside')

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # LOGIN BOX
    if not st.session_state.logged_in:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h3>🔒 Educator Login</h3>', unsafe_allow_html=True)
        st.write('Enter your username and password to reveal student details and recommendations.')

        uname = st.text_input("Username", key="login_username")
        pwd = st.text_input("Password", type="password", key="login_password")
        
        login_col1, login_col2 = st.columns([1, 1])
        with login_col1:
            login_btn = st.button("Login", key="login_button")
        with login_col2:
            st.write("")

        if login_btn:
            if uname == HARDCODED_USERNAME and pwd == HARDCODED_PASSWORD:
                st.session_state.logged_in = True
                st.success("✅ Login successful — sensitive sections are now visible.")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Footer caption
    st.caption("Note: Developed by Oluwatudimu Emmanuel Tobi - IFS/19/0622")

    # Stop here if not logged in
    if not st.session_state.logged_in:
        st.info("Sensitive sections are hidden. Log in to view student lists, feature comparisons, and recommendations.")
        return

    # LOGOUT button
    logout_col1, logout_col2 = st.columns([1, 5])
    with logout_col1:
        if st.button("Logout"):
            for k in ["login_username", "login_password"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.logged_in = False
            st.success("Logged out. The sensitive sections are hidden again.")
            st.rerun()

    # SECTION 2: Explore students by cluster
    st.markdown('<div class="blue-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-chip mb-8"><span class="icon">🔎</span>Explore students by cluster</div>', unsafe_allow_html=True)

    cluster_options = ["All"] + list(cluster_counts.index)
    selected_cluster = st.selectbox("Choose a cluster to explore:", cluster_options, index=0)

    if selected_cluster == "All":
        subset = df.copy()
    else:
        subset = df[df[cluster_col] == selected_cluster].copy()

    st.write(f"Showing **{len(subset)}** students ({(len(subset)/total_students*100):.1f}% of total)")

    # Columns to show
    cols_to_show = []
    if applicant_col:
        cols_to_show.append(applicant_col)
    cols_to_show += [cluster_col] + feature_cols
    cols_to_show = [c for c in cols_to_show if c in subset.columns]

    # Show sample
    st.dataframe(subset[cols_to_show].head(6), height=260, use_container_width=True)

    with st.expander("Show full table and download"):
        st.dataframe(subset[cols_to_show], height=380, use_container_width=True)
        csv = subset.to_csv(index=False).encode('utf-8')
        st.download_button("Download shown students (CSV)", csv, "students_subset.csv", "text/csv")

    st.markdown('</div>', unsafe_allow_html=True)

    # SECTION 3: Feature comparison
    st.markdown('<div class="blue-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-chip"><span class="icon">📈</span>Feature comparison: selected cluster vs overall</div>', unsafe_allow_html=True)

    if len(feature_cols) == 0:
        st.info("No numeric engagement features (Played/Paused/Likes/Segment) were found in the CSV to compare.")
    else:
        overall_mean = df[feature_cols].mean()

        if selected_cluster == "All":
            cluster_means = df.groupby(cluster_col)[feature_cols].mean().round(2)
            st.dataframe(cluster_means, use_container_width=True)
        else:
            cluster_mean = subset[feature_cols].mean()
            compare_df = pd.DataFrame({
                'Feature': feature_cols,
                'Selected cluster mean': cluster_mean.values,
                'Overall mean': overall_mean.values
            })

            fig2 = px.bar(
                compare_df.melt(id_vars='Feature', var_name='Group', value_name='Value'),
                x='Feature', y='Value', color='Group', barmode='group',
                title=f"Selected cluster ({selected_cluster}) vs overall",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig2.update_layout(
                height=380, 
                margin=dict(l=10, r=10, t=40, b=20), 
                plot_bgcolor="white", 
                paper_bgcolor="white",
                font=dict(size=10)
            )
            
            st.markdown('<div class="chart-card mb-12">', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Interpretation
            interpretation_parts = []
            for feature in feature_cols:
                cluster_val = cluster_mean[feature]
                overall_val = overall_mean[feature]
                if overall_val != 0:
                    diff_pct = ((cluster_val - overall_val) / overall_val) * 100
                    if abs(diff_pct) >= 5:
                        direction = "more" if diff_pct > 0 else "fewer"
                        if feature.lower() == "played":
                            feature_name = "videos"
                            action_word = "watch"
                        elif feature.lower() == "paused":
                            feature_name = "pauses"
                            action_word = "have"
                        elif feature.lower() == "likes":
                            feature_name = "likes"
                            action_word = "give"
                        elif feature.lower() == "segment":
                            feature_name = "forum messages"
                            action_word = "post"
                        else:
                            feature_name = feature
                            action_word = "have"

                        interpretation_parts.append(
                            f"{selected_cluster} {action_word} {abs(diff_pct):.0f}% {direction} {feature_name} than average"
                        )

            if interpretation_parts:
                if len(interpretation_parts) > 1:
                    last_part = interpretation_parts.pop()
                    interpretation_text = ", ".join(interpretation_parts) + f", but {last_part}"
                else:
                    interpretation_text = interpretation_parts[0]
            else:
                interpretation_text = "This cluster's engagement is close to the overall average across the features."

            st.markdown(f'<div class="callout"><strong>Interpretation:</strong> {interpretation_text}.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # SECTION 4: Educator insights & recommendations
    st.markdown('<div class="blue-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-chip"><span class="icon">💡</span>Educator insights & recommended actions</div>', unsafe_allow_html=True)

    # Recommendations
    recommendations = {
        "The Enthusiasts": [
            "Offer advanced readings or enrichment activities.",
            "Invite them as peer mentors or group leaders.",
            "Give formative challenges to keep them engaged."
        ],
        "The Steady Learners": [
            "Give regular reminders and short recaps.",
            "Provide practice quizzes and worked examples.",
            "Encourage participation with low-stakes interactions."
        ],
        "The Silent Observers": [
            "Add interactive polls and tiny quizzes during videos.",
            "Use prompts or reflective questions to elicit responses.",
            "Reach out with personalized, friendly nudges."
        ],
        "The Disengaged": [
            "Provide very short, simplified materials and quick wins.",
            "Offer targeted outreach (office hours, mentorship).",
            "Consider adaptive content paths and scaffolded tasks."
        ]
    }

    def map_cluster_label(label):
        """Map cluster labels to recommendation keys, handling emojis and variations"""
        if not label or label == "All":
            return None
        
        clean_label = re.sub(r'[^\w\s]', '', str(label)).strip().lower()
        
        if "enthusiast" in clean_label:
            return "The Enthusiasts"
        elif "steady" in clean_label or "learner" in clean_label:
            return "The Steady Learners"
        elif "silent" in clean_label or "observer" in clean_label:
            return "The Silent Observers"
        elif "disengaged" in clean_label:
            return "The Disengaged"
        
        # Fallback: try partial matching with recommendation keys
        for key in recommendations.keys():
            key_clean = re.sub(r'[^\w\s]', '', key).strip().lower()
            if key_clean in clean_label or clean_label in key_clean:
                return key
        
        return None

    # Render recommendations as responsive cards
    st.markdown('<div class="rec-grid">', unsafe_allow_html=True)

    if selected_cluster == "All":
        # Show all recommendation cards
        for key, recs in recommendations.items():
            html = f'<div class="rec-card"><h4 class="m-0">{key}</h4><ul>'
            for r in recs:
                html += f"<li>{r}</li>"
            html += "</ul></div>"
            st.markdown(html, unsafe_allow_html=True)
    else:
        # Show only the selected cluster's recommendations
        mapped_cluster = map_cluster_label(selected_cluster)
        
        if mapped_cluster and mapped_cluster in recommendations:
            recs = recommendations[mapped_cluster]
            html = f'<div class="rec-card"><h4 class="m-0">{mapped_cluster}</h4><ul>'
            for r in recs:
                html += f"<li>{r}</li>"
            html += "</ul></div>"
            st.markdown(html, unsafe_allow_html=True)
        else:
            # Fallback message if no matching recommendations found
            st.info(f"No specific recommendations available for '{selected_cluster}'. Please check the cluster name mapping.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer caption
    st.caption("Tip: Use the cluster explorer to select a group and download the list for targeted interventions and quick response from online educators. Developed by Oluwatudimu Emmanuel Tobi - IFS/19/0622")

# ------------------------------------------------------------
# MAIN APP LOGIC
# ------------------------------------------------------------

# Show appropriate page based on state
if not st.session_state.show_dashboard:
    show_welcome_page()
else:
    show_dashboard()
