from fastapi import FastAPI
import uvicorn
# from argparse import ArgumentParser

from config_dev import PORT, HOST

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
