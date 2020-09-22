import os
import yaml
import numpy as np
import PIL.Image as pilimg
import matplotlib.image as mpimg
import tensorflow as tf
from matplotlib import pyplot as plt

class Evaluation:
    def __init__(self, obj):
        self.SAMPLE_SET_DIRECTORY_NAME = obj["sample_set_directory"]
        self.TEST_SET_DIRECTORY_NAME = obj["test_set_directory"]
        self.TEST_SET_RAW_DIRECTORY_NAME = obj["test_set_raw_directory"]

        self.DIR_ABSPATH = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.SAMPLE_SET_ABSPATH = self.DIR_ABSPATH + self.SAMPLE_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_ABSPATH = self.DIR_ABSPATH + self.TEST_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_RAW_ABSPATH = self.TEST_SET_ABSPATH + self.TEST_SET_RAW_DIRECTORY_NAME + "/"

        self.MASKSIZE_OPTIONS = obj["masksize_options"]

    def calculate_psnr(self, img1, img2, max=255):
        psnr = tf.image.psnr(img1, img2, max_val=max)

        with tf.Session() as sess:
            value = sess.run(psnr)  
        return value

    def calculate_ssim(self, img1, img2, max=255):
        ssim = tf.image.ssim(img1, img2, max_val=max)
        with tf.Session() as sess:
            value = sess.run(ssim)   
        return value
    
    def visualize(self, psnr, ssim):
        #psnr
        x_values = self.MASKSIZE_OPTIONS
        y_values = psnr
        plt.plot(x_values, y_values)
        plt.title('Image Inpainting Evaluation(PSNR) with Different Mask Size')
        plt.xlabel('Mask size')
        plt.ylabel('PSNR')
        plt.show()

        #ssim
        x_values = self.MASKSIZE_OPTIONS
        y_values = ssim
        plt.plot(x_values, y_values)
        plt.title('Image Inpainting Evaluation(SSIM) with Different Mask Size')
        plt.xlabel('Mask size')
        plt.ylabel('SSIM')
        plt.show()

    def evaluate(self):
        raw_image_name = 'case%i_raw.png'
        output_image_name = 'case%i_output.png'
        file_sz = (int)(len(next(os.walk(self.TEST_SET_RAW_ABSPATH))[2])) 
        psnr_result = []
        ssim_result = []
        for mask in self.MASKSIZE_OPTIONS:
            path_to_test = self.TEST_SET_ABSPATH + mask + '/'
            pnsr_sum = 0.0
            ssim_sum = 0.0
            for num in range(1, file_sz+1):
                raw_image_path = self.TEST_SET_RAW_ABSPATH + raw_image_name%num
                output_image_path = self.TEST_SET_ABSPATH + mask + '/' + output_image_name%num
                img1 = pilimg.open(raw_image_path)
                img2 = pilimg.open(output_image_path)
                image1 = tf.image.convert_image_dtype(np.array(img1), tf.float32)
                image2 = tf.image.convert_image_dtype(np.array(img2), tf.float32)
                pnsr_sum += self.calculate_psnr(image1, image2)
                ssim_sum += self.calculate_ssim(image1, image2)

            psnr_result.append(pnsr_sum/file_sz)
            ssim_result.append(ssim_sum/file_sz)

        self.visualize(psnr_result, ssim_result)

if __name__ == "__main__":
    obj = yaml.safe_load(open('generate.yml', 'r'))
    Evaluation(obj).evaluate()
    

