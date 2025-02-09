import streamlit as st
import os
import json
from pathlib import Path
import markdown
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Trading Automation Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #0e1117;
    }
    .stTabs [aria-selected="true"] {
        background-color: #262730;
    }
    .strategy-card {
        padding: 20px;
        border-radius: 5px;
        background-color: #262730;
        margin: 10px 0;
    }
    .notes-section {
        margin-top: 20px;
        padding: 15px;
        background-color: #1e1e1e;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'All'

def load_readme(path):
    """Load and parse README.md file"""
    readme_path = os.path.join(path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            return markdown.markdown(f.read())
    return None

def load_pine_code(path):
    """Load main.pine file"""
    pine_path = os.path.join(path, "main.pine")
    if os.path.exists(pine_path):
        with open(pine_path, 'r') as f:
            return f.read()
    return None

def save_note(strategy_name, note_content, category):
    """Save note to JSON file"""
    notes_dir = Path("notes")
    notes_dir.mkdir(exist_ok=True)
    
    notes_file = notes_dir / "trading_notes.json"
    
    if notes_file.exists():
        with open(notes_file, 'r') as f:
            notes = json.load(f)
    else:
        notes = {}
    
    if category not in notes:
        notes[category] = {}
    
    notes[category][strategy_name] = {
        "content": note_content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(notes_file, 'w') as f:
        json.dump(notes, f, indent=4)

def load_notes():
    """Load all notes from JSON file"""
    notes_file = Path("notes/trading_notes.json")
    if notes_file.exists():
        with open(notes_file, 'r') as f:
            return json.load(f)
    return {}

def main():
    st.title("Trading Automation Dashboard 📈")
    
    # Sidebar
    st.sidebar.header("Navigation")
    
    # Category selection
    categories = ["All", "Indicators", "Strategies"]
    selected_category = st.sidebar.radio("Select Category", categories)
    
    # Search/Filter
    search_term = st.sidebar.text_input("🔍 Search", "")
    
    # Main content area
    tab1, tab2 = st.tabs(["Custom", "TradingView"])
    
    with tab1:
        if selected_category in ["All", "Indicators"]:
            st.header("Custom Indicators")
            custom_indicators_path = "indicators/custom"
            if os.path.exists(custom_indicators_path):
                for indicator in os.listdir(custom_indicators_path):
                    if search_term.lower() in indicator.lower():
                        indicator_path = os.path.join(custom_indicators_path, indicator)
                        if os.path.isdir(indicator_path):
                            with st.expander(f"📊 {indicator}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    # README content
                                    readme_content = load_readme(indicator_path)
                                    if readme_content:
                                        st.markdown(readme_content, unsafe_allow_html=True)
                                    
                                    # Code section
                                    pine_code = load_pine_code(indicator_path)
                                    if pine_code:
                                        st.code(pine_code, language="pine")
                                
                                with col2:
                                    # Notes section
                                    st.markdown("### 📝 Notes")
                                    notes = load_notes()
                                    current_note = notes.get("Indicators", {}).get(indicator, {}).get("content", "")
                                    
                                    note_input = st.text_area(
                                        "Add/Edit Note",
                                        value=current_note,
                                        key=f"note_{indicator}"
                                    )
                                    
                                    if st.button("Save Note", key=f"save_{indicator}"):
                                        save_note(indicator, note_input, "Indicators")
                                        st.success("Note saved successfully!")
        
        if selected_category in ["All", "Strategies"]:
            st.header("Custom Strategies")
            custom_strategies_path = "strategies/custom"
            if os.path.exists(custom_strategies_path):
                for strategy in os.listdir(custom_strategies_path):
                    if search_term.lower() in strategy.lower():
                        strategy_path = os.path.join(custom_strategies_path, strategy)
                        if os.path.isdir(strategy_path):
                            with st.expander(f"🎯 {strategy}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    # README content
                                    readme_content = load_readme(strategy_path)
                                    if readme_content:
                                        st.markdown(readme_content, unsafe_allow_html=True)
                                    
                                    # Code section
                                    pine_code = load_pine_code(strategy_path)
                                    if pine_code:
                                        st.code(pine_code, language="pine")
                                    
                                    # # Mock visualization
                                    # fig = go.Figure()
                                    
                                    # # Add sample data - replace with actual strategy performance data
                                    # dates = [datetime.now() - timedelta(days=x) for x in range(100, 0, -1)]
                                    # values = [1000000 * (1 + i/100) for i in range(100)]  # Sample equity curve
                                    
                                    # fig.add_trace(go.Scatter(
                                    #     x=dates,
                                    #     y=values,
                                    #     mode='lines',
                                    #     name='Equity Curve',
                                    #     line=dict(color='#00ff00', width=2)
                                    # ))
                                    
                                    # fig.update_layout(
                                    #     title="Strategy Performance (Last 3 Years)",
                                    #     xaxis_title="Date",
                                    #     yaxis_title="Portfolio Value ($)",
                                    #     template="plotly_dark",
                                    #     showlegend=True,
                                    #     height=400
                                    # )
                                    
                                    # st.plotly_chart(fig, use_container_width=True)
                                
                                with col2:
                                    # Strategy metrics
                                    st.markdown("### 📊 Key Metrics")
                                    metrics_col1, metrics_col2 = st.columns(2)
                                    with metrics_col1:
                                        st.metric("Initial Capital", "$1,000,000")
                                        # st.metric("Win Rate", "65%")
                                    with metrics_col2:
                                        st.metric("Risk per Trade", "2%")
                                        # st.metric("Profit Factor", "1.8")
                                    
                                    # Notes section
                                    st.markdown("### 📝 Notes")
                                    notes = load_notes()
                                    current_note = notes.get("Strategies", {}).get(strategy, {}).get("content", "")
                                    
                                    note_input = st.text_area(
                                        "Add/Edit Note",
                                        value=current_note,
                                        key=f"note_{strategy}"
                                    )
                                    
                                    if st.button("Save Note", key=f"save_{strategy}"):
                                        save_note(strategy, note_input, "Strategies")
                                        st.success("Note saved successfully!")
    
    with tab2:
        st.info("TradingView indicators and strategies will be displayed here. Implementation pending based on TradingView API access.")

if __name__ == "__main__":
    main()