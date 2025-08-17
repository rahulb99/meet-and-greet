from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from philoagents.application.conversation_service.generate_response import (
    get_response,
    get_streaming_response,
)
from philoagents.application.conversation_service.reset_conversation import (
    reset_conversation_state,
)
from philoagents.domain.celeb_factory import CelebFactory

from .opik_utils import configure

configure()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the API."""
    # Startup code (if any) goes here
    yield
    # Shutdown code goes here
    opik_tracer = OpikTracer()
    opik_tracer.flush()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str
    celeb_id: str


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        celeb_factory = CelebFactory()
        celeb = celeb_factory.get_celeb(chat_message.celeb_id)

        response, _ = await get_response(
            messages=chat_message.message,
            celeb_id=chat_message.celeb_id,
            celeb_name=celeb.name,
            celeb_perspective=celeb.perspective,
            celeb_style=celeb.style,
            celeb_context="",
        )
        return {"response": response}
    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()

        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            if "message" not in data or "celeb_id" not in data:
                await websocket.send_json(
                    {
                        "error": "Invalid message format. Required fields: 'message' and 'celeb_id'"
                    }
                )
                continue

            try:
                celeb_factory = CelebFactory()
                celeb = celeb_factory.get_celeb(
                    data["celeb_id"]
                )

                # Use streaming response instead of get_response
                response_stream = get_streaming_response(
                    messages=data["message"],
                    celeb_id=data["celeb_id"],
                    celeb_name=celeb.name,
                    celeb_perspective=celeb.perspective,
                    celeb_style=celeb.style,
                    celeb_context="",
                )

                # Send initial message to indicate streaming has started
                await websocket.send_json({"streaming": True})

                # Stream each chunk of the response
                full_response = ""
                async for chunk in response_stream:
                    full_response += chunk
                    await websocket.send_json({"chunk": chunk})

                await websocket.send_json(
                    {"response": full_response, "streaming": False}
                )

            except Exception as e:
                opik_tracer = OpikTracer()
                opik_tracer.flush()

                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        pass


@app.post("/reset-memory")
async def reset_conversation():
    """Resets the conversation state. It deletes the two collections needed for keeping LangGraph state in MongoDB.

    Raises:
        HTTPException: If there is an error resetting the conversation state.
    Returns:
        dict: A dictionary containing the result of the reset operation.
    """
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
