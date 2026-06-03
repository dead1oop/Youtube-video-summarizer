import streamlit as st


def inject_premium_theme() -> None:
    """Injects the exact modern, cool-tone dark AI SaaS theme layout into the viewport."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Global Application Color Palette Variables */
            :root {
                --background: #020617;
                --primary-surface: #0F172A;
                --card-surface: #1E293B;
                --primary-accent: #06B6D4;
                --secondary-accent: #38BDF8;
                --primary-text: #F8FAFC;
                --secondary-text: #94A3B8;
            }

            /* Main Canvas Overrides */
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: var(--background) !important;
                color: var(--primary-text) !important;
                font-family: 'Inter', sans-serif !important;
            }
            
            /* Primary Surface: Sidebar Navigation */
            [data-testid="stSidebar"] {
                background-color: var(--primary-surface) !important;
                border-right: 1px solid var(--card-surface) !important;
            }
            
            /* Card Surface: Glassmorphic Component Layout Blocks */
            .saas-card {
                background: var(--card-surface);
                border: 1px solid rgba(6, 182, 212, 0.15);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .saas-card:hover {
                transform: translateY(-2px);
                border-color: var(--primary-accent);
                box-shadow: 0 0 20px rgba(6, 182, 212, 0.25);
            }
            
            /* Nested Analytics Metric Containers */
            .metric-box {
                background: var(--primary-surface);
                border: 1px solid var(--card-surface);
                border-radius: 12px;
                padding: 16px;
                text-align: center;
            }
            .metric-box h4 {
                color: var(--secondary-text) !important;
                font-size: 0.85rem !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .metric-box div {
                color: var(--primary-accent) !important;
                font-size: 1.75rem !important;
                font-weight: 700 !important;
            }

            /* Keep all main content visible */
            [data-testid="stAppViewContainer"] h1,
            [data-testid="stAppViewContainer"] h2,
            [data-testid="stAppViewContainer"] h3,
            [data-testid="stAppViewContainer"] p,
            [data-testid="stAppViewContainer"] label,
            [data-testid="stAppViewContainer"] .stMarkdown,
            [data-testid="stTextArea"] textarea,
            [data-testid="stTextInput"] input,
            [data-testid="stSelectbox"] div {
                color: var(--primary-text) !important;
                -webkit-text-fill-color: var(--primary-text) !important;
            }
            [data-testid="stCaptionContainer"] {
                color: var(--secondary-text) !important;
            }

            /* Action Control Buttons: Dual Accent Gradient Highlight Loop */
            .stButton>button {
                background: linear-gradient(135deg, var(--primary-accent) 0%, var(--secondary-accent) 100%) !important;
                color: var(--background) !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.6rem 1.5rem !important;
                box-shadow: 0 4px 14px 0 rgba(6, 182, 212, 0.3) !important;
                transition: all 0.2s ease !important;
            }
            .stButton>button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px 0 rgba(6, 182, 212, 0.5) !important;
            }
            
            /* Hide Streamlit chrome only (do NOT hide content headers) */
            #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
                visibility: hidden;
                height: 0;
            }
        </style>
    """, unsafe_allow_html=True)