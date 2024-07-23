from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Define a list of allowed origins for CORS
origins = [
    "*",
]

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allows only specified methods
    allow_headers=["X-Requested-With", "Content-Type"],  # Allows only specified headers
)

# 数据模型
class Score(BaseModel):
    name: str
    score: int


# 数据库初始化
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  score INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


init_db()


# 提交分数的API
@app.post("/score")
async def submit_score(score: Score):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (score.name, score.score))
    conn.commit()
    conn.close()
    return {"message": "Score submitted successfully"}


# 获取排行榜的API
@app.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()

    leaderboard = [{"name": name, "score": score} for name, score in results]
    return {"leaderboard": leaderboard}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)