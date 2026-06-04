import streamlit as st
import time
import random

# 1. Page Configuration
st.set_page_config(page_title="Cuber's Station Pro", page_icon="🧩", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .title-text { font-size: 42px; font-weight: 800; color: #FF5722; margin-bottom: 5px; }
    .timer-display { font-family: 'Courier New', Courier, monospace; font-size: 72px; font-weight: bold; color: #1E88E5; background-color: #1E1E1E; padding: 10px 30px; border-radius: 12px; display: inline-block; margin: 10px 0px; text-align: center; min-width: 300px; border: 2px solid #FF5722; }
    
    /* Algorithm box dark mode styling */
    .algo-box { 
        background-color: #1E1E1E; 
        color: #00E676; 
        padding: 18px; 
        border-radius: 10px; 
        font-family: 'Courier New', monospace; 
        font-size: 20px; 
        font-weight: bold;
        border-left: 6px solid #FF5722; 
        letter-spacing: 2px;
        margin-bottom: 15px; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Helper Functions for Scrambles
def generate_scramble(cube_type):
    moves3x3 = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'", "R2", "L2", "U2", "D2", "F2", "B2"]
    moves4x4 = moves3x3 + ["Rw", "Lw", "Uw", "Dw", "Fw", "Bw", "Rw'", "Lw'", "Uw'", "Dw'", "Fw'", "Bw'", "Rw2", "Lw2", "Uw2", "Dw2", "Fw2", "Bw2"]
    
    scramble = []
    length = 20 if cube_type == "3x3" else 40
    available_moves = moves3x3 if cube_type == "3x3" else moves4x4
    
    last_move = ""
    for _ in range(length):
        move = random.choice(available_moves)
        while move[0] == last_move:
            move = random.choice(available_moves)
        scramble.append(move)
        last_move = move[0]
        
    return " ".join(scramble)

# 3. Fidget Switchboard Logic (State Management)
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "⏱️ Arena"
if 'solve_history' not in st.session_state:
    st.session_state.solve_history = []

# Sidebar Fidget Button Layout
with st.sidebar:
    st.markdown("## 🕹️ Fidget Control Deck")
    st.write("Click a tactical box to flip the station module:")
    
    if st.button("⏱️ Practice Arena", use_container_width=True, type="primary" if st.session_state.active_tab == "⏱️ Arena" else "secondary"):
        st.session_state.active_tab = "⏱️ Arena"
        st.rerun()
        
    if st.button("🧠 3x3 CFOP Guide", use_container_width=True, type="primary" if st.session_state.active_tab == "🧠 CFOP" else "secondary"):
        st.session_state.active_tab = "🧠 CFOP"
        st.rerun()
        
    if st.button("⚠️ 4x4 Parity Rescue", use_container_width=True, type="primary" if st.session_state.active_tab == "⚠️ Parity" else "secondary"):
        st.session_state.active_tab = "⚠️ Parity"
        st.rerun()
        
    if st.button("🎨 Visual Pattern Lab", use_container_width=True, type="primary" if st.session_state.active_tab == "🎨 Patterns" else "secondary"):
        st.session_state.active_tab = "🎨 Patterns"
        st.rerun()

    st.markdown("---")
    st.caption(f"Active Module: {st.session_state.active_tab}")

# Main Header
st.markdown('<p class="title-text">🎲 Cuber\'s Station Pro</p>', unsafe_allow_html=True)
st.write("Production-ready elite speedcubing layout dashboard.")
st.markdown("---")

# ==========================================
# MODULE 1: PRACTICE ARENA
# ==========================================
if st.session_state.active_tab == "⏱️ Arena":
    st.markdown("### ⚡ Live Millisecond Practice Station")
    
    col_config1, col_config2 = st.columns(2)
    with col_config1:
        cube_selection = st.radio("Select Puzzle Session:", ["3x3 Cube", "4x4 Cube"], horizontal=True)
    
    if 'current_scramble' not in st.session_state:
        st.session_state.current_scramble = generate_scramble("3x3")
    if 'scramble_type' not in st.session_state:
        st.session_state.scramble_type = "3x3 Cube"

    if st.session_state.scramble_type != cube_selection:
        st.session_state.scramble_type = cube_selection
        st.session_state.current_scramble = generate_scramble("3x3" if "3x3" in cube_selection else "4x4")

    st.markdown("#### 🔄 Practice Scramble Sequence:")
    st.info(st.session_state.current_scramble)
    
    if st.button("🔄 Generate Fresh Scramble"):
        st.session_state.current_scramble = generate_scramble("3x3" if "3x3" in cube_selection else "4x4")
        st.rerun()

    st.markdown("---")
    
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'final_time' not in st.session_state:
        st.session_state.final_time = 0.000

    col_btn1, col_btn2, _ = st.columns([1, 1, 2])
    timer_placeholder = st.empty()

    with col_btn1:
        if not st.session_state.timer_running:
            if st.button("▶️ START TIMER", use_container_width=True, type="primary"):
                st.session_state.timer_running = True
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            if st.button("⏹️ STOP TIMER", use_container_width=True, type="secondary"):
                stop_timestamp = time.time()
                st.session_state.timer_running = False
                recorded_time = stop_timestamp - st.session_state.start_time
                st.session_state.final_time = recorded_time
                
                # Save to history list
                st.session_state.solve_history.append(round(recorded_time, 3))
                
                st.session_state.current_scramble = generate_scramble("3x3" if "3x3" in cube_selection else "4x4")
                st.rerun()

    with col_btn2:
        if st.button("🗑️ Reset Session Stats", use_container_width=True):
            st.session_state.final_time = 0.000
            st.session_state.timer_running = False
            st.session_state.solve_history = []
            st.rerun()

    if st.session_state.timer_running:
        while st.session_state.timer_running:
            live_elapsed = time.time() - st.session_state.start_time
            timer_placeholder.markdown(f'<div class="timer-display">{live_elapsed:.3f}s</div>', unsafe_allow_html=True)
    else:
        timer_placeholder.markdown(f'<div class="timer-display">{st.session_state.final_time:.3f}s</div>', unsafe_allow_html=True)

    # HISTORY AND STATISTICS ARRAYS
    st.markdown("---")
    col_hist, col_stats = st.columns(2)
    
    with col_hist:
        st.markdown("#### 📜 Session History")
        if len(st.session_state.solve_history) == 0:
            st.write("No solves recorded yet for this session.")
        else:
            # Display history in reverse so newest is at top
            for idx, solve in enumerate(reversed(st.session_state.solve_history)):
                st.write(f"Solve {len(st.session_state.solve_history) - idx}: **{solve:.3f}s**")

    with col_stats:
        st.markdown("#### 📊 Speed Metrics")
        if len(st.session_state.solve_history) > 0:
            st.metric("Best Solve", f"{min(st.session_state.solve_history):.3f}s")
            
            # Calculate Average of Last 5 (Ao5) if enough scores exist
            if len(st.session_state.solve_history) >= 5:
                last_five = st.session_state.solve_history[-5:]
                # Traditional Ao5 removes best and worst scores
                last_five.remove(max(last_five))
                last_five.remove(min(last_five))
                ao5 = sum(last_five) / 3
                st.metric("Current Ao5 (Avg of 5)", f"{ao5:.3f}s")
            else:
                st.info("Record at least 5 solves to compute your official competitive Ao5!")
        else:
            st.write("Awaiting practice completion data.")

# ==========================================
# MODULE 2: 3x3 CFOP GUIDE
# ==========================================
elif st.session_state.active_tab == "🧠 CFOP":
    st.markdown("### 🧠 Advanced 3x3 CFOP Reference Engine")
    
    cfop_col1, cfop_col2 = st.columns(2)
    with cfop_col1:
        st.markdown("#### 🟡 Essential OLL (Orientation)")
        st.markdown("**Cross Case 1 (Sune):**")
        st.markdown('<div class="algo-box">R U R\' U R U2 R\'</div>', unsafe_allow_html=True)
        st.markdown("**Cross Case 2 (Anti-Sune):**")
        st.markdown('<div class="algo-box">R U2 R\' U\' R U\' R\'</div>', unsafe_allow_html=True)
    
    with cfop_col2:
        st.markdown("#### 🟢 Crucial PLL (Permutation)")
        st.markdown("**T-Permutation:**")
        st.markdown('<div class="algo-box">R U R\' U\' R\' F R2 U\' R\' U\' R U R\' F\'</div>', unsafe_allow_html=True)
        st.markdown("**U-Permutation:**")
        st.markdown('<div class="algo-box">R U\' R U R U R U\' R\' U\' R2</div>', unsafe_allow_html=True)

# ==========================================
# MODULE 3: 4x4 PARITY RESCUE
# ==========================================
elif st.session_state.active_tab == "⚠️ Parity":
    st.markdown("### ⚠️ 4x4 Parity Emergency Handling")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.error("🚨 Case 1: OLL Parity (One Flipped Edge Pair)")
        st.markdown('<div class="algo-box">Rw2 B2 U2 Lw U2 Rw\' U2 Rw U2 F2 Rw F2 Lw\' B2 Rw2</div>', unsafe_allow_html=True)
    with col_p2:
        st.error("🚨 Case 2: PLL Parity (Opposite Edges Swapped)")
        st.markdown('<div class="algo-box">r2 U2 r2 Uw2 r2 uw2</div>', unsafe_allow_html=True)

# ==========================================
# MODULE 4: PATTERN LAB
# ==========================================
elif st.session_state.active_tab == "🎨 Patterns":
    st.markdown("### 🎨 Desk Show-Off Pattern Laboratory")
    
    pattern_choice = st.selectbox(
        "Choose a Pattern Structure:", 
        [
            "Anaconda (The Serpent Line)", 
            "Cube-in-a-Cube", 
            "Cube-in-a-Cube-in-a-Cube (Triple Nested Box)", 
            "Six-Spot Pattern (All Centers Swapped)", 
            "Classic Checkerboard Matrix"
        ]
    )
    
    st.markdown("#### 🛠️ Execution Algorithm:")
    if "Anaconda" in pattern_choice:
        st.markdown('<div class="algo-box">L U B U\' R L\' B R\' F B\' D R D\' F\'</div>', unsafe_allow_html=True)
    elif "Cube-in-a-Cube" in pattern_choice and "Triple" not in pattern_choice:
        st.markdown('<div class="algo-box">F L F U\' R U F2 L2 U\' L\' B D\' B\' L2 U</div>', unsafe_allow_html=True)
    elif "Triple Nested" in pattern_choice:
        st.markdown('<div class="algo-box">U\' L\' U\' F\' R2 B\' R F U B2 U B\' L U\' F U R F\'</div>', unsafe_allow_html=True)
    elif "Six-Spot" in pattern_choice:
        st.markdown('<div class="algo-box">U D\' R L\' F B\' U D\'</div>', unsafe_allow_html=True)
    elif "Checkerboard" in pattern_choice:
        st.markdown('<div class="algo-box">R2 L2 U2 D2 F2 B2</div>', unsafe_allow_html=True)