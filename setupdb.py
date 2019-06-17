from facelock import db, Usuario
import bcrypt

db.create_all()

senha = u"scp1234"
gabriel = Usuario('Gabriel', 'henriques.gabriel@outlook.com',  bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt()), True, True)
test = Usuario('Teste', 'teste@test.com',  bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt()), False, False)


db.session.add_all([gabriel, test])

db.session.commit()

#gabriel = Usuario.query.get(1)
#test = Usuario.query.get(2)

#senha = u"scp1234"
#gabriel.senha = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt())

#db.session.add(gabriel)
#db.session.add(test)
#
#db.session.commit()
