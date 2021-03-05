from csflask import create_app
from csflask import db
from csflask.models import current_app
from csflask.__init__ import db
app = create_app()
app.app_context().push()

print(app)
db.create_all()