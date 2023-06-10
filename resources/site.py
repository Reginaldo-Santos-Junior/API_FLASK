from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message' : 'Site not found.'}, 404

    def post(self, url):
        if SiteModel.find_site(url):
            return {'message' : 'esse site já existe'}, 400
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message ' : 'Houve um erro interno ao tentar criar o site'}, 500
        return site.json(), 201

    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            try:
                site.delete_site()
            except:
                return {'message ' : 'Houve um erro interno ao tentar criar o site'}, 500
            return site.json(), 201
        return {'message' : 'Não existe este site'}, 404