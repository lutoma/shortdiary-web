# shortdiary

Shortdiary consists of two parts, an API written in Python using [FastAPI](https://fastapi.tiangolo.com/) and [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/), and an ES6 frontend using [Vue 3](https://vuejs.org/) + [Vite](https://vitejs.dev/) + [Pinia](https://pinia.vuejs.org/) + [Element-Plus](https://element-plus.org/).

## Backend

```
poetry install
poetry run uvicorn main:app --reload
```

## Frontend

```
yarn install
yarn dev
```
