import streamlit as st
from fpdf import FPDF
from langchain_mistralai import ChatMistralAI

# Your mistral  API key (ensure this is kept secret in actual deployments)

MISTRAL_API_KEY = "***"
mistral_model = "codestral-latest"

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def append_message(role, content):
    """Appends a message to the conversation history."""
    st.session_state["messages"].append({"role": role, "content": content})

def display_last_response():
    """Displays only the last message in the conversation history."""
    if st.session_state["messages"]:
        last_message = st.session_state["messages"][-1]
        if last_message['role'] == 'user':
            st.write(f"**You**: {last_message['content']}")
        else:
            st.write(f"**Chatbot**: {last_message['content']}")

def code_generation_tab():
    st.title("Code Generation")

    # Dropdown options for programming languages
    programming_languages = [
        None, "Python", "Java", "C++", "JavaScript", "C#", "PHP", "Ruby", "Swift",
        "Kotlin", "Go", "Rust", "Dart", "TypeScript", "Perl", "R", "Scala", "Julia",
        "MATLAB", "SQL", "Assembly", "HTML", "CSS"
    ]

    # Selectbox for dropdown
    selected_language = st.selectbox("Select a programming language", programming_languages)

    # Text input for user query
    user_input = st.text_area("Enter your question")

    # Button to generate code
    if st.button("Generate"):
        if user_input and selected_language:
            # Append user input to history
            append_message("user", f"Code:\n{user_input}\n in \n{selected_language}")

            # Display conversation including the loading state
            with st.spinner('Waiting for response...'):
                try:
                    llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=MISTRAL_API_KEY)
                    prompt = f"""develop the working code for :\n\nCode:\n{user_input}\n\n in \n{selected_language}
                                while explaining code also mention feature of code like time complexity etc
                                """
                    response = llm.invoke([("user", prompt)])
                    bot_response = response.content

                    append_message("bot", bot_response)
                    st.code(bot_response, language=selected_language.lower())
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            # Display the last response
            display_last_response()
        else:
            st.warning("Please select a programming language and enter your question before clicking 'Generate'.")

def code_conversion_tab():
    st.title("Code Conversion")

    # Dropdown options for programming languages
    programming_languages = [
        None, "Python", "Java", "C++", "JavaScript", "C#", "PHP", "Ruby", "Swift",
        "Kotlin", "Go", "Rust", "Dart", "TypeScript", "Perl", "R", "Scala", "Julia",
        "MATLAB", "SQL", "Assembly", "HTML", "CSS"
    ]

    # User input field for code
    user_code_input = st.text_area("Enter your code here:")
    language = st.selectbox("Select the target language", programming_languages)

    # Button to convert code
    if st.button("Convert Code"):
        if user_code_input and language:
            # Append user code to history
            append_message("user", user_code_input)

            # Display conversation including the loading state
            with st.spinner('Converting code...'):
                try:
                    llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=MISTRAL_API_KEY)
                    prompt = f"Convert the following code to {language}:\n\n{user_code_input}"
                    response = llm.invoke([("user", prompt)])
                    converted_code = response.content

                    append_message("bot", converted_code)
                    st.code(converted_code, language='java')
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            # Display the last response
            display_last_response()

def code_reviewer_tab():
    st.title("Code Review Chatbot")

    # User input field for code
    user_code_input = st.text_area("Enter your code here:")

    # Button to submit code
    if st.button("Send"):
        if user_code_input:
            # Append user code to history
            append_message("user", user_code_input)

            # Display conversation including the loading state
            with st.spinner('Waiting for response...'):
                try:
                    llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=MISTRAL_API_KEY)
                    prompt = f"Review the following code and provide feedback:\n\n{user_code_input}"
                    response = llm.invoke([("user", prompt)])
                    bot_response = response.content

                    append_message("bot", bot_response)
                except Exception as e:
                    bot_response = f"An error occurred: {e}"
                    append_message("bot", bot_response)

        # Display the last response
        display_last_response()

