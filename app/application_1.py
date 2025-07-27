from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from markupsafe import Markup
from dotenv import load_dotenv
from app.components.retriever import create_qa_chain
import asyncio

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# Register nl2br filter
def nl2br(value: str):
    return Markup(value.replace("\n", "<br>\n"))

templates.env.filters["nl2br"] = nl2br

# Global in-memory chat history (shared across users)
chat_history = []

# ---------- GET Route for HTML UI ----------
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": chat_history,
            "error": None
        }
    )

# ---------- Streaming POST API ----------
@app.post("/stream")
async def stream_response(prompt: str = Form(...)):
    chat_history.append({"role": "user", "content": prompt})

    try:
        qa_chain = create_qa_chain()
        if qa_chain is None:
            raise Exception("QA chain could not be created")

        response = qa_chain.invoke({"query": prompt})
        result = response.get("result", "No response")

        async def token_generator():
            for token in result.split():
                yield token + " "
                await asyncio.sleep(0.0001)

        chat_history.append({"role": "assistant", "content": result})
        return StreamingResponse(token_generator(), media_type="text/plain")

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        chat_history.append({"role": "assistant", "content": error_msg})
        async def err_gen(): yield error_msg
        return StreamingResponse(err_gen(), media_type="text/plain")

# ---------- Clear Chat ----------
@app.get("/clear")
async def clear_chat():
    chat_history.clear()
    return RedirectResponse("/", status_code=303)
