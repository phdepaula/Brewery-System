from fastapi.responses import RedirectResponse

from resources.settings.App import app


@app.get("/", tags=["Documentation"])
def documentation_route():
    """
    Redirects to the /swagger route,\
    a screen which allows access to documentation.
    """
    return RedirectResponse("/swagger")
