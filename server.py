import uvicorn
from fastapi import FastAPI
import socketio

sio = socketio.AsyncServer(
    async_mode="asgi", 
    cors_allowed_origins="*"
)

fastapi_app = FastAPI()

@fastapi_app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@sio.on('connect')
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.on('disconnect')
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on('chat_message')
async def handle_chat_message(sid, data):
    user_text = data.get("message", "")
    llm_reply = f"LLM says: I heard you say '{user_text}'."
    await sio.emit("chat_response", {"reply": llm_reply}, room=sid)


app = socketio.ASGIApp(sio, fastapi_app)

if __name__ == "__main__":
    # Now run `app` rather than `fastapi_app`
    uvicorn.run(app, host="localhost", port=8001)
