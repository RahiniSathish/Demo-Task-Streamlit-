# streamlit_app.py

import streamlit as st
import socketio

# Create a Socket.IO client
sio = socketio.Client()

# We'll store incoming responses in a session_state list
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Socket event handlers
@sio.on("connect")
def on_connect():
    st.session_state["messages"].append("Connected to Socket.IO server!")

@sio.on("disconnect")
def on_disconnect():
    st.session_state["messages"].append("Disconnected from server.")

@sio.on("chat_response")
def on_chat_response(data):
    """
    Whenever we get a "chat_response" event from the server,
    append the message to our chat display.
    """
    reply_text = data.get("reply", "")
    st.session_state["messages"].append(f"Bot: {reply_text}")
    # Force rerun of the Streamlit app so we see the new message
    st.experimental_rerun()

def main():
    st.title("Socket.IO Chatbot (Streamlit)")

    # Attempt to connect if not already connected
    if not sio.connected:
        try:
            sio.connect("http://localhost:8001", wait_timeout=10)  # Ensure this URL is correct
        except Exception as e:
            st.error(f"Could not connect to server: {e}")

    # Chat message input
    user_message = st.text_input("Your message:")

    # Send button
    if st.button("Send"):
        if sio.connected:
            # Send the user's message to the server
            sio.emit("chat_message", {"message": user_message})
            # Also show user's own text in the local chat history
            st.session_state["messages"].append(f"You: {user_message}")
        else:
            st.warning("Not connected to the server!")

    # Display the conversation
    st.write("---")
    for msg in st.session_state["messages"]:
        st.write(msg)

if __name__ == "__main__":
    main()