from flask import current_app, Flask
from swagger_parser import SwaggerParser

class FlaskSwagger(object):

    def __init__(self, app=None, swagger_file=None):
        self.app = app
        if app is not None:
            self.init_app(app, swagger_file=swagger_file)


    def init_app(self, app, swagger_file=None):
        if not swagger_file:
            raise Exception('Swagger file not specified')
        

    
        self.parser = SwaggerParser(swagger_path=swagger_file)
        self.paths = self.parser.get_paths_data()

        print(self.paths)



if __name__== "__main__":

    app = Flask(__name__)

    FlaskSwagger(app, "C:\\repos\\flask-swagger\\swagger.yaml")