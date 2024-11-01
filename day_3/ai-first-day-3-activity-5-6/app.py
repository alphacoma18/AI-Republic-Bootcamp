import os
import openai
import streamlit as st
from streamlit_option_menu import option_menu
import base64

# Set up the page configuration
st.set_page_config(
    page_title="VerseForge - AI Lyrics Mixer",
    page_icon='images/logo.jpg',
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
        background-image: url("data:image/png;base64,{image_data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Apply the background image
set_background("images/studio.jpg")

# Custom CSS for enhanced styling
custom_css = """
<style>
    /* Global Styles */
    :root {
        --primary-color: #ff006e;
        --secondary-color: #03a9f4;
        --background-color: #1b1b1b;
        --text-color: #ffffff;
        --accent-color: #dec960;
    }

    body {
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
    }

    /* Sidebar Styles */
    .streamlit-expanderHeader {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--primary-color);
    }

    .stSidebar {
        background-color: var(--background-color);
    }

    .stSidebar .sidebar-content {
        padding: 1rem;
    }

    /* Menu Styles */
    .nav-link-selected {
        background-color: var(--secondary-color);
        color: var(--background-color);
    }

    /* Button Styles */
    .stButton {
        background-color: var(--primary-color);
        color: var(--background-color);
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton:hover {
        background-color: var(--secondary-color);
    }

    /* Input Styles */
    .stTextInput > div > div > input {
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 0.25rem;
        border: 1px solid var(--accent-color);
    }

    /* Text Area Styles */
    .stTextArea > div > div > textarea {
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 0.25rem;
        border: 1px solid var(--accent-color);
    }

    /* Download Button Styles */
    .stDownloadButton > button {
        background-color: var(--secondary-color);
        color: var(--background-color);
        padding: 0.5rem 1rem;
        font-size: 1rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background-color: var(--primary-color);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image('images/logo.jpg')
    
    # API key input
    api_key_container = st.empty()
    openai.api_key = api_key_container.text_input(
        'Enter OpenAI API token:',
        type='password',
        placeholder='Your API token here'
    )
    
    # API key validation
    if not openai.api_key:
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        try:
            openai.ChatCompletion.create(
                model="gpt-4-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            st.success('Ready to mix some melodies!', icon='🎵')
        except openai.error.AuthenticationError:
            st.error('Invalid API key. Please check your token and try again.', icon='🚫')
        except openai.error.APIError as e:
            st.error(f'OpenAI API error: {str(e)}', icon='❌')
        except Exception as e:
            st.error(f'An error occurred: {str(e)}', icon='⚠️')

# Menu configuration
options = option_menu(
    "Dashboard", 
    ["Home", "About Us", "Mix Songs"],
    icons = ['house', 'info-circle', 'music'],
    menu_icon = "list", 
    default_index = 0,
    styles = {
        "icon": {"color": "#dec960", "font-size": "20px"},
        "nav-link": {"font-size": "17px", "text-align": "left", "margin": "5px", "--hover-color": "#262730"},
        "nav-link-selected": {"background-color": "#262730"}          
    })

if options == "Home":
    # Home content
    st.markdown("<h1 style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>VerseForge - AI Music Mixer</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>
            <h3>Harmonize Multiple Songs into One</h3>
            <p>VerseForge combines AI technology with musical creativity to blend lyrics from various songs into a cohesive masterpiece.</p>
        </div>
    """, unsafe_allow_html=True)

elif options == "About Us":
    # About Us content
    st.markdown("<h1 style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>About Us</h1><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>
            <p>VerseForge is an AI-powered music mixing application created by Alpha Romer Coma.</p>
            <p>This project aims to push the boundaries of what's possible in music creation using artificial intelligence.</p>
        </div>
    """, unsafe_allow_html=True)

elif options == "Mix Songs":
    # Mix Songs content
    st.markdown("<h1 style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px;'>Create Your Mixed Masterpiece</h1>", unsafe_allow_html=True)
    
    # Input fields for multiple song lyrics
    num_songs = st.number_input(
        "Number of songs to mix:",
        min_value=2,
        max_value=5,
        value=2,
        label_visibility="visible"
    )
    
    lyrics_inputs = []
    for i in range(num_songs):
        lyrics_input = st.text_area(
            f"Lyrics for Song {i+1}:",
            height=150,
            label_visibility="visible"
        )
        lyrics_inputs.append(lyrics_input)

    # System prompt for AI model
    system_prompt = """
<MusicMixerPrompt>
<Role>
You are Melodia, an AI music mixer specializing in combining multiple song lyrics into cohesive and meaningful mixed songs.
</Role>

<Instructions>
Your primary task is to analyze input lyrics from multiple songs and create a new set of lyrics that combines elements from all input songs while maintaining coherence and flow. Follow these steps:

1. Analyze the input lyrics from multiple songs.
2. Identify common themes, emotions, and styles across the songs.
3. Create a new set of lyrics that combines elements from all input songs.
4. Ensure the resulting lyrics have a clear structure (verse-chorus-verse-chorus-bridge-chorus).
5. Use language that is poetic and engaging, suitable for a popular song.
6. Avoid repetition and maintain variety throughout the mixed lyrics.
7. If possible, incorporate elements that tie all songs together (e.g., similar imagery or metaphors).
8. Keep the mixed lyrics concise, aiming for a total of about 200-250 words.

Present your response in the format of a complete song with verses and choruses clearly marked.
</Instructions>

<Context>
As an AI music mixer, you operate in a creative environment where artistic expression meets technical skill. Your mixed lyrics will be used by musicians, producers, and music enthusiasts seeking innovative ways to combine different musical styles and themes. The goal is to create something unique yet familiar, blending the essence of multiple songs into a single, coherent piece.
</Context>

<Constraints>
1. Maintain a balance between creativity and coherence in the mixed lyrics.
2. Ensure all elements of the mixed lyrics align with the identified common themes and styles.
3. Avoid copyright infringement by transforming original lyrics sufficiently.
4. Keep the mixed lyrics suitable for a general audience, avoiding explicit content.
5. Maintain consistency in tone and style throughout the mixed song.
6. Do not introduce completely new themes or ideas not present in the original songs.
7. Ensure the mixed lyrics flow naturally and maintain musicality.
</Constraints>

<Examples>
<!-- Example 1 -->
<Example>
    <InputLyrics>
        Song 1: "Yesterday" by The Beatles
        Song 2: "Stairway to Heaven" by Led Zeppelin
    </InputLyrics>
    <ExpectedOutput>
        Verse 1:
        In yesterday's misty mountains high
        Where shadows play, I hear her sigh
        The wind whispers secrets, echoes of the past
        A melancholy tune that forever lasts

        Chorus:
        Oh, my love, she's gone away
        Left me standing here to face the day
        With memories that never fade
        And a heart that's lost its way

        Verse 2:
        There's a lady who's sure all that glitters is gold
        And she's buying a stairway to heaven
        When she gets there she knows, if the stores are all closed
        With a word she can get what she came for

        Chorus:
        Oh, my love, she's gone away
        Left me standing here to face the day
        With memories that never fade
        And a heart that's lost its way

        Bridge:
        Yes, there are two paths you can go by
        But in the long run, there's still time to change the road you're on
        Your head is humming, and your feet are cold
        You've been a long time on the road

        Chorus:
        Oh, my love, she's gone away
        Left me standing here to face the day
        With memories that never fade
        And a heart that's lost its way
    </ExpectedOutput>
</Example>
</Examples>
</MusicMixerPrompt>
    """

    # Mix Songs button
    mix_button = st.button("Mix Songs")
    
    if mix_button:
        # Combine input lyrics
        combined_lyrics = "\n\n".join(lyrics_inputs)
        
        # Generate mixed song using AI model
        response = openai.ChatCompletion.create(
            model="gpt-4-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Combine these lyrics into a cohesive mixed song:\n\n{combined_lyrics}"}
            ]
        )
        
        # Display the mixed song
        st.success("Your mixed masterpiece is ready!")
        st.markdown(response.choices[0].message.content)

        # Add download button for the mixed song
        st.download_button(
            label="Download Your Mixed Song",
            data=response.choices[0].message.content,
            file_name="mixed_song.txt",
            mime="text/plain"
        )

# Footer
st.markdown("""
<div style='background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; position: fixed; bottom: 0; left: 0; right: 0; text-align: center;'>
    <p>&copy; 2024 Alpha Romer Coma. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
