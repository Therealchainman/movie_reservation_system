



```sh
docker compose -f service.yaml up

docker ps

docker exec -it postgres_db bash

psql -h localhost -U admin -d default


```

ipykernel, asyncpg, fastapi, pydantic, uvicorn, requests
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```sh
uvicorn main:app --reload
```