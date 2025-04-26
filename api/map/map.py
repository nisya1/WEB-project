import requests
from flask import jsonify, session, make_response
from flask_restful import Resource, abort


class MapInfoApi(Resource):
    def get(self):
        server_address = 'http://geocode-maps.yandex.ru/1.x/?'
        api_key = '8013b162-6b42-4997-9691-77b7074026e0'
        image_api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        geocode = 'Петергофское шоссе, 51'
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"].replace(' ', ',')

            image_request = f'https://static-maps.yandex.ru/v1?ll={toponym_coodrinates}8&spn=0.016457,0.00619&apikey={image_api_key}'

            return jsonify({'cinema': {'address': toponym_address, 'coords': toponym_coodrinates, 'image': image_request}})
        else:
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)
