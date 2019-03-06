import connexion


def hello():
    return {
        'message': 'hello world!'
    }


connexion_app = connexion.FlaskApp(__name__)
connexion_app.add_api('api.yaml')

if __name__ == '__main__':
    connexion_app.run(port=8080)
