import streamlit as st
import random

EMOJIS = ['❤️', '💀', '🤖', '👽']
# Fixed colors for each emoji type
EMOJI_COLORS = {
    '❤️': "#FFCDD2",  # Soft red
    '💀': "#FFF9C4",  # Soft yellow 
    '🤖': "#BBDEFB",  # Soft blue
    '👽': "#C8E6C9"   # Soft green
}

# Initialize session state variables
if 'correct_order' not in st.session_state:
    st.session_state.correct_order = random.sample(EMOJIS, len(EMOJIS))
    st.session_state.current_order = random.sample(EMOJIS, len(EMOJIS))
    st.session_state.attempts = 0
    st.session_state.selected = []  # List to track selected emojis
    st.session_state.just_swapped = False

def create_emoji_container(emoji, selected=False):
    """Create HTML for an emoji container with appropriate background color"""
    color = EMOJI_COLORS[emoji]
    border = "3px solid #00FF00" if selected else "1px solid transparent"
    
    return f"""
    <div style="
        background-color: {color};
        border-radius: 8px;
        border: {border};
        padding: 10px;
        height: 120px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 64px;
        margin-bottom: 8px;
    ">
        {emoji}
    </div>
    """

def main():
    st.title("Swap Emoji Guessing Game")
    st.write("Click emojis to select and swap them. Selected emojis are outlined in green.")

    # Create a row of emoji containers
    cols = st.columns(4)
    for i, col in enumerate(cols):
        emoji = st.session_state.current_order[i]
        selected = i in st.session_state.selected
        
        # Display the emoji in a styled container
        col.markdown(create_emoji_container(emoji, selected), unsafe_allow_html=True)
        
        # Add a button below - use CSS to hide the label instead of label_visibility
        button_label = "Select" if not selected else "Deselect"
        
        # Add custom CSS to hide the button text but keep it accessible
        col.markdown(
            """
            <style>
            div[data-testid="stButton"] button span {
                display: none;
            }
            div[data-testid="stButton"] button {
                height: 0;
                padding: 0;
                min-height: 32px;
                width: 100%;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        if col.button(button_label, key=f"button_{i}"):
            handle_click(i)

    # Display game status
    correct_count = sum(
        st.session_state.current_order[i] == st.session_state.correct_order[i] for i in range(4)
    )
    st.write(f"Correct positions: {correct_count}/4")
    st.write(f"Attempts: {st.session_state.attempts}")

    if correct_count == 4:
        st.success(f"Congratulations! You solved it in {st.session_state.attempts} swaps.")
        st.write(f"Secret order: {' '.join(st.session_state.correct_order)}")

    # Add restart button in the middle with green text
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <style>
            div[data-testid="stButton"] > button[kind="primary"] {
                background-color: white !important;
                color: #143c2c !important;
                font-weight: bold !important;
                border: 2px solid #143c2c !important;
            }
            div[data-testid="stButton"] > button[kind="primary"]:hover {
                background-color: #143c2c !important;
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        if st.button("Restart Game", type="primary", use_container_width=True):
            st.session_state.correct_order = random.sample(EMOJIS, len(EMOJIS))
            st.session_state.current_order = random.sample(EMOJIS, len(EMOJIS))
            st.session_state.attempts = 0
            st.session_state.selected = []
            st.session_state.just_swapped = False
            st.rerun()

def handle_click(index):
    """Handle clicks on emoji buttons"""
    # Check if this index is already selected
    if index in st.session_state.selected:
        st.session_state.selected.remove(index)
    else:
        # Add to selection
        st.session_state.selected.append(index)
        
    # If we have 2 selected, swap them immediately
    if len(st.session_state.selected) == 2:
        i1, i2 = st.session_state.selected
        # Swap the emojis
        st.session_state.current_order[i1], st.session_state.current_order[i2] = (
            st.session_state.current_order[i2], st.session_state.current_order[i1]
        )
        st.session_state.attempts += 1
        # Clear the selection after swapping
        st.session_state.selected = []
        # Force a rerun to show the updated state immediately
        st.rerun()

if __name__ == "__main__":
    main()