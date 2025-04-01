from .messages import messages_bp

def register_routes(app):
    app.register_blueprint(messages_bp)