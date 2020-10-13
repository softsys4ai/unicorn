import numpy as np
class Workload(object):
    """This class is used to initialize workload
    """
    def __init__(self):
        print ("[STATUS]: Initializing Image Class") 
 
    def get_image_params(self):
        """This function is used to load pretrained model"""      
        try:           
               # xception          
                from tensorflow.keras.models import load_model
                from tensorflow.keras.datasets import cifar10 
                (_, _), (x_test, _) = cifar10.load_data() 
                x_test = (x_test / 255.0).astype(np.float32) 
                model=load_model('Xception.h5')
                return model, x_test
        except Exception as e:
            print("[ERROR]: Xception model load failed due to {0}".format(str(e)))    
    
         
