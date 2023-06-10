from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel


class Hoteis(Resource):

    query_params = reqparse.RequestParser()
    query_params.add_argument("cidade", type=str, default="", location="args")
    query_params.add_argument("estrelas_min", type=float, default=0, location="args")
    query_params.add_argument("estrelas_max", type=float, default=0, location="args")
    query_params.add_argument("diaria_min", type=float, default=0, location="args")
    query_params.add_argument("diaria_max", type=float, default=0, location="args")


    def get(self):
        filters = Hoteis.query_params.parse_args()

        query = HotelModel.query

        if filters["cidade"]:
            query = query.filter(HotelModel.cidade == filters["cidade"])
        if filters["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(HotelModel.diaria <= filters["diaria_max"])

        return {"hoteis": [hotel.json() for hotel in query]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='Nao deixe o campo em branco')
    argumentos.add_argument('estrelas', type=float, required=True, help='Nao deixe o campo em branco')
    argumentos.add_argument('diaria', type=float, required=True, help='Nao deixe o campo em branco')
    argumentos.add_argument('cidade', type=str, required=True, help='Nao deixe o campo em branco')
    argumentos.add_argument('site_id', type=int, required=True, help='Nao deixe o campo em branco')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel não encontrado.'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id "{}" ja existe'.format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel= HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return { 'message ' : 'O hotel precisa estar associado a um hotel valido'}, 400
        try:
            hotel.save_hotel()
        except:
            return {'message' : 'Erro interno ao tentar salvar hotel'}, 500
        return hotel.json(), 200

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message' : 'Erro interno ao tentar salvar hotel'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Erro interno ao tentar deletar hotel'}, 500
            return {'message': 'Hotel deletado.'}, 200
        return {'message': 'Hotel nao encontrado.'}, 404
