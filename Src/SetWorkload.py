from flask import Flask, request, jsonify
from Workload import Workload
import time
import json

class SetWorkload():
    """This class is used to set workload and run as a flask app
    after initialization. 
    """
    def __init__(self,logger,options):
        self.logger=logger
        self.app=self.create_app(options)
        self.app.run()
    
    def create_app(self,opt):
        """This function is used to create an app
        """
        app=Flask(__name__)
        
        if opt['software_system']=='DNN':
            swl=Workload(self.logger,
                         opt['properties']['model'],
                         opt['properties']['height'],
                         opt['properties']['width'])  
            (_,
             test_data, 
             model)=swl.get_workload_params(opt['properties']['cur_input'])
            model._make_predict_function()    
                           
        @app.route('/api',methods=['POST'])
        def predict():
            data=request.get_json(force=True)
            start=time.time() 
            output=model.predict(test_data)    
            duration=time.time()-start           
            return jsonify(json.dumps({'time':duration}))
                        
        return app 
