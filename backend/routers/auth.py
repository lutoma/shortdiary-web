from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from models import User, User_Pydantic
from tortoise.exceptions import DoesNotExist


SECRET_KEY = '381ba6066c7387729b6c295834b220376058fe1d2ee6769cce7b0950935bda3b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
router = APIRouter()


class TokenData(BaseModel):
	uuid: str | None = None


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
		token_data = TokenData(uuid=uuid)
	except JWTError:
		raise credentials_exception

	user = User.get(id=token_data.uuid)
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
	ephemeral_key_salt: str
	master_key: str
	master_key_nonce: str


@router.post('/login', response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	try:
		user = await User_Pydantic.from_queryset_single(User.get(name=form_data.username))
	except DoesNotExist:
		user = None

	if not user or not pwd_context.verify(form_data.password, user.password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect username or password',
			headers={'WWW-Authenticate': 'Bearer'},
		)

	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={'sub': str(user.id)}, expires_delta=access_token_expires
	)
	return {
		'access_token': access_token,
		'ephemeral_key_salt': user.ephemeral_key_salt,
		'master_key': user.master_key,
		'master_key_nonce': user.master_key_nonce,
	}


class SignupData(BaseModel):
	name: str
	email: str
	password: str
	ephemeral_key_salt: str
	master_key: str
	master_key_nonce: str


class SignupResponse(BaseModel):
	name: str
	email: str


@router.post('/signup', response_model=SignupResponse)
async def signup(user: SignupData):
	user.password = pwd_context.hash(user.password)
	user = await User.create(**user.dict(exclude_unset=True))
	return await User_Pydantic.from_tortoise_orm(user)
