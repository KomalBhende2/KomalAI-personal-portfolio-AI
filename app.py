from dotenv import load_dotenv
load_dotenv()

import os
import json
import streamlit as st
from utils.retriever import get_retriever
from utils.chatbot import get_chatbot_chain

st.set_page_config(
    page_title="KomalAI",
    page_icon="👩‍💻",
    layout="centered"
)

st.title("KomalAI - Komal's Portfolio AI")
st.caption("Ask me about Komal's skills, projects, experience, education, or certifications.")

def parse_bot_response(raw_answer: str) -> str:
    try:
        cleaned = raw_answer.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data       = json.loads(cleaned)
        status     = data.get("status", "")
        answer     = data.get("answer", "")
        intent     = data.get("intent", "")
        payload    = data.get("data", {})
        confidence = data.get("confidence", 0)

        if status == "out_of_scope":
            return "⚠️ " + answer

        if status == "not_found":
            return "❌ " + answer

        parts = [answer]

        # Skills
        skills = payload.get("skills", [])
        if skills:
            parts.append("\n\n**Skills:**\n" + " · ".join(f"`{s}`" for s in skills))

        # Projects
        projects = payload.get("projects", [])
        if projects:
            project_lines = []
            for p in projects:
                if isinstance(p, dict):
                    title       = p.get("title", "") or p.get("name", "")
                    description = p.get("description", "")
                    if title and description:
                        project_lines.append(f"**{title}**\n  {description}")
                    elif title:
                        project_lines.append(f"**{title}**")
                    else:
                        project_lines.append(str(p))
                else:
                    project_lines.append(f"- {p}")
            parts.append("\n\n**Projects:**\n" + "\n\n".join(project_lines))

        # Experience
        experience = payload.get("experience", [])
        if experience:
            exp_lines = []
            for e in experience:
                if isinstance(e, dict):
                    title       = e.get("title", "") or e.get("role", "") or e.get("company", "") or e.get("name", "")
                    description = e.get("description", "")
                    if title and description:
                        exp_lines.append(f"**{title}**\n  {description}")
                    elif title:
                        exp_lines.append(f"**{title}**")
                    else:
                        exp_lines.append(str(e))
                else:
                    exp_lines.append(f"- {e}")
            parts.append("\n\n**Experience:**\n" + "\n\n".join(exp_lines))

        # Education
        education = payload.get("education", [])
        if education:
            edu_lines = []
            for e in education:
                if isinstance(e, dict):
                    institution = e.get("institution", "") or e.get("school", "") or e.get("name", "")
                    degree      = e.get("degree", "") or e.get("description", "")
                    if institution and degree:
                        edu_lines.append(f"**{institution}**\n  {degree}")
                    elif institution:
                        edu_lines.append(f"**{institution}**")
                    else:
                        edu_lines.append(str(e))
                else:
                    edu_lines.append(f"- {e}")
            parts.append("\n\n**Education:**\n" + "\n\n".join(edu_lines))

        # Certifications
        certifications = payload.get("certifications", [])
        if certifications:
            cert_lines = []
            for c in certifications:
                if isinstance(c, dict):
                    name = c.get("name", "") or c.get("title", "")
                    cert_lines.append(f"- {name}" if name else str(c))
                else:
                    cert_lines.append(f"- {c}")
            parts.append("\n\n**Certifications:**\n" + "\n".join(cert_lines))

        # Links — only show for contact/links intent
        links    = payload.get("links", {})
        github   = links.get("github", "")
        linkedin = links.get("linkedin", "")
        email    = links.get("email", "")
        phone    = links.get("phone", "")

        link_parts = []
        if email:
            link_parts.append(f"[{email}](mailto:{email})")
        if phone:
            link_parts.append(f"📞 {phone}")
        if github:
            link_parts.append(f"[GitHub]({github})")
        if linkedin:
            link_parts.append(f"[LinkedIn]({linkedin})")

        if link_parts and intent in ("links", "general"):
            is_contact_query = any(x in answer.lower() for x in ["contact", "email", "phone", "reach", "gmail"])
            if is_contact_query:
                parts[0] = ""
            parts.append("\n**Contact:**\n" + " · ".join(link_parts))

        # Low confidence note
        if confidence < 0.5 and status == "success":
            parts.append("\n\n*Note: This answer is based on partial information.*")

        return "".join(parts)

    except (json.JSONDecodeError, KeyError, TypeError):
        return raw_answer

@st.cache_resource
def load_chain():
    retriever = get_retriever()
    return get_chatbot_chain(retriever)

qa_chain = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome screen — shown only when no messages yet
if not st.session_state.messages:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a1a2e, #2d1b69);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        border: 1px solid #6C3FC5;
    ">
        <div style="font-size: 3rem; margin-bottom: 0.5rem">👩‍💻</div>
        <h2 style="color: white; margin: 0 0 0.5rem 0;">Hi, I'm KomalAI</h2>
        <p style="color: #c0b3e8; margin: 0 0 1.5rem 0;">
            Your personal guide to Komal Bhende's portfolio.<br>
            Ask me anything about her skills, projects, or experience.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick starter buttons
    st.markdown("**✨ Try asking:**")
    cols = st.columns(2)

    starters = [
        "What are Komal's skills?",
        "Tell me about her projects",
        "What is her work experience?",
        "Share her contact details",
        "What is her education?",
        "List her certifications"
    ]

    for i, question in enumerate(starters):
        with cols[i % 2]:
            if st.button(question, use_container_width=True, key=f"starter_{i}"):
                # Inject the question as if user typed it
                st.session_state.messages.append({"role": "user", "content": question})
                with st.spinner("Thinking..."):
                    try:
                        response = qa_chain.invoke({"input": question})
                        raw_answer = response.get("answer", "")
                        display_answer = parse_bot_response(raw_answer)
                    except Exception as e:
                        import traceback
                        display_answer = f"⚠️ Error: {traceback.format_exc()}"
                st.session_state.messages.append({"role": "assistant", "content": display_answer})
                st.rerun()

    st.divider()
    st.markdown("**📄 Want Komal's resume?**")

    try:
        with open("assets/Komal_Bhende_Resume.pdf", "rb") as pdf_file:
            st.download_button(
                label="📄 Download Resume PDF",
                data=pdf_file,
                file_name="Komal_Bhende_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except FileNotFoundError:
        st.warning("Resume PDF not found. Please add it to the assets/ folder.")



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask about Komal's skills, projects, experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response       = qa_chain.invoke({"input": prompt})
                raw_answer     = response.get("answer", "")
                display_answer = parse_bot_response(raw_answer)
            except Exception as e:
                import traceback
                display_answer = f"⚠️ Error: {traceback.format_exc()}"

        st.markdown(display_answer)
        st.session_state.messages.append({
            "role": "assistant",
            "content": display_answer
        })