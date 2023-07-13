from ..website import db

db.session.execute('ALTER DATABASE postgres REFRESH COLLATION VERSION;')
db.session.commit()
db.session.execute('ALTER DATABASE petsite REFRESH COLLATION VERSION;')
db.session.commit()