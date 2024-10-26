from fastapi import FastAPI
from routers import feedback_router


app = FastAPI()

# Check server status
@app.get("/")
def root():
    return {"message": "Python Running"}


# routes
app.include_router(feedback_router.router)