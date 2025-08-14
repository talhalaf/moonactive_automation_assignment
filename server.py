from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from graph.models import LevelConfig
from graph.graph import build_graph



app = FastAPI(title="Level Config Validation API")

# Build/compile the graph once at startup
graph = build_graph()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/validate")
def validate_level(config: LevelConfig):
    """
    Accept a LevelConfig, invoke the validation/review graph, and return the full state.
    """
    try:
        # The graph expects an input dict with key `input_config`
        result = graph.invoke(input={"input_config": config})
        return JSONResponse(content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optional: provide an ASGI entrypoint for `uvicorn server:app --reload`
