import streamlit as st
import requests
import logging
import json
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_session_state():
    # Check for stored credentials in query parameters
    stored_credentials = st.query_params.get("credentials", None)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Initialize API URL and bearer token
    if "api_url" not in st.session_state:
        st.session_state.api_url = ""
    if "bearer_token" not in st.session_state:
        st.session_state.bearer_token = ""
    
    # Initialize welcome state
    if "show_welcome" not in st.session_state:
        st.session_state.show_welcome = True
    
    # If we have stored credentials, try to restore the session
    if stored_credentials:
        try:
            # Decode the credentials from base64
            decoded_bytes = base64.b64decode(stored_credentials)
            decoded_str = decoded_bytes.decode('utf-8')
            credentials = json.loads(decoded_str)
            
            # Restore the session state
            st.session_state.api_url = credentials.get("api_url", "")
            st.session_state.bearer_token = credentials.get("bearer_token", "")
            
            # Only set logged_in to True if we have both values
            if st.session_state.api_url and st.session_state.bearer_token:
                st.session_state.logged_in = True
                logger.info("Session restored from stored credentials")
        except Exception as e:
            logger.error(f"Error restoring session: {str(e)}")


def make_api_request(data):
    headers = {
        "Authorization": f"Bearer {st.session_state.bearer_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(st.session_state.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.info(f"API request: {data}")
        st.error(f"API Error: {str(e)}")
        return None


def extract_last_message_text(response):
    """
    Extract the text from the last message in the response.
    
    :param response: API response JSON
    :return: Text content of the last message
    """
    try:
        # Extract the text from the last message's content
        if response and isinstance(response, list) and len(response) > 0:
            # Check if the response has the expected structure
            if "output" in response[0] and "message" in response[0]["output"]:
                message = response[0]["output"]["message"]
                if "content" in message and isinstance(message["content"], list) and len(message["content"]) > 0:
                    # Get the text from the first content item
                    return message["content"][0]["text"]
    except Exception as e:
        logger.error(f"Error extracting message text: {str(e)}")
    
    return "No response text available."


def display_login_page():
    st.title("🔐 Login to BriefMe Brilliantly")
    
    with st.form("login_form"):
        st.subheader("Enter API Configuration")
        
        api_url = st.text_input(
            "API URL",
            value="",
            placeholder="Enter API URL"
        )
        
        bearer_token = st.text_input(
            "Bearer Token",
            value="",
            placeholder="Enter Bearer Token",
            type="password"
        )
        
        remember_me = st.checkbox("Remember me", value=True,
                                help="Keep me logged in when I refresh the page")
        
        submit_button = st.form_submit_button("Login", use_container_width=True)
    
    if submit_button:
        if not api_url or not bearer_token:
            st.error("Please enter both API URL and Bearer Token")
        else:
            # Store credentials in session state
            st.session_state.api_url = api_url
            st.session_state.bearer_token = bearer_token
            st.session_state.logged_in = True
            
            # If remember me is checked, store credentials in query parameters
            if remember_me:
                # Create a JSON object with the credentials
                credentials = {
                    "api_url": api_url,
                    "bearer_token": bearer_token
                }
                
                # Encode the credentials as base64 to avoid issues with special characters
                credentials_json = json.dumps(credentials)
                credentials_bytes = credentials_json.encode('utf-8')
                credentials_base64 = base64.b64encode(credentials_bytes).decode('utf-8')
                
                # Store the encoded credentials in query parameters
                st.query_params["credentials"] = credentials_base64
                logger.info("Credentials stored in query parameters")
            
            st.success("Login successful!")
            st.rerun()


def display_welcome():
    welcome_md = """
    # 🎯 Welcome to BriefMe Brilliantly! 🎯

    ### *"Because walking into a meeting unprepared is like bringing a spoon to a knife fight!"*

    ---

    ## 🤖 Your Pre-Meeting Intelligence Partner 🤖

    I'm your AI-powered briefing specialist, designed to make you look like you've done your homework (even if you were binge-watching cat videos last night).

    ### What I can do for you:

    * **Company Deep Dives** - Get the lowdown on any organization faster than you can say "quarterly earnings"
    
    * **People Intelligence** - Discover who's who before you shake hands (and avoid those awkward "So... what do you do here?" moments)
    
    * **LinkedIn Reconnaissance** - Find professional backgrounds without the endless scrolling
    
    * **Meeting Prep Made Easy** - Comprehensive briefings that fit in your pocket (or at least your tablet)

    ### How to use me:

    Simply tell me who you're meeting with and their company name. For example:
    
    > "I'm meeting with Sarah Johnson and Michael Lee from Acme Corporation tomorrow."
    
    Then sit back and watch as I compile a detailed briefing that will make your colleagues wonder if you've hired a private investigator!

    ---

    *Ready to be the most prepared person in the room? Let's get started!*
    """
    
    st.markdown(welcome_md)
    
    if st.button("Let's Get Started!", type="primary"):
        st.session_state.show_welcome = False
        st.rerun()


def main():
    st.set_page_config(
        page_title="BriefMe Brilliantly",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    initialize_session_state()

    # Display login page if not logged in
    if not st.session_state.logged_in:
        display_login_page()
        return

    # Display welcome page if it's the first visit and user is logged in
    if st.session_state.show_welcome:
        display_welcome()
        return

    st.title("🎯 BriefMe Brilliantly")
    st.caption("Your AI-powered meeting prep assistant - making you look good since 2025!")

    # Add logout button in the sidebar
    with st.sidebar:
        if st.button("Logout"):
            # Clear session state
            st.session_state.logged_in = False
            st.session_state.api_url = ""
            st.session_state.bearer_token = ""
            
            # Clear stored credentials from query parameters
            if "credentials" in st.query_params:
                del st.query_params["credentials"]
                logger.info("Credentials cleared from query parameters")
            
            st.rerun()
        
        if st.button("Show Welcome Page"):
            st.session_state.show_welcome = True
            st.rerun()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Who are you meeting with? (e.g., 'I'm meeting with John Smith from Acme Corp')"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Format the request with messages array
        request_data = {"prompt": prompt}

        with st.spinner("Researching your contacts... This might take a moment..."):
            api_response = make_api_request(request_data)

        if api_response:
            # Extract the text from the last message
            response_text = extract_last_message_text(api_response)
            
            # Add to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })

            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response_text)


if __name__ == "__main__":
    main()