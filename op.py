import streamlit as st
import google.generativeai as genai

# ---------------------------
#  Configure Gemini API key (Direct way)
# ---------------------------
genai.configure(api_key="enter key")  

# ---------------------------
# Gemini Model
# ---------------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------
# Helper Functions
# ---------------------------
def generate_code(prompt, language, difficulty, use_case):
    enhanced_prompt = f"""
    Generate {language} code.
    Difficulty: {difficulty}.
    Use-case: {use_case}.
    Task: {prompt}.
    Please provide clean, structured, and commented code.
    """
    response = model.generate_content(enhanced_prompt)
    return response.text

def explain_code(code):
    response = model.generate_content(f"Explain the following code line by line:\n{code}")
    return response.text

def debug_code(code):
    response = model.generate_content(f"Debug this code and suggest fixes:\n{code}")
    return response.text

def refactor_code(code):
    response = model.generate_content(f"Refactor and optimize this code:\n{code}")
    return response.text

# Streamlit UI

st.set_page_config(page_title="AI Code Generator", layout="wide")
st.title(" AI Code Generator with Explanations & Debugging")

# Input: Natural language prompt
user_prompt = st.text_area(" Enter your coding task (e.g., 'Write a Python function for merge sort'):")

# Dropdowns for parameters
col1, col2, col3 = st.columns(3)
with col1:
    selected_language = st.selectbox("Select Language", ["Python", "Java", "JavaScript", "C++", "SQL"])
with col2:
    difficulty = st.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])
with col3:
    use_case = st.selectbox("Select Use Case", ["General", "Web Development", "Data Science", "Algorithms"])

# Generate Code
if st.button("Generate Code"):
    if user_prompt.strip():
        generated_code = generate_code(user_prompt, selected_language, difficulty, use_case)
        st.subheader(" Generated Code")
        st.code(generated_code, language=selected_language.lower())
        
        # Export Option
        file_ext = {"Python": "py", "Java": "java", "JavaScript": "js", "C++": "cpp", "SQL": "sql"}[selected_language]
        st.download_button(
            label="⬇ Download Code",
            data=generated_code,
            file_name=f"generated_code.{file_ext}",
            mime="text/plain"
        )

# Explain Code
st.subheader(" Explain Code")
code_to_explain = st.text_area("Paste code to explain", key="explain_area")
if st.button("Explain", key="explain_btn"):
    if code_to_explain.strip():
        explanation = explain_code(code_to_explain)
        st.write(explanation)

# Debug Code
st.subheader("Debug & Analyze Code")
code_to_debug = st.text_area("Paste code to debug", key="debug_area")
if st.button(" Debug", key="debug_btn"):
    if code_to_debug.strip():
        debugged = debug_code(code_to_debug)
        st.write(debugged)

# Refactor Code
st.subheader("Refactor & Optimize Code")
code_to_refactor = st.text_area("Paste code to refactor", key="refactor_area")
if st.button(" Refactor", key="refactor_btn"):
    if code_to_refactor.strip():
        refactored = refactor_code(code_to_refactor)
        st.write(refactored)
