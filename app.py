import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from models import Post, Comment, Location, Category, User

app = FastAPI()

# Будущая база данных
posts = []
comments = []

# Реализация запросов GET, POST, PUT, DELETE методов REST

@app.get("/posts")
async def get_posts():
    return posts

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    for post in posts:
        if post.id == post_id: # Поиск по айди поста
            return post
    raise HTTPException(404, "Post not found") # Дальше - ошибки 

@app.post("/posts")
async def create_post(post: Post):
    post.id = len(posts) + 1 # Контроль количества постов
    posts.append(post)
    return post

@app.put("/posts/{post_id}")
async def update_post(post_id: int, updated_post: Post):
    for i, post in enumerate(posts):
        if post.id == post_id:
            updated_post.id = post_id  
            posts[i] = updated_post
            return updated_post
    raise HTTPException(404, "Post not found")

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    for i, post in enumerate(posts):
        if post.id == post_id:
            posts.pop(i)
            return {"message": "Post deleted"}
    raise HTTPException(404, "Post not found")

@app.get("/posts/{post_id}/comments")
async def get_comments(post_id: int):
    return [c for c in comments if c.post_id == post_id]

@app.post("/comments")
async def create_comment(comment: Comment):
    comment.id = len(comments) + 1
    comments.append(comment)
    return comment

async def run():
    config = uvicorn.Config("app:app", host="127.0.0.1", port=8000)
    server = uvicorn.Server(config=config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(run())