from server import db,Usuario
import bcrypt

db.create_all()

gabriel = Usuario('Gabriel', 'henriques.gabriel@outlook.com', '123456')
test = Usuario('Teste', 'teste@test.com', '123456')

#db.session.add_all([gabriel,test])

#db.session.commit()

gabriel = Usuario.query.get(2)
senha = u"scp1234"
gabriel.senha = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt())

db.session.add(gabriel)

db.session.commit()