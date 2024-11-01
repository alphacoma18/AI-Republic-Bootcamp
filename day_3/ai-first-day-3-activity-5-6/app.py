import os
import openai
import streamlit as st
import base64
from streamlit_option_menu import option_menu

# Set up the page configuration
st.set_page_config(
    page_title="VerseForge - AI Lyrics Mixer",
    page_icon='day_3/ai-first-day-3-activity-5-6/images/logo.jpg',
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to set the background image
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{image_data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        backdrop-filter: brightness(0.7) blur(5px);
    }}
    /* Updated chat message styling */
    .stChatMessage {{
        width: 80%;
        margin: 1rem auto !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .stChatMessage div[data-testid="stMarkdownContainer"] {{
        color: #ffffff;
    }}
    /* Align user messages to the right */
    .stChatMessage.user-message {{
        background-color: rgba(30, 30, 40, 0.85) !important;
        margin-left: 20% !important;
    }}
    /* Align assistant messages to the left */
    .stChatMessage.assistant-message {{
        background-color: rgba(50, 50, 70, 0.85) !important;
        margin-right: 20% !important;
    }}
    /* Chat input container styling */
    .stChatInputContainer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background-color: rgba(27, 27, 27, 0.9);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }}
    /* Chat message container */
    [data-testid="stChatMessageContainer"] {{
        padding: 0.5rem;
        margin-bottom: 60px;  /* Space for fixed chat input */
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Custom CSS for enhanced styling
def load_custom_css():
    custom_css = """
    <style>
    :root {
        --primary-color: #262730;
        --secondary-color: #03a9f4;
        --background-color: #1b1b1b;
        --text-color: #ffffff;
        --accent-color: #dec960;
    }
    body {
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
    }
    .stSidebar {
        background-color: rgba(27, 27, 27, 0.8);
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background-color: var(--accent-color);
        color: var(--primary-color);
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--secondary-color);
        transform: scale(1.05);
    }
    /* Chat input styling */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
    }
    .stTextInput input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(222, 201, 96, 0.2);
    }
    /* Improve scrollbar appearance */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(222, 201, 96, 0.5);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(222, 201, 96, 0.7);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Main application class
class VerseForgeApp:
    def __init__(self):
        # Initialize session state variables
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'song_lyrics' not in st.session_state:
            st.session_state.song_lyrics = []
        if 'current_stage' not in st.session_state:
            st.session_state.current_stage = 'start'
        if 'total_songs' not in st.session_state:
            st.session_state.total_songs = 0

    def system_prompt(self):
        return """
You are Melodia, an AI music mixer specializing in combining multiple song lyrics into cohesive and meaningful mixed songs.

Your task is to guide the user through the lyric mixing process:
1. Ask how many songs they want to mix
2. Help them input lyrics for each song
3. Ask if they want to add any specific creative direction
4. Generate a mixed song that combines their inputs creatively

Be conversational, encouraging, and help users explore their musical creativity!
"""

    def chat_message(self, content, role='assistant'):
        # Add message to chat history
        st.session_state.chat_history.append({
            'role': role,
            'content': content
        })

        # Display message
        with st.chat_message(role):
            st.markdown(content)

    def get_ai_response(self, user_input):
        # System prompt for lyric generation
        system_prompt = """
<MusicMixerPrompt>
<Role>
You are Melodia, an AI music mixer specializing in combining multiple song lyrics into cohesive and meaningful mixed songs.
</Role>

<Instructions>
Your primary task is to analyze input lyrics from multiple songs and create a new set of lyrics that combines elements from all input songs while maintaining coherence and flow:

1. Analyze the input lyrics from multiple songs
2. Identify common themes, emotions, and styles
3. Create a new set of lyrics combining elements from all input songs
4. Ensure a clear verse-chorus-verse-chorus-bridge-chorus structure
5. Use poetic and engaging language
6. Avoid repetition and maintain variety
7. Incorporate elements that tie all songs together
8. Keep mixed lyrics concise (200-250 words)
</Instructions>
</MusicMixerPrompt>
        """

        # Generate mixed song
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        return response.choices[0].message.content

    def run(self):
        # Sidebar for API key and navigation
        with st.sidebar:
            st.image('day_3/ai-first-day-3-activity-5-6/images/logo.jpg')

            # API key input
            openai.api_key = st.text_input(
                'Enter OpenAI API token:',
                type='password',
                placeholder='Your API token here'
            )

            # Navigation menu
            options = option_menu(
                "VerseForge",
                ["Home", "Mix Songs", "About"],
                icons=['house', 'music-note', 'info-circle'],
                menu_icon="list",
                default_index=0,
                styles={
                    "icon": {"color": "#dec960"},
                    "nav-link-selected": {"background-color": "#262730"}
                }
            )

        # Main content area
        st.markdown("<h1 style='text-align:center; color:#dec960;'>VerseForge - AI Music Mixer</h1>", unsafe_allow_html=True)

        if options == "Home":
            st.markdown("""
            <div style='text-align:center; background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>
                <h3>Harmonize Multiple Songs into One</h3>
                <p>VerseForge combines AI technology with musical creativity to blend lyrics from various songs into a cohesive masterpiece.</p>
            </div>
            """, unsafe_allow_html=True)

        elif options == "About":
            st.markdown("""
            <div style='text-align:center; background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>
                <p>VerseForge is an AI-powered music mixing application created by Alpha Romer Coma.</p>
                <p>This project aims to push the boundaries of what's possible in music creation using artificial intelligence.</p>
            </div>
            """, unsafe_allow_html=True)

        elif options == "Mix Songs":
            # Chat-based interaction for song mixing
            chat_container = st.container()

            with chat_container:
                # Display chat history
                for message in st.session_state.chat_history:
                    with st.chat_message(message['role']):
                        st.markdown(message['content'])

            # User input
            user_input = st.chat_input("Let's mix some music!")

            if user_input:
                # User message
                self.chat_message(user_input, role='user')

                # AI conversation flow
                if st.session_state.current_stage == 'start':
                    self.chat_message("Hi there! I'm Melodia, your AI music mixer. How many songs would you like to mix today?")
                    st.session_state.current_stage = 'song_count'

                elif st.session_state.current_stage == 'song_count':
                    try:
                        total_songs = int(user_input)
                        if 2 <= total_songs <= 5:
                            st.session_state.total_songs = total_songs
                            st.session_state.song_lyrics = []
                            self.chat_message(f"Great! We'll mix {total_songs} songs. Please provide the lyrics for Song 1.")
                            st.session_state.current_stage = 'collecting_lyrics'
                        else:
                            self.chat_message("Please choose between 2 and 5 songs.")
                    except ValueError:
                        self.chat_message("Please enter a valid number between 2 and 5.")

                elif st.session_state.current_stage == 'collecting_lyrics':
                    st.session_state.song_lyrics.append(user_input)

                    if len(st.session_state.song_lyrics) < st.session_state.total_songs:
                        self.chat_message(f"Lyrics for Song {len(st.session_state.song_lyrics)} added. Please provide lyrics for Song {len(st.session_state.song_lyrics) + 1}.")
                    else:
                        self.chat_message("All song lyrics collected! Do you have any special creative direction or theme you'd like me to consider while mixing?")
                        st.session_state.current_stage = 'creative_direction'

                elif st.session_state.current_stage == 'creative_direction':
                    # Combine lyrics with creative direction
                    combined_input = "\n\n".join(st.session_state.song_lyrics) + f"\n\nCreative Direction: {user_input}"

                    # Generate mixed song
                    mixed_song = self.get_ai_response(combined_input)

                    # Display mixed song
                    self.chat_message("Here's your mixed song masterpiece!")
                    self.chat_message(mixed_song)

                    # Add download button
                    st.download_button(
                        label="Download Mixed Song",
                        data=mixed_song,
                        file_name="mixed_song.txt",
                        mime="text/plain"
                    )

                    # Reset for next mixing session
                    st.session_state.current_stage = 'start'
                    st.session_state.song_lyrics = []

# Main app execution
def main():
    # Set background and load custom CSS
    set_background("day_3/ai-first-day-3-activity-5-6/images/studio.jpg")
    load_custom_css()

    # Initialize and run the app
    app = VerseForgeApp()
    app.run()

if __name__ == "__main__":
    main()