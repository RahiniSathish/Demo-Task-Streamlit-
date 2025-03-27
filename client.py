import streamlit as st
import socketio


sio = socketio.Client()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

@sio.on("connect")
def on_connect():
    st.session_state["messages"].append("Connected to Socket.IO server!")

@sio.on("disconnect")
def on_disconnect():
    st.session_state["messages"].append("Disconnected from server.")

@sio.on("chat_response")
def on_chat_response(data):
    reply_text = data.get("reply", "")
    st.session_state["messages"].append(f"Bot: {reply_text}")
    st.experimental_rerun()

def main():
    st.title("Socket.IO Chatbot (Streamlit)")

    if not sio.connected:
        try:
            sio.connect("http://localhost:8001", wait_timeout=10) 
        except Exception as e:
            st.error(f"Could not connect to server: {e}")

    user_message = st.text_input("Your message:")

    if st.button("Send"):
        if sio.connected:
            # Send the user's message to the server
            sio.emit("chat_message", {"message": user_message})
            # Also show user's own text in the local chat history
            st.session_state["messages"].append(f"You: {user_message}")
        else:
            st.warning("Not connected to the server!")

    st.write("---")
    for msg in st.session_state["messages"]:
        st.write(msg)

if __name__ == "__main__":
    main()
