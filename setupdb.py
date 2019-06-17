from server import db, Usuario
import bcrypt

db.create_all()

#gabriel = Usuario('Gabriel', 'henriques.gabriel@outlook.com', 'scp1234')
#test = Usuario('Teste', 'teste@test.com', 'scp1234')

#db.session.add_all([gabriel, test])

# db.session.commit()

gabriel = Usuario.query.get(1)
test = Usuario.query.get(2)

#senha = u"scp1234"
#gabriel.senha = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt())
gabriel.is_admin = True
test.is_admin = False
db.session.add(gabriel)
db.session.add(test)

db.session.commit()
