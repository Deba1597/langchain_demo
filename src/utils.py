import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        # print(quiz_str.split('=')[1])
        # quiz_str = quiz_str.split('=')[1]
        quiz_dict=json.loads(str(quiz_str))

        data_dict=[]
        
        # iterate over the quiz dictionary and extract the required information
        for question_id, question_data in quiz_dict.items():
            mcq = question_data['mcq']
            OptionA = question_data['options']['a']
            OptionB = question_data['options']['b']
            OptionC = question_data['options']['c']
            OptionD = question_data['options']['d']
            CorrectAnswer = question_data['correct']
                                
            data_dict.append({'Question':mcq,'A':OptionA,'B':OptionB,'C':OptionC,'D':OptionD,'ANS':CorrectAnswer})
        return data_dict
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False