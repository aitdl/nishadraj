from app.main import app
import json

routes = []
for route in app.routes:
    methods = getattr(route, "methods", None)
    path = getattr(route, "path", None)
    routes.append({"path": path, "methods": list(methods) if methods else None})

print(json.dumps(routes, indent=2))
