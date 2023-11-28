import cv2
import pytesseract
import re
import urllib.request
import numpy as np

import config

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
class Pan_OCR:
    def __init__(self, img_path):
        self.user_no = str()

        self.img_name = img_path
    
    def extract_data(self):
        if self.img_name.startswith('http://') or self.img_name.startswith('https://'):
            with urllib.request.urlopen(self.img_name) as url:
                image_data = url.read()
            nparr = np.frombuffer(image_data, np.uint8)
            img= cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            img = cv2.imread(self.img_name)

            
        resized_image = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        sharpened = cv2.addWeighted(resized_image, 2, cv2.GaussianBlur(resized_image, (0, 0), 10), -0.5, 0)
        grayscale = cv2.cvtColor(sharpened, cv2.COLOR_RGB2GRAY)
        denoised_image = cv2.fastNlMeansDenoising(grayscale, h=10)

        text = pytesseract.image_to_string(denoised_image,lang="hin+eng")


        all_text_list = re.split(r'[\n]', text) 
        text_list = list()
        for i in all_text_list:
            if re.match(r'^(\s)+$', i) or i == '':
                continue
            else:
                text_list.append(i)

        pan_no_pat = r'[A-Z]{5}[0-9]{4}[A-Z]'
        for i in text_list:
            if re.search(pan_no_pat, i):
                self.user_no = i
            else:
                continue

        
        return [self.user_no]
        
    

# ocr = Pan_OCR(r"C:\Users\Dell\Downloads\pan_2.jpg")

# extracted_data = ocr.extract_data()


# no = extracted_data
# print("Pan No:", no[0])
