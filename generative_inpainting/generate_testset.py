import cv2
import os


class TestSet:
    def __init__(self, obj):
        self.SAMPLE_SET_DIRECTORY_NAME = obj["sample_set_directory"]
        self.TEST_SET_DIRECTORY_NAME = obj["test_set_directory"]
        self.TEST_SET_RAW_DIRECTORY_NAME = obj["test_set_raw_directory"]

        self.DIR_ABSPATH = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.SAMPLE_SET_ABSPATH = self.DIR_ABSPATH + self.SAMPLE_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_ABSPATH = self.DIR_ABSPATH + self.TEST_SET_DIRECTORY_NAME + "/"
        self.TEST_SET_RAW_ABSPATH = self.TEST_SET_ABSPATH + self.TEST_SET_RAW_DIRECTORY_NAME + "/"

        self.MASKSIZE_OPTIONS = obj["masksize_options"]

        self.SAMPLE_FILE_FORMAT = obj["raw_file_format"]

    def get_sample_files(self):
        if not os.path.isdir(self.SAMPLE_SET_ABSPATH):
            print("raw data set cannot found")
            return []

        file_list = []
        for file in os.listdir(self.SAMPLE_SET_ABSPATH):
            if self.SAMPLE_FILE_FORMAT in file:
                file_list.append(file)

        print("sample files : ", file_list)

        return file_list

    def create_testset_directories(self, mask_info):
        # create main directory for test set
        try:
            if not os.path.isdir(self.TEST_SET_ABSPATH):
                os.mkdir(self.TEST_SET_ABSPATH)
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                print("Failed to create testset directory.")
                raise

        # create sub directory for raw test set
        try:
            if not os.path.isdir(self.TEST_SET_RAW_ABSPATH):
                os.mkdir(self.TEST_SET_RAW_ABSPATH)
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                print("Failed to create testset directory.")
                raise

        # create sub directories for each mask size
        for subdir_name, mask_size in mask_info:
            dir_path = self.TEST_SET_ABSPATH + subdir_name
            try:
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
            except OSError as e:
                if e.errno != e.errno.EEXIST:
                    print("Failed to create mask sub directory.")
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
            dir_name = height + " * " + width
            ret.append([dir_name, (int(height), int(width))])

        return ret

    def get_mask_img(self, mask_size, img_shape):
        import numpy as np

        img_h, img_w, img_c = img_shape
        mask_h, mask_w = mask_size
        mask_start = (int((img_w - mask_w) / 2), int((img_h - mask_h) / 2))
        mask_end = (int((img_w + mask_w) / 2), int((img_h + mask_h) / 2))
        color = (255, 255, 255, 255)

        mask_img = np.zeros(img_shape)
        mask_img = cv2.rectangle(mask_img, mask_start, mask_end, color, cv2.FILLED)

        return mask_img

    def get_input_img(self, raw_img, mask_img):
        input_img = raw_img + mask_img
        return input_img

    def generate_testset(self):
        mask_info = self.parse_mask_info(self.MASKSIZE_OPTIONS)

        self.create_testset_directories(mask_info)

        sample_files = self.get_sample_files()

        for sample_file in sample_files:
            case_name = sample_file[0:sample_file.find("_") + 1]
            raw_img = cv2.imread(self.SAMPLE_SET_ABSPATH + sample_file, cv2.IMREAD_UNCHANGED)

            # create raw files in raw directory
            cv2.imwrite(os.path.join(self.TEST_SET_RAW_ABSPATH, case_name + "raw.png"), raw_img)

            for subdir_name, mask_size in mask_info:
                dir_path = self.TEST_SET_ABSPATH + subdir_name
                mask_img = self.get_mask_img(mask_size, raw_img.shape)
                input_img = self.get_input_img(raw_img, mask_img)

                # create mask files in each sub directory
                cv2.imwrite(os.path.join(dir_path, case_name + "mask.png"), mask_img)

                # create input files in each sub directory
                cv2.imwrite(os.path.join(dir_path, case_name + "input.png"), input_img)


if __name__ == "__main__":
    import yaml

    obj = yaml.safe_load(open('generate.yml', 'r'))

    TestSet(obj).generate_testset()
