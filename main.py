from fastapi import FastAPI
from routers import feedback_router
from routers import translate_router


app = FastAPI()

# Check server status
@app.get("/")
def root():
    return {"message": "Python Running"}


# routes
app.include_router(feedback_router.router)
app.include_router(translate_router.router)