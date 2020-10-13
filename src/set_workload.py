import time
import json
from flask import Flask, request, jsonify
from cadet.workload import Workload
            
class SetWorkload():
    """This class is used to set workload and run as a flask app
    after initialization. 
    """
    def __init__(self, options):
        self.app=self.create_app(options)
        self.app.run()
    
    def create_app(self, opt):
        """This function is used to create an app
        """
        app=Flask(__name__)
        if opt['software_system']=='Image':
            swl=Workload()
            model, test_data = swl.get_image_params()
            model._make_predict_function()    
                           
        @app.route('/api',methods=['POST'])
        def predict():
            data=request.get_json(force=True)
            start=time.time() 
            output=model.predict(test_data)    
            duration=time.time()-start           
            return jsonify(json.dumps({'time':duration}))
                        
        return app 
