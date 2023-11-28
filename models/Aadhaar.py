#With image invert (Final)
import cv2
import pytesseract
import re
import urllib.request
import numpy as np
import config

# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
class Aadhaar_OCR:
    def __init__(self, img_path):
        self.user_aadhaar_no = str()
        self.user_gender = str()
        self.user_dob = str()
        self.user_name = str()

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
#         gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
#         _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        sharpened = cv2.addWeighted(resized_image, 2, cv2.GaussianBlur(resized_image, (0, 0), 10), -0.5, 0)


        #invert
#         inverted_image = cv2.bitwise_not(sharpened)
        text = pytesseract.image_to_string(sharpened,lang="hin+eng")
#         print(text)

        all_text_list = re.split(r'[\n]', text) 
        #text process
        text_list = list()
        for i in all_text_list:
            if re.match(r'^(\s)+$', i) or i == '':
                continue
            else:
                text_list.append(i)
#         text_list

                
                
#         aadhaar_no_pat = r'^[0-9]{4}\s[0-9]{4}\s[0-9]{4}$'
        aadhaar_no_pat = r"(\d{4} \d{4} \d{4})"
#         no = re.search(aadhaar_no_pat, text)
#         num = no.group(1) if no else "None"
#         print("Aadhaar Card Number:", num)
        for i in text_list:
            if re.search(aadhaar_no_pat, i):
                self.user_aadhaar_no = i
            else:
                continue

        
        gender_pat = r'\b(male|female|MALE|FEAMALE|Male|Feamale)\b'
        for i in text_list:
            match = re.search(gender_pat, i, re.IGNORECASE)
            if match:
                self.user_gender = match.group(0).upper()
                break

        
        aadhaar_dob_pat = r'(Year|Birth|irth|YoB|YOB:|DOB:|DOB)'
        date_ele = str()
        index = -1  
        dob_idx = -1  
        for idx, i in enumerate(text_list):
            if re.search(aadhaar_dob_pat, i):
                index = re.search(aadhaar_dob_pat, i).span()[1]
                date_ele = i
                dob_idx = idx
            else:
                continue

        date_str = ''
        for i in date_ele[index:]:
            if re.match(r'\d', i):
                date_str = date_str + i
            elif re.match(r'/', i):
                date_str = date_str + i
            else:
                continue
        self.user_dob = date_str

        self.user_name = text_list[dob_idx - 1]
        
        return {
            "aadhaar_no": self.user_aadhaar_no,
            "gender": self.user_gender,
            "dob": self.user_dob, 
            "user_name": self.user_name
        }
        
    

# ocr = Aadhaar_OCR(r"https://res.cloudinary.com/gurukol/image/upload/v1688653743/aiw/aadhaar/aadhaar02_duwdke.jpg")

# extracted_data = ocr.extract_data()


# aadhaar_no, gender, dob, name = extracted_data
# print("Aadhaar Card No:", aadhaar_no)
# print("Gender:", gender)
# print("Date of Birth/YoB:", dob)
# print("Name:", name)
