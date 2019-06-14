from server import db,Usuario

db.create_all()

gabriel = Usuario('Gabriel', 'henriques.gabriel@outlook.com', '123456')
test = Usuario('Teste', 'teste@test.com', '123456')

#db.session.add_all([gabriel,test])

#db.session.commit()

all_users = Usuario.query.all()

print(all_users)