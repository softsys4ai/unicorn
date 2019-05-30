from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

class Workload(object):
    """This class is used to initialize workload
    """
    def __init__(self,
                 logger,
                 model_name,
                 row,
                 col):
        self.logger=logger
        self.logger.info("[STATUS]: Initializing SetWorkload Class")
        self.model_name=model_name
        self.load_model() 
        self.row=row
        self.col=col
 
    def load_model(self):
        """This function is used to load pretrained model
        """      
        try:           
            # resnet50 
            if self.model_name=="resnet50":
                from keras.applications import ResNet50
                from keras.applications.resnet50 import preprocess_input 
                self.preprocess=preprocess_input
                self.model=ResNet50()
            # vgg16
            elif self.model_name=="vgg16":
                from keras.applications import VGG16
                from keras.applications.vgg16 import preprocess_input
                self.preprocess=preprocess_input
                self.model=vgg16()
            # vgg19
            elif self.model_name=="vgg19":
                from keras.applications import VGG19
                from keras.applications.vgg19 import preprocess_input
                self.preprocess=preprocess_input
                self.model=vgg19()
            
            # xception
            elif self.model_name=="xception":
                from keras.applications import Xception
                from keras.applications.xception import preprocess_input
                self.preprocess=preprocess_input
                self.model=Xception()
           
            # inceptionv3
            elif self.model_name=="inceptionv3":
                from keras.applications import InceptionV3
                from keras.applications.inception_v3 import preprocess_input
                self.preprocess=preprocess_input
                self.model=InceptionV3()
            
            # mobilenetv2
            elif self.model_name=="mobilenet":
                from keras.applications.mobilenetv2 import MobileNetV2
                from keras.applications.mobilenetv2 import preprocess_input
                self.preprocess=preprocess_input
                self.model=MobileNetV2()
            else:
                self.logger.error("[ERROR]: invalid model")
               
        
        except Exception as e:
            self.logger.error("[ERROR]: workload model load failed due to {0}".format(str(e)))    
    
    def get_workload_params(self,
                     td):
        """This function is used to preprocess test data
        @returns:
            s: size
            td: test data
            model: pretrained model
        """        
        # preprocess
        try:
            self.model, self.preprocess
        except NameError:
            self.logger.error("[ERROR]: necessary variable not defined")
        else:
                
            td=load_img(td,target_size=(self.row,self.col))
            s=str(self.row)+"x"+str(self.col)
            td =img_to_array(td)
            td =td.reshape((1, td.shape[0], td.shape[1], td.shape[2]))
            td=self.preprocess(td)
              
            return (s,td, self.model)
        
