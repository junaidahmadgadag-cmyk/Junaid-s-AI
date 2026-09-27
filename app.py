import streamlit as st
from react_agent import ReactAgent


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Junaid AI",
    page_icon="🤖",
    layout="wide"
)


# ==============================
# SESSION STATE
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==============================
# AI AGENT
# ==============================

@st.cache_resource
def get_agent():
    return ReactAgent()


try:
    agent = get_agent()
    agent_ready = True
    agent_error = None

except Exception as e:
    agent = None
    agent_ready = False
    agent_error = str(e)


# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.markdown("# 🤖 Junaid's AI")

    st.caption("Powered by Gemini + LangChain")

    st.divider()

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### Workspace")

    st.write("🏠 Home")
    st.write("💬 Chat History")
    st.write("⚙️ Settings")

    st.divider()

    st.markdown("### Features")

    st.write("🔎 Web Search")
    st.write("🤖 AI Agent")
    st.write("✨ Gemini")
    st.write("🔗 LangChain")

    st.divider()

    if agent_ready:
        st.success("● Agent Online")
    else:
        st.error("● Agent Offline")


# ==============================
# MAIN HEADER
# ==============================

st.markdown(
    """
    <div style="text-align:center; padding:30px 10px 10px 10px;">
        <div style="font-size:60px;">🤖</div>
        <h1>Welcome to <span style="color:#6c7cff;">Junaid AI</span></h1>
        <p style="color:#8b95a7;">
            Your intelligent AI assistant powered by Gemini and LangChain.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==============================
# AGENT STATUS
# ==============================

if agent_ready:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
            margin:10px auto 25px auto;
            border-radius:12px;
            background:#0d1917;
            color:#42e6a0;
            max-width:650px;
        ">
            🟢 AI Agent is ready
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.error("AI Agent could not start.")

    st.code(agent_error)

    st.stop()


# ==============================
# WELCOME SUGGESTIONS
# ==============================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div style="
            max-width:700px;
            margin:auto;
            padding:20px;
            border:1px solid #26344a;
            border-radius:18px;
            background:#0d141f;
        ">

        <h4 style="text-align:center;">
            Try asking me...
        </h4>

        <p>💻 What is Python?</p>

        <p>🧠 Explain machine learning</p>

        <p>🌐 Search for the latest AI news</p>

        <p>🔗 How does LangChain work?</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================
# CHAT HISTORY
# ==============================

for message in st.session_state.messages:

    if message["role"] == "user":
        avatar = "👤"
    else:
        avatar = "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# ==============================
# CHAT INPUT
# ==============================

user_input = st.chat_input(
    "Ask Junaid AI anything..."
)


# ==============================
# PROCESS USER MESSAGE
# ==============================

if user_input:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(user_input)


    # AI message
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        # Thinking indicator
        thinking = st.empty()

        thinking.markdown(
            """
            <div style="
                display:inline-block;
                padding:10px 15px;
                border-radius:12px;
                background:#111a29;
                color:#8b95a7;
            ">
                ● ● ● &nbsp; Thinking...
            </div>
            """,
            unsafe_allow_html=True
        )

        try:

            response = agent.run(user_input)

        except Exception as e:

            response = (
                "⚠️ Something went wrong.\n\n"
                + str(e)
            )

        # Remove thinking indicator
        thinking.empty()

        # Show response
        st.markdown(response)


    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ==============================
# FOOTER
# ==============================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#596579;
        font-size:11px;
        padding:25px;
    ">
        Junaid AI • Gemini • LangChain
    </div>
    """,
    unsafe_allow_html=True
)