def code_debugger_tab():
    st.title("Code Debugger")

    # User input fields for code and error
    user_code_input = st.text_area("Enter your code here:")
    user_error_input = st.text_area("Enter the error message here:")

    # Button to submit code and error
    if st.button("Debug"):
        if user_code_input and user_error_input:
            # Append user code and error to history
            append_message("user", f"Code:\n{user_code_input}\nError:\n{user_error_input}")

            # Display conversation including the loading state
            with st.spinner('Waiting for response...'):
                try:
                    llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=MISTRAL_API_KEY)
                    prompt = f"Debug the following code and fix the error:\n\nCode:\n{user_code_input}\n\nError:\n{user_error_input}"
                    response = llm.invoke([("user", prompt)])
                    bot_response = response.content

                    append_message("bot", bot_response)
                except Exception as e:
                    bot_response = f"An error occurred: {e}"
                    append_message("bot", bot_response)

        # Display the last response
        display_last_response()

def generate_document(code):
    llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=MISTRAL_API_KEY)
    prompt = f"""
        Create a detailed PDF document about the following code:
        \n\nCode:\n{code}\n\n
        The document should include:
        1. A generated heading based on the code.
        2. A list of contents.
        3. An about section with a short paragraph about the code and its use.
        4. The provided code.
        5. A line-by-line explanation of the code.
        6. Other ways to write the given code.
        7. A conclusion.
        """
    response = llm.invoke([("user", prompt)])
    document_content = response.content
    
    return document_content

def save_pdf(content, file_name="Code_Document.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    pdf.output(file_name)

def document_generation_tab():
    st.title("Document Generation")

    # User input field for code
    user_code_input = st.text_area("Enter your code here:")

    # Button to submit code
    if st.button("Generate Document"):
        if user_code_input:
            # Append user code to history
            append_message("user", user_code_input)

            # Display conversation including the loading state
            with st.spinner('Generating document...'):
                try:
                    document_content = generate_document(user_code_input)
                    save_pdf(document_content)
                    st.success("Document generated successfully. Download the PDF below:")
                    st.download_button(label="Download PDF", data=open("Code_Document.pdf", "rb"), file_name="Code_Document.pdf")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

def css_code_execution():
    st.markdown("""
    <style>
        .question-container {
            border-radius: 10px; /* Round corners */
            overflow-y: auto; /* Enable scrolling for content within */
        }
        .human {
            background-color: #e0e0e0; /* Light grey background for question */
            padding: 5px; /* Add some padding for better separation */
            border-radius: 5px; /* Round corners for the question paragraph */
            font-weight: bold; /* Bold text for question */
        }
        .st-emotion-cache-18ni7ap.ezrtsby2 {
            visibility:hidden;
        }
    </style>
    """, unsafe_allow_html=True)

# Define the sidebar navigation
def main():
    css_code_execution()
    st.sidebar.markdown("<h1 style='font-size: 32px;'>Code Assist+</h1>", unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Code Generation", "Code Conversion", "Code Review Chatbot", "Code Debugger", "Document Generation", "About"])

    if app_mode == "Code Generation":
        code_generation_tab()
    elif app_mode == "Code Conversion":
        code_conversion_tab()
    elif app_mode == "Code Review Chatbot":
        code_reviewer_tab()
    elif app_mode == "Code Debugger":
        code_debugger_tab()
    elif app_mode == "Document Generation":
        document_generation_tab()
    elif app_mode == "About":
        st.title("About Code Assist+")
        st.markdown("""
        **Code Assist+** is a powerful tool designed to help developers with their coding needs. Whether you are looking for code generation, code conversion, code reviews, debugging assistance, or creating detailed documentation, Code Assist+ has you covered.

        ### Features
        - **Code Generation**: Generate working code snippets in various programming languages.
        - **Code Conversion**: Convert code from one programming language to another.
        - **Code Review Chatbot**: Get feedback and suggestions on your code snippets.
        - **Code Debugger**: Find and fix errors in your code quickly and efficiently.
        - **Document Generation**: Create detailed PDF documents about your code, including explanations and alternative implementations.

        ### How to Use
        1. Navigate to the desired tab using the sidebar.
        2. Enter your code or query in the input fields provided.
        3. Click the relevant button to get feedback, assistance, or generate documents.

        We hope Code Assist+ becomes an essential part of your development workflow. Happy coding!
        """)

if __name__ == "__main__":
    main()