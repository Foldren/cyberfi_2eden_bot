from typing import Annotated
from fastapi import FastAPI, Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import UJSONResponse
from uvicorn import run

app = FastAPI(default_response_class=UJSONResponse)
templates = Jinja2Templates(directory=".")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/validate_hash")
async def validate_hash(x_telegram_init_data: Annotated[str | None, Header()] = None):
    print(x_telegram_init_data)
    # idata = user.init_data[:55] + "2" + user.init_data[56:]
    # data = check_webapp_signature(token=TOKEN, init_data=idata)
    # data2 = check_webapp_signature(token=TOKEN, init_data=user.init_data)
    # print(str(data), str(data2))
    # try:
    #     data = safe_parse_webapp_init_data(token=TOKEN, init_data=init_data["_auth"])
    # except ValueError:
    #     return UJSONResponse(content={"ok": False, "err": "Unauthorized"}, status_code=401)
    # return UJSONResponse(content={"ok": True, "data": "cool"})


if __name__ == "__main__":
    run(app, port=8001)
