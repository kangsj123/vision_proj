import os
import yaml

class Predict:
    def __init__(self, obj):
        self.SAMPLE_SET_DIRECTORY_NAME = obj["sample_set_directory"]
        self.TEST_SET_DIRECTORY_NAME = obj["test_set_directory"]
        self.TEST_SET_RAW_DIRECTORY_NAME = obj["test_set_raw_directory"]
        self.MODEL_PATH = obj["model_directory"]

        self.DIR_ABSPATH = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.SAMPLE_SET_ABSPATH = self.DIR_ABSPATH + self.SAMPLE_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_ABSPATH = self.DIR_ABSPATH + self.TEST_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_RAW_ABSPATH = self.TEST_SET_ABSPATH + self.TEST_SET_RAW_DIRECTORY_NAME + "/"
        self.MODEL_ABS_PATH = self.DIR_ABSPATH + self.MODEL_PATH

        self.MASKSIZE_OPTIONS = obj["masksize_options"]
    
    def run(self):
        input_image_name = 'case%i_input.png'
        mask_image_name = 'case%i_mask.png'
        output_image_name = 'case%i_output.png'
        file_sz = (int)(len(next(os.walk(self.TEST_SET_RAW_ABSPATH))[2])) 
        
        for mask in self.MASKSIZE_OPTIONS:
            path_to_test = self.TEST_SET_ABSPATH + mask + '/'

            for num in range(1, file_sz+1):
                input_image_path = " --image " + self.TEST_SET_ABSPATH + mask + '/' + input_image_name%num
                mask_image_path = " --mask " + self.TEST_SET_ABSPATH + mask + '/' + mask_image_name%num
                output_image_path = " --output " + self.TEST_SET_ABSPATH + mask + '/' + output_image_name%num
                model_path = " --checkpoint_dir " + self.MODEL_ABS_PATH
                #python3 test.py --image examples/places2/case4_input.png --mask examples/places2/case4_mask.png --output examples/places2/case4_output.png --checkpoint_dir model_logs/release_places2_256
                command = "python3 test.py" + input_image_path + mask_image_path + output_image_path + model_path
                #print(command)
                os.system(command)


if __name__ == '__main__':
    obj = yaml.safe_load(open('generate.yml', 'r'))
    Predict(obj).run()