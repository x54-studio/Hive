# app/routes/__init__.py
from app.routes.user_routes import user_routes
from app.routes.article_routes import article_routes
from app.routes.main_routes import main_routes  # For home route

def init_app(app):
    app.register_blueprint(main_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(article_routes)
