from csflask import create_app
app = create_app()
app.app_context().push()
from csflask import db
db.create_all()