from typing import List
from fastapi import APIRouter, HTTPException, Depends
from models import User, Post_Pydantic, PostIn_Pydantic, Post
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from .auth import get_current_user

router = APIRouter()


class Status(BaseModel):
	message: str


@router.get('', response_model=List[Post_Pydantic])
async def get_posts(user: User = Depends(get_current_user)):
	return await Post_Pydantic.from_queryset(user.posts.all().order_by('-date'))


@router.post('', response_model=Post_Pydantic)
async def create_post(post: PostIn_Pydantic, user: User = Depends(get_current_user)):
	Post_obj = await Post.create(author=user, **post.dict(exclude_unset=True))
	return await Post_Pydantic.from_tortoise_orm(Post_obj)


@router.get(
	'/{post_id}', response_model=Post_Pydantic, responses={404: {'model': HTTPNotFoundError}}
)
async def get_post(post_id: str, user: User = Depends(get_current_user)):
	return await Post_Pydantic.from_queryset_single(Post.get(author=user, id=post_id))


@router.put(
	'/{post_id}', response_model=Post_Pydantic, responses={404: {'model': HTTPNotFoundError}}
)
async def update_post(post_id: str, post: PostIn_Pydantic, user: User = Depends(get_current_user)):
	await user.posts.filter(id=post_id).update(author=user, **post.dict(exclude_unset=True))
	return await Post_Pydantic.from_queryset_single(Post.get(author=user, id=post_id))


@router.delete('/{post_id}', response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_Post(post_id: str, user: User = Depends(get_current_user)):
	deleted_count = await user.posts.filter(id=post_id).delete()
	if not deleted_count:
		raise HTTPException(status_code=404, detail=f'Post {post_id} not found')
	return Status(message=f'Deleted Post {post_id}')
