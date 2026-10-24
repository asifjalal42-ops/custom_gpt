import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Custom ChatGPT AI Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #211d32;
        --muted: #77718f;
        --purple: #8057ff;
        --pink: #f05eb7;
        --line: #ece7f5;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 8%, rgba(202, 182, 255, .48), transparent 36%),
            radial-gradient(ellipse at 90% 18%, rgba(255, 211, 228, .35), transparent 32%),
            linear-gradient(135deg, #f3efff 0%, #fbf8fc 52%, #fffaf6 100%);
        color: var(--ink);
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Welcome panel */
    .welcome-card {
        max-width: 520px;
        margin: 0 auto;
        padding: 34px 38px 28px;
        border: 1px solid rgba(255,255,255,.92);
        border-radius: 34px;
        background: rgba(255,255,255,.78);
        box-shadow: 0 24px 80px rgba(69, 47, 105, .12);
        text-align: center;
        backdrop-filter: blur(18px);
    }
    .robot {
        font-size: 4.2rem;
        line-height: 1.2;
        margin: 0 0 22px;
        filter: drop-shadow(0 9px 10px rgba(124, 87, 255, .12));
    }
    .hero-title {
        font-size: clamp(2.25rem, 5vw, 3rem);
        font-weight: 800;
        line-height: 1.08;
        letter-spacing: -1.8px;
        color: var(--ink);
        margin: 0 0 14px;
    }
    .gradient-text {
        background: linear-gradient(100deg, #ff789f 5%, #ff9b7c 47%, #8558ff 95%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .hero-subtitle {
        color: var(--muted);
        font-size: 1.12rem;
        line-height: 1.65;
        margin: 0 auto 22px;
        max-width: 380px;
    }
    .feature-row {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 9px;
        margin: 0 0 26px;
    }
    .feature-pill {
        border: 1px solid #e6d2ff;
        border-radius: 999px;
        padding: 8px 14px;
        background: linear-gradient(100deg, #f1e8ff, #ffe7f3);
        color: #29233a;
        font-size: .88rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .key-label {
        text-align: left;
        font-size: .98rem;
        font-weight: 600;
        margin: 8px 0 8px;
        color: var(--ink);
    }
    .security-note {
        color: var(--muted);
        font-size: .84rem;
        line-height: 1.7;
        text-align: center;
        margin-top: 22px;
    }
    .security-note a {
        color: #8057ff;
        font-weight: 700;
        text-decoration: none;
    }

    /* Streamlit inputs and buttons */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        border: 1px solid #e8e5ef;
        border-radius: 13px;
        background: #f4f5f8;
        min-height: 48px;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #a58aff;
        box-shadow: 0 0 0 3px rgba(128,87,255,.12);
    }
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        min-height: 48px;
        border: 0;
        border-radius: 15px;
        color: white;
        font-weight: 700;
        background: linear-gradient(100deg, #8057ff 0%, #b65ce9 52%, #f05eb7 100%);
        box-shadow: 0 12px 25px rgba(197, 83, 195, .19);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 15px 28px rgba(197, 83, 195, .25);
        border: 0;
    }

    /* Chat workspace */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 18px 22px;
        border: 1px solid rgba(255,255,255,.9);
        border-radius: 22px;
        background: rgba(255,255,255,.78);
        box-shadow: 0 12px 35px rgba(69,47,105,.08);
        margin-bottom: 22px;
    }
    .brand {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -.3px;
    }
    .brand span {
        background: linear-gradient(100deg, #ff789f, #8558ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .online-pill {
        color: #4f8a69;
        background: #e9f8ef;
        border: 1px solid #ccebd7;
        padding: 6px 11px;
        border-radius: 999px;
        font-size: .8rem;
        font-weight: 700;
        white-space: nowrap;
    }
    .workspace-title {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -.8px;
        margin-bottom: 3px;
    }
    .workspace-caption {
        color: var(--muted);
        margin-bottom: 22px;
    }
    div[data-testid="stChatMessage"] {
        border: 1px solid rgba(232,225,245,.8);
        border-radius: 18px;
        background: rgba(255,255,255,.72);
        padding: 12px 15px;
        box-shadow: 0 5px 18px rgba(69,47,105,.035);
    }
    div[data-testid="stChatInput"] {
        border-radius: 18px;
    }
    .small-caption {
        font-size: .82rem;
        color: var(--muted);
    }

    @media (max-width: 600px) {
        .block-container { padding: 1rem .65rem 2rem; }
        .welcome-card { padding: 27px 20px 22px; border-radius: 27px; }
        .hero-title { letter-spacing: -1.2px; }
        .app-header { padding: 14px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------
defaults = {
    "api_key": "",
    "unlocked": False,
    "messages": [],
    "system_prompt": "You are a helpful, clear, and thoughtful assistant.",
    "model_name": "gpt-5.2",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_chat():
    st.session_state.messages = []


# ---------------------------------------------------------
# Welcome / API key screen
# ---------------------------------------------------------
if not st.session_state.unlocked:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="robot">🤖</div>
            <h1 class="hero-title">Welcome to<br>your <span class="gradient-text">Custom<br>ChatGPT</span></h1>
            <p class="hero-subtitle">
                Plug in your OpenAI API key to unlock your personal AI studio.
            </p>
            <div class="feature-row">
                <span class="feature-pill">⚡ Streaming-ready</span>
                <span class="feature-pill">🗂️ Saved chats</span>
                <span class="feature-pill">🎭 Custom persona</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    # Keep the form narrow and centered, similar to the reference design.
    _, center_col, _ = st.columns([1, 2.4, 1])
    with center_col:
        st.markdown('<div class="key-label">🔑 OpenAI API key</div>', unsafe_allow_html=True)
        with st.form("unlock_form", clear_on_submit=False):
            entered_key = st.text_input(
                "OpenAI API key",
                type="password",
                placeholder="sk-...",
                label_visibility="collapsed",
            )
            unlock_clicked = st.form_submit_button("🚀 Unlock the magic")

        if unlock_clicked:
            if not entered_key.strip():
                st.error("Please enter your OpenAI API key.")
            else:
                # Key is kept in this Streamlit session only; it is not written to disk.
                st.session_state.api_key = entered_key.strip()
                st.session_state.unlocked = True
                st.rerun()

        st.markdown(
            """
            <div class="security-note">
                🔒 Your key is held in this app session and is not written to a file by this code.<br>
                For production deployments, use server-side secrets and avoid sharing your session.<br>
                Need one? <a href="https://platform.openai.com/api-keys" target="_blank">Get an API key ↗</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# Chat workspace
# ---------------------------------------------------------
else:
    with st.sidebar:
        st.markdown("## 🎭 Assistant persona")
        st.session_state.system_prompt = st.text_area(
            "System role",
            value=st.session_state.system_prompt,
            height=130,
            help="Describe the tone, role, and behavior you want from the assistant.",
        )
        st.session_state.model_name = st.selectbox(
            "Model",
            options=["gpt-5.2", "gpt-4.1", "gpt-4.1-mini"],
            index=["gpt-5.2", "gpt-4.1", "gpt-4.1-mini"].index(
                st.session_state.model_name
            ) if st.session_state.model_name in ["gpt-5.2", "gpt-4.1", "gpt-4.1-mini"] else 0,
        )
        if st.button("🧹 Clear conversation"):
            reset_chat()
            st.rerun()
        if st.button("🔐 Lock and return"):
            st.session_state.api_key = ""
            st.session_state.unlocked = False
            reset_chat()
            st.rerun()
        st.caption("Your API key is not saved to a local file by this app.")

    st.markdown(
        """
        <div class="app-header">
            <div class="brand">🤖 Custom <span>ChatGPT</span> Studio</div>
            <div class="online-pill">● Ready to chat</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="workspace-title">Your AI workspace ✨</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="workspace-caption">Ask a question, explore an idea, or work through a problem.</div>',
        unsafe_allow_html=True,
    )

    # Render previous messages.
    for message in st.session_state.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    prompt = st.chat_input("Message your assistant…")

    if prompt:
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            model = ChatOpenAI(
                model=st.session_state.model_name,
                api_key=st.session_state.api_key,
                streaming=True,
            )
            model_messages = [
                SystemMessage(
                    content=st.session_state.system_prompt.strip()
                    or "You are a helpful assistant."
                ),
                *st.session_state.messages,
            ]

            with st.chat_message("assistant"):
                response_text = st.write_stream(
                    model.stream(model_messages)
                )

            st.session_state.messages.append(
                AIMessage(content=str(response_text))
            )

        except Exception as exc:
            # Keep the user's prompt, but do not store an error as an AI response.
            st.error(
                "The request could not be completed. Check your API key, model access, "
                f"billing, and network connection. Details: {exc}"
            )
