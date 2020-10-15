import cv2
import os
import time
import csv
import numpy as np
import PIL.Image as pilimg
import matplotlib.image as mpimg
import tensorflow as tf
from matplotlib import pyplot as plt

class TestMaskSize:
    def __init__(self, obj):
        print("generate.yml", obj, "\n")
        self.SAMPLE_SET_DIRECTORY_NAME = obj["sample_set_directory"]
        self.TEST_SET_DIRECTORY_NAME = obj["test_set_directory"]
        self.MODEL_PATH = obj["model_directory"]

        self.DIR_ABSPATH = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.SAMPLE_SET_ABSPATH = self.DIR_ABSPATH + self.SAMPLE_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_ABSPATH = self.DIR_ABSPATH + self.TEST_SET_DIRECTORY_NAME + "/"
        self.MODEL_ABS_PATH = self.DIR_ABSPATH + self.MODEL_PATH
        
        self.MASKSIZE_OPTIONS = obj["masksize_options"]

    def get_sample_files(self):
        if not os.path.isdir(self.SAMPLE_SET_ABSPATH):
            print("Sample data set('%s') cannot found. "%self.SAMPLE_SET_ABSPATH)
            print("You should set 'SAMPLE_DIRECTORY' properly from generate.xml file")
            return None

        file_list = []
        for file in os.listdir(self.SAMPLE_SET_ABSPATH):
            file_list.append(file)

        print("sample files : ", file_list)

        return file_list

    def create_testset_directories(self):
        # create main directory for test set
        try:
            if not os.path.isdir(self.TEST_SET_ABSPATH):
                os.mkdir(self.TEST_SET_ABSPATH)
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                print("Failed to create testset directory.")
                raise

    def parse_mask_info(self, source):
        import re

        # get name for sub directories and mask height, width
        ret = []    # [["10 * 10", (10, 10)], ["20 * 50", (20, 50)], ...]
        for mask in source:
            if len(mask.split('*')) != 2:
                print("The format of mask size is wrong : ", mask)
                continue
            height, width = re.sub(r"\s+", "", mask).split('*')
            ret.append([int(height), int(width)])

        return ret

    def get_mask_img(self, mask_h, mask_w, img_shape):
        import numpy as np

        img_h, img_w, img_c = img_shape
        mask_start = (int((img_w - mask_w) / 2), int((img_h - mask_h) / 2))
        mask_end = (int((img_w + mask_w) / 2), int((img_h + mask_h) / 2))
        color = (255, 255, 255, 255)

        mask_img = np.zeros(img_shape)
        mask_img = cv2.rectangle(mask_img, mask_start, mask_end, color, cv2.FILLED)

        return mask_img

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

    def get_input_img(self, raw_img, mask_img):
        input_img = raw_img + mask_img
        return input_img

    def run_test_command(self, input_file_path, mask_file_path, output_file_path):
        input_image_path = " --image " + input_file_path
        mask_image_path = " --mask " + mask_file_path
        output_image_path = " --output " + output_file_path
        model_path = " --checkpoint_dir " + self.MODEL_ABS_PATH
        #python3 test.py --image examples/places2/case4_input.png --mask examples/places2/case4_mask.png --output examples/places2/case4_output.png --checkpoint_dir model_logs/release_places2_256
        command = "python3 test.py" + input_image_path + mask_image_path + output_image_path + model_path
        #print(command)
        try:
            if os.system(command) != 0:
                raise Exception('command does not exist')
        except:
            print("command does not work")

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist")

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

    def save(self, cnt, psnr, ssim):
        # name = 'result' + str(cnt) + '.csv'
        with open('result.csv', 'w') as csvfile:
            resultwriter = csv.writer(csvfile, delimiter=',')
            resultwriter.writerow(self.MASKSIZE_OPTIONS)
            resultwriter.writerow(psnr)
            resultwriter.writerow(ssim)
    
    def run(self):
        start = time.time()

        sample_files = self.get_sample_files()[:500]
        if sample_files is None:
            return
        
        file_sz = len(sample_files)
        print("the number of images : ", file_sz)
        mask_info = self.parse_mask_info(self.MASKSIZE_OPTIONS)
        self.create_testset_directories()

        #set path
        mask_file_path = os.path.join(self.TEST_SET_ABSPATH, "mask.png")
        input_file_path = os.path.join(self.TEST_SET_ABSPATH, "input.png")
        output_file_path = os.path.join(self.TEST_SET_ABSPATH, "output.png")

        psnr_result = []
        ssim_result = []
        for height, width in mask_info:
            pnsr_sum = 0.0
            ssim_sum = 0.0
            cnt = 0
            for idx, sample_file in enumerate(sample_files):
                if cnt==500:
                    break
                print("mask size: "+ str(height) + "," + str(width) + " " + str(idx) + "th file")
                # read raw file
                raw_file_path = self.SAMPLE_SET_ABSPATH + sample_file
                raw_img = cv2.imread(raw_file_path, cv2.IMREAD_UNCHANGED)
                #cv2.imwrite(os.path.join(self.TEST_SET_ABSPATH, "raw.png"), raw_img)
                if len(raw_img.shape) != 3:
                    print("case ", str(idx + 1), " : the size of sample img shape ('%s') is not 3 "%sample_file)
                    continue

                # create mask file
                mask_img = self.get_mask_img(height, width, raw_img.shape)
                cv2.imwrite(mask_file_path, mask_img)

                # create input file
                input_img = self.get_input_img(raw_img, mask_img)
                cv2.imwrite(input_file_path, input_img)

                # run test command 
                self.run_test_command(input_file_path, mask_file_path, output_file_path)
                
                # evaluate
                img1 = np.array(pilimg.open(output_file_path))
                h,w,_ = img1.shape
                img2 = np.array(pilimg.open(raw_file_path))[0:h, 0:w,:]
                
                if img1.shape == img2.shape:
                    image1 = tf.image.convert_image_dtype(img1, tf.float32)
                    image2 = tf.image.convert_image_dtype(img2, tf.float32)
                    pnsr_sum += self.calculate_psnr(image1, image2)
                    ssim_sum += self.calculate_ssim(image1, image2)
                    cnt += 1
                else:
                    print("img1 shape : ", img1.shape)
                    print("img2 shape : ", img2.shape)
                    print("mismatch dimension")

                # delete file to reserve memory
                self.delete_file(input_file_path)
                self.delete_file(output_file_path)
                self.delete_file(mask_file_path)

            psnr_result.append(pnsr_sum/cnt)
            ssim_result.append(ssim_sum/cnt)
            self.save(cnt, psnr_result, ssim_result)
        # save result
        self.visualize(psnr_result, ssim_result)

        print("Total time taken:", time.time() - start)
                
if __name__ == "__main__":
    import yaml

    obj = yaml.safe_load(open('generate.yml', 'r'))

    TestMaskSize(obj).run()
