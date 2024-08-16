import requests
import redis
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from cache.Cache import Cache

# try:
#     rd = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
#     # Testando a conexão
#     rd.ping()
# except redis.ConnectionError as e:
#     print("Failed to connect to Redis:", e)
#     raise

app = FastAPI()
cache = Cache()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    try:
        cache_key = f"todo_{todo_id}"
        # cached_data = rd.get(cache_key)
        cached_data = cache.get_cache(cache_key)

        if cached_data:
            print("Reading from cache...")
            return json.loads(cached_data)

        else:
            print("Fetching data from API...")
            response = requests.get(f"https://jsonplaceholder.typicode.com/todos/{todo_id}")
            response.raise_for_status()

            data = response.json()
            # rd.set(cache_key, json.dumps(data), ex=10)
            cache.set_cache(cache_key, json.dumps(data))
            return data

    except requests.exceptions.RequestException as e:
        error_message = {
            "error": "Erro ao buscar dados da API.",
            "details": str(e)
        }
        return JSONResponse(status_code=500, content=error_message)

    except Exception as e:
        error_message = {
            "error": "Ocorreu um erro inesperado.",
            "details": str(e)
        }
        return JSONResponse(status_code=500, content=error_message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)