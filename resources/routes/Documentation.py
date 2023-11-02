from fastapi.openapi.models import Tag
from fastapi.responses import RedirectResponse

from resources.settings.App import app

TAG_DOCUMENTATION = Tag(
    name="Documentation",
    description="Documentation selection: Swagger.",
)


@app.get("/", tags=[TAG_DOCUMENTATION])
def documentation_route():
    """
    Redirects to the /swagger route,\
    a screen which allows access to documentation.
    """
    return RedirectResponse("/swagger")
