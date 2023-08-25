


from fastapi import FastAPI

from main_router import router as UserRouter


app = FastAPI()

app.include_router(UserRouter, tags=["Company"], prefix="/company")

@app.get("/", tags=["Root"])
async def read_root():
    return "Welcome !"