from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="findora/templates")

router = APIRouter(tags=["Pages"])


@router.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/home.html",
        context={},
    )