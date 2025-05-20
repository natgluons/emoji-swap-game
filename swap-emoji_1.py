import streamlit as st
import random
import textwrap

EMOJIS = ['❤️', '💀', '🤖', '👽']
EMOJI_COLORS = {
    '❤️': "#FFCDD2",
    '💀': "#FFF9C4",
    '🤖': "#BBDEFB",
    '👽': "#C8E6C9"
}

# Initialize session state
if 'correct_order' not in st.session_state:
    st.session_state.correct_order = random.sample(EMOJIS, len(EMOJIS))
    st.session_state.current_order = random.sample(EMOJIS, len(EMOJIS))
    st.session_state.attempts = 0
    st.session_state.selected = []

def create_emoji_container(emoji, selected=False):
    color = EMOJI_COLORS[emoji]
    border = "3px solid #00FF00" if selected else "1px solid transparent"
    return f'''
    <div style="
        background-color: {color};
        border-radius: 8px;
        border: {border};
        padding: 10px;
        height: 70px;
        width: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
    ">
        {emoji}
    </div>
    '''.strip()

def handle_click(index):
    if index in st.session_state.selected:
        st.session_state.selected.remove(index)
    else:
        st.session_state.selected.append(index)
    
    if len(st.session_state.selected) == 2:
        i1, i2 = st.session_state.selected
        st.session_state.current_order[i1], st.session_state.current_order[i2] = (
            st.session_state.current_order[i2], st.session_state.current_order[i1]
        )
        st.session_state.attempts += 1
        st.session_state.selected = []
        st.rerun()

def main():
    st.title("Swap Emoji Guessing Game")
    st.write("Click to select and swap them into the correct order.")

    # Custom CSS
    st.markdown("""
    <style>
    .emoji-container {
        width: 100vw;
        overflow-x: auto;
        white-space: nowrap;
        padding-bottom: 10px;
    }
    .emoji-grid {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        width: 100%;
        gap: 5px;
        padding-right: 10px;
    }
    .emoji-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        width: 70px;
        flex-shrink: 0;
    }
    div[data-testid="stButton"] button span {
        display: none;
    }
    div[data-testid="stButton"] button {
        height: 0;
        padding: 0;
        min-height: 32px;
        width: 70px !important;
    }
    /* Restart button specific styles */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: white !important;
        color: #143c2c !important;
        font-weight: bold !important;
        border: 2px solid #143c2c !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #143c2c !important;
        color: white !important;
    }
    @media (max-width: 640px) {
        .stHorizontalBlock {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
        }
        .stHorizontalBlock > div {
            min-width: 70px !important;
            width: 70px !important;
            flex-shrink: 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Create columns for each emoji+button pair
    cols = st.columns(4)
    for i, col in enumerate(cols):
        emoji = st.session_state.current_order[i]
        selected = i in st.session_state.selected
        with col:
            st.markdown(create_emoji_container(emoji, selected), unsafe_allow_html=True)
            label = "Deselect" if selected else "Select"
            if st.button(label, key=f"btn_{i}", use_container_width=True):
                handle_click(i)

    # Game status
    correct = sum(st.session_state.current_order[i] == st.session_state.correct_order[i] for i in range(4))
    st.write(f"Correct positions: {correct}/4")
    st.write(f"Attempts: {st.session_state.attempts}")

    if correct == 4:
        st.success(f"Congratulations! You solved it in {st.session_state.attempts} swaps.")
        st.write("Secret order: " + " ".join(st.session_state.correct_order))

    # Restart button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Restart Game", type="primary", use_container_width=True):
            st.session_state.correct_order = random.sample(EMOJIS, len(EMOJIS))
            st.session_state.current_order = random.sample(EMOJIS, len(EMOJIS))
            st.session_state.attempts = 0
            st.session_state.selected = []
            st.rerun()

if __name__ == "__main__":
    main()
