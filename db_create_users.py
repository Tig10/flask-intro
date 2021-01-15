from project import db
from project.models import User

# insert data
db.session.add(User('tig', 'tig@python.org', 'I\'ll-never-tell'))
db.session.add(User('admin', 'admin@admin.com', 'admin'))

# commit the changes
db.session.commit()