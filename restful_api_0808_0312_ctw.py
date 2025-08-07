# 代码生成时间: 2025-08-08 03:12:11
# -*- coding: utf-8 -*-

"""
RESTful API using Falcon framework
"""

from falcon import API, HTTPError, HTTP_400, HTTP_404, HTTP_500, Request, Response
from falcon.asgi import StarletteAdapter
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.middleware.wsgi import WSGIMiddleware
import json

# Middleware to handle errors
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPError as e:
            return JSONResponse(
                status_code=e.status,
                content=json.dumps({"error": e.description}),
                media_type="application/json"
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTP_500,
                content=json.dumps({"error": str(e)}),
                media_type="application/json"
            )

# A simple resource
class SimpleResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({"message": "Hello, World!"}).encode()
        resp.status = HTTP_200
        resp.media_type = "application/json"

    def on_post(self, req, resp):
        try:
            data = json.load(req.stream)
            resp.body = json.dumps({"message": "Data received", "your_data": data}).encode()
            resp.status = HTTP_200
            resp.media_type = "application/json"
        except json.JSONDecodeError:
            raise HTTPError(status=HTTP_400, description="Invalid JSON")

# Initialize the application
app = Starlette()

# Add routes
app.add_route("/", SimpleResource(), methods=["GET", "POST"])

# Add middleware for error handling
middleware = Middleware(ErrorHandlerMiddleware)
app.add_middleware(middleware)

# Create Falcon app
falcon_app = API()
falcon_app.add_route('/', SimpleResource())

# Run the ASGI application
if __name__ == "__main__":
    from starlette.config import Config
    config = Config(".env")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(config("PORT", 8000)))

# To run the app with WSGI server, uncomment the following lines:
# from wsgiref.simple_server import make_server
# server = make_server("0.0.0.0", 8000, WSGIMiddleware(app))
# server.serve_forever()