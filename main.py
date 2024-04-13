from fastapi import FastAPI
from starlette.responses import JSONResponse
from utils import get_from_json

app = FastAPI()


@app.get("/")
async def root():
    news = get_from_json('news.json')
    if isinstance(news, JSONResponse):
        return news
    comments = get_from_json('comments.json')
    if isinstance(comments, JSONResponse):
        return comments
    comments_count = dict()
    for i, elem_news in enumerate(news['news']):
        if elem_news['deleted']:
            del news['news'][i]
    for i in comments['comments']:
        if i['news_id'] not in comments_count:
            comments_count[i['news_id']] = 1
        else:
            comments_count[i['news_id']] += 1
    for elem_news in news['news']:
        elem_news['comments_count'] = comments_count[elem_news['id']] if elem_news['id'] in comments_count else 0
    return JSONResponse(status_code=200, content=news)


@app.get("/news/{news_id}")
async def get_news_object(news_id: int):
    news = get_from_json('news.json')
    if isinstance(news, JSONResponse):
        return news
    comments = get_from_json('comments.json')
    if isinstance(comments, JSONResponse):
        return comments

    news_filtered = list(filter(lambda x: x['id'] == news_id and not x['deleted'], news['news']))
    if len(news_filtered) == 0:
        return JSONResponse(status_code=404, content=f"Новости №={news_id} не существует")
    news_filtered = news_filtered[0]

    news_comments = list(filter(lambda x: x['news_id'] == news_filtered['id'], comments['comments']))
    news_filtered['comments'] = news_comments
    news_filtered['comments_count'] = len(news_comments)
    return JSONResponse(status_code=200, content=news_filtered)
