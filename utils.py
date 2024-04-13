import json5
from starlette.responses import JSONResponse


def get_from_json(filename: str):
    try:
        with open(f'json_data/{filename}', 'r') as news_file:
            return json5.load(news_file)
    except BaseException:
        return JSONResponse(status_code=404, content=f"ошибка декодирования json: '{filename}'")