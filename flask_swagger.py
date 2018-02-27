from flask import current_app, Flask, jsonify, request, abort
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
                example = method_config['responses'][first_response_code]['examples']['application/json']

                return jsonify(example)
        
        return responder

    
    def before_request(self):

        print("BEFORE A REQUEST", request)

        # print('Request method', type(request.method), request.method)
        # print('Request path', type(request.path), request.path)
        # print('Request query string', type(request.query_string), request.query_string)

        # if request.is_json:
        #     print('Request json', type(request.get_json()), request.get_json())
        # else:
        #     print("Request is not JSON")

        valid = self.validate_werkzeug_request(request)

        if not valid:
            abort(400)


    def validate_werkzeug_request(self, req):

        json_methods = set(['post', 'put', 'patch'])
        method = req.method.lower()

        if method in json_methods:
            if not req.is_json:
                raise Exception('A ' + method + ' call is not JSON. Check it has a body of well-formed JSON and the content-type is set to application/json')
            body = req.get_json()
        else:
            body = None

        return self.parser.validate_request(req.path, method, body=body)



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

                # print(app.url_map)
                for rule in app.url_map.iter_rules():
                    if rule.rule == path and method.upper() in rule.methods:
                        found = True
                        # print(dir(rule.map.iter_rules))
                
                if not found:
                    print("Warning: spec route not implemented; using example from Swagger: " + method.upper() + " " + path)

                    app.add_url_rule(path, path+method, self.resolve_example(method_config), methods=[method])
        
        app.before_request(self.before_request)


if __name__== "__main__":

    from waitress import serve

    app = Flask(__name__)

    @app.route('/pet/<pet_id>')
    def something(pet_id):
        return "This is from code"
    
    @app.route('/pet', methods=['POST'])
    def something_else():
        return 'valid'

    FlaskSwagger(app, "swagger.yaml")
    # serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000)
