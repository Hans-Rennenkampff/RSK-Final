from fastapi import FastAPI, __version__ as fastapi_version

app = FastAPI()

@app.get("/version")
async def get_version():
    return {"fastapi_version": fastapi_version}