from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import posts, auth

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="Shortdiary API")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"],
	dependencies=[Depends(auth.get_current_user)])

register_tortoise(
	app,
	db_url="sqlite://db.sqlite3",
	modules={"models": ["models"]},
	generate_schemas=True,
	add_exception_handlers=True,
)
