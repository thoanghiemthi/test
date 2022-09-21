from adapter.api import create_app
from core import config


app = create_app(config_object=config)
app.run(
    debug=app.config['DEBUG'],
    host=app.config["FLASK_RUN_HOST"],
    port=int(app.config["FLASK_RUN_PORT"])
)
