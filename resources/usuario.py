from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
import hmac
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

BLACKLIST = set()

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True)
atributos.add_argument('senha', type=str, required=True)


class User(Resource):

    def get(self, user_id):
        user = UsuarioModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'usuario não encontrado.'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UsuarioModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'user deletado.'}
        return {'message': 'user nao encontrado.'}, 404


class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {'message': "o Login '{}' ja existe".format(dados['login'])}, 404
        user = UsuarioModel(**dados)
        user.save_user()
        return {'message': 'Usuario criado com sucesso'}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UsuarioModel.find_by_login(dados['login'])
        if user and hmac.compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'Usuario ou senha invalido'}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return{'message':'Voce foi deslogado com sucesso'}, 200