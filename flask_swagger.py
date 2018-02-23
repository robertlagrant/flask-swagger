from flask import current_app, Flask, jsonify
from swagger_parser import SwaggerParser

class FlaskSwagger(object):

    def __init__(self, app=None, swagger_file=None):
        self.app = app
        if app is not None:
            self.init_app(app, swagger_file=swagger_file)
    

    # Resolves in this order:
    # - full example on endpoint's first response
    # - individual fields on endpoint
    # - full example on model
    # = individual fields on model
    def resolve_example(self, method_config):

        def responder():
            # Prep
            if 'responses' in method_config:
                first_response_code = sorted([key for key in method_config['responses']])[0]
            
            # First option
            if 'responses' in method_config and 'examples' in method_config['responses'][first_response_code]:
                top_response = method_config['responses'][first_response_code]['examples']['application/json']
            


                return jsonify(top_response)
        
        return responder
    

    def default_http_responder(self, path, method, method_config):

        def responder():
            print(method_config)
            print("Finding example for " + method + " " + path)
            #print(self.parser.get_send_request_correct_body(path, method))
            return "Time to implement stuff, lazy!"
        
        return responder


    def init_app(self, app, swagger_file=None):
        if not swagger_file:
            raise Exception('Swagger file not specified')
        
        with open(swagger_file) as f:
            swagger_yaml = f.read()
        
        if not swagger_yaml:
            raise Exception('No swagger found')
    
        self.parser = SwaggerParser(swagger_yaml=swagger_yaml)

        for path, path_config in self.parser.paths.items():
            for method, method_config in path_config.items():
                found = False
                for rule in app.url_map.iter_rules():
                    if rule.rule == path and method in rule.methods:
                        found = True
                
                if not found:
                    print("Warning: spec route not implemented; using example from Swagger: " + method.upper() + " " + path)

                    app.add_url_rule(path, path+method, self.resolve_example(method_config), methods=[method])


if __name__== "__main__":

    app = Flask(__name__)

    FlaskSwagger(app, "swagger.yaml")

    from waitress import serve

    serve(app, host='0.0.0.0', port=5000)

    # print()
    # for rule in app.url_map.iter_rules():
    #     print(dir(rule))
    #     print()
    #     print(rule, rule.rule, rule.methods)
    

    