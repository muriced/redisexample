import requests
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from cache import Cache

cache = Cache()
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    try:
        cache_key = f"todo_{todo_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            print("Reading from cache...")
            return json.loads(cached_data)

        else:
            print("Fetching data from API...")
            response = requests.get(f"https://jsonplaceholder.typicode.com/todos/{todo_id}")
            response.raise_for_status()

            data = response.json()
            cache.set(cache_key, json.dumps(data), timeout=60*60) # Using cache for 1 hour
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