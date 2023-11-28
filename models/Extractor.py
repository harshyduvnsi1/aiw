import pytesseract
import re
import config

class Data_Extraction:
    def __init__(self,images):
      self.images=images
      pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
      # pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
      # pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
      
    #  first run this function 
    def extracted_text(self):
      extractedInformation=''
      for i in range(len(self.images)):
        extractedInformation += pytesseract.image_to_string(self.images[i])
      return extractedInformation

    def spliting_with_newline_char(self,extracted_Data):
      paragraphs = extracted_Data.split('\n\n')
      info=""
      for line in paragraphs:
        if "Amount Disc" in line:
          break
        info=info+line
        info+="\n"
      return info

    def remove_rows_witout_semicolon(self,list_):
      edited_paragraphs = list_.split('\n')
      final_para=[]
      for line in edited_paragraphs:
        if ":" not in line:
          continue
        final_para.append(line)
      return final_para

    def extract_key_value_pairs(self,data_list): 
      #giving partial output
      result = {}
      for item in data_list:
          if ":" in item:
              key, value = item.split(":", 1)
              key = key.strip()
              value = value.strip()
              result[key] = value
      return result

    def extracting_fields(self,s_info):
      dic={}
      for key,value in s_info.items():
        # dic={}
        if ":" in value:
          if "Ph" in value:
            string = value
            pattern = r'Ph:\s(.+)'
            match = re.search(pattern, string)
            if match:
                dic["Ph"] = match.group(1)
          elif "Bill Date" in value:
            string = value
            pattern = r'Bill Date:\s(.+)'
            match = re.search(pattern, string)
            if match:
                dic["Bill Date"] = match.group(1)

          elif "Consultant" in value:
            string = value
            pattern = r'Consultant:\s(.+)'
            match = re.search(pattern, string)
            if match:
                dic["Consultant"] = match.group(1)

          elif "Adm. Date" in value:
            string = value
            pattern = r'Adm. Date:\s(.+)'
            match = re.search(pattern, string)
            if match:
                dic["Adm. Date"] = match.group(1)

      return  dic

    def extracting_subdictonary_with_siglekv(self,s_info):
      dic_wsv={}
      for key,value in s_info.items():
        if ("Ph" in value or "Bill Date" in value or "Consultant" in value or "Adm. Date" in value):
          continue
        else:
          dic_wsv[key]=value

      return  dic_wsv 

    def extracting_subdictonary_with_multiplekv(self,s_info):
      sub_dic={}
      for key,value in s_info.items():
        if "Ph" in value or "Bill Date" in value or "Consultant" in value or "Adm. Date" in value:
          sub_dic[key]=value

      return  sub_dic

    def filter_value(self,value,filter):
      # s=""
      i=value.index(filter)
      s=value[:i]
      s=s.strip()
      return s

    def spliting_the_keys(self,dic_com):
      for key,value in dic_com.items():
        if "Ph" in value:
          value=self.filter_value(value,"Ph")
          dic_com[key]=value
        elif "Bill Date" in value:
          value=self.filter_value(value,"Bill Date")
          dic_com[key]=value
        elif "Consultant" in value:
          value=self.filter_value(value,"Consultant")
          dic_com[key]=value
        elif "Adm. Date" in value:
          value=self.filter_value(value,"Adm. Date")
          dic_com[key]=value
      return dic_com
    
    def combining_dic(self,dic1,dic2,dic3):
      dic=dic1 | dic2 | dic3
      return dic

    def final_function_combined(self,raw_data):
      info=self.spliting_with_newline_char(raw_data)
      info_l=self.remove_rows_witout_semicolon(info)
      info_d=self.extract_key_value_pairs(info_l)
      dic_3=self.extracting_fields(info_d)
      dic_1=self.extracting_subdictonary_with_siglekv(info_d)
      dic_comb=self.extracting_subdictonary_with_multiplekv(info_d)
      dic_2=self.spliting_the_keys(dic_comb)
      final_dic=self.combining_dic(dic_1,dic_2,dic_3)
      return final_dic

    def filter_total_billamount(self,Text):
      pattern = r"(?:Mrs|Mr)\.\s([A-Z\s]+)"
      Name = re.findall(pattern, Text)
      
      corporate_payable_pattern = r"Corporate Payable (\d+\.\d+)"
      corporate_payable_match = re.search(corporate_payable_pattern, Text)
      if corporate_payable_match:
          corporate_payable = float(corporate_payable_match.group(1))
      else:
          corporate_payable = None
      dic={
          'Name':Name[0].strip(),
          'Bill Amount':corporate_payable,
          'Corporate Payable':corporate_payable
      }
      return dic

    def extracting_footer(self,Text):
      data=self.spliting_with_newline_char(Text)
      dic_4=self.filter_total_billamount(data)
      return dic_4

    def combined_data(self):
      raw_header=self.extracted_text()
      f_dic=self.final_function_combined(raw_header)
      b_dic=self.extracting_footer(raw_header)
      final_dic=f_dic|b_dic
      return final_dic