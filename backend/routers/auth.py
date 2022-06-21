from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from models import User, User_Pydantic, UserIn_Pydantic
from tortoise.exceptions import DoesNotExist
import os


SECRET_KEY = os.environ.get('SHORTDIARY_SECRET', 'insecure-changeme')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={'WWW-Authenticate': 'Bearer'},
	)

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		uuid: str = payload.get('sub')
		if uuid is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception

	user = await User.get(id=uuid)
	if user is None:
		raise credentials_exception
	return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({'exp': expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


class LoginResponse(BaseModel):
	access_token: str
	user: User_Pydantic


@router.post('/login', response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	try:
		user = await User.get(email=form_data.username)
	except DoesNotExist:
		user = None

	if not user or not pwd_context.verify(form_data.password, user.password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect username or password',
			headers={'WWW-Authenticate': 'Bearer'},
		)

	user.last_seen = datetime.utcnow()
	await user.save()

	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={'sub': str(user.id)}, expires_delta=access_token_expires
	)
	return {
		'access_token': access_token,
		'user': await User_Pydantic.from_tortoise_orm(user),
		'ephemeral_key_salt': user.ephemeral_key_salt,
		'master_key': user.master_key,
		'master_key_nonce': user.master_key_nonce,
	}


class SignupData(BaseModel):
	email: str
	password: str
	ephemeral_key_salt: str
	master_key: str
	master_key_nonce: str


class SignupResponse(BaseModel):
	email: str


@router.post('/signup', response_model=SignupResponse)
async def signup(user: SignupData):
	if await User.get(email=user.email).exists():
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail='An account with this email address already exists'
		)

	user.password = pwd_context.hash(user.password)
	user = await User.create(**user.dict(exclude_unset=True))
	return await User_Pydantic.from_tortoise_orm(user)


@router.get('/user', response_model=User_Pydantic)
async def get_user(user: User = Depends(get_current_user)):
	return await User_Pydantic.from_tortoise_orm(user)


@router.put('/user', response_model=User_Pydantic)
async def update_user(user_data: UserIn_Pydantic, user: User = Depends(get_current_user)):
	await User.filter(id=user.id).update(**user_data.dict(exclude_unset=True))
	return await User_Pydantic.from_queryset_single(User.get(id=user.id))
