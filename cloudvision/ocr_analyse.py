import urllib
import json
from django.conf import settings
import sys

"""
4 ways of ocr analysis:
analysis_ocr_from_urls, list of url that return JSON Data, ocr_field_nm has to be specified

analysis_ocr_from_json, JSON object that contains multiple objects containing OCR field, ocr_field_nm has to be specified

analysis_ocr_from_txts, list of plain text of OCR

analysis_ocr_from_files, list of local files that return JSON Data, ocr_field_nm has to be specified. 
Each file can contain only single OCR object and the format has to be the same
"""

# load NLP model
# Use settings.py global variable
nlp = settings.NLP


# get analysis that below 45000 words result
def process_ocr(ocr):
      global nlp
      # ocr = "Give it back! He pleaded 55 53535 66. dasda dasd!-"

      doc = nlp(ocr)
      # list of errors
      errors = []
      # total num of tokens not exist in the dictionary
      not_found = 0
      # total num of words
      total_words = 0
      # total num of chars
      total_chars = 0
      # total num of chars of errors
      total_chars_of_error_words = 0

      # list all not founds
      for token in doc:
         check = False
         # print(token.text, token.pos_)
         if token.pos_ == 'NUM':
            if not token.text.replace('.', '', 1).isdigit():
               total_words += 1
               total_chars += token.__len__()
               check = True
         elif token.pos_ == 'PUNCT' and len(token.text) > 1:
            total_words += 1
            total_chars += token.__len__()
            check = True
         elif token.pos_ not in ['NUM', 'PUNCT']:
            total_words += 1
            total_chars += token.__len__()
            check = True

         #Spacy 2.0 version: if token.text not in word_compare.vocab and check == True:
         #Spacy 3.0 version code
         if token.text not in settings.WORD_DICT and check == True:
            # print(token.text, token.pos_, (token.text in nlp.vocab))
            errors.append(token.text)
            not_found += 1
            total_chars_of_error_words += token.__len__()

      # OCR accuracy
      if total_words == 0:
         word_accuracy = 0
      else:
         word_accuracy = (1 - (not_found / float(total_words))) * 100
      word_accuracy = round(word_accuracy, 2)

      if total_chars == 0:
          char_accuracy = 0
      else:
          char_accuracy = (1 - (total_chars_of_error_words / float(total_chars))) * 100
      char_accuracy = round(char_accuracy, 2)

      return word_accuracy, char_accuracy, total_words, not_found, errors, total_chars, total_chars_of_error_words


# get analysis on large ocr that over 45000 words
def process_large_ocr(ocr):

    x = ocr.split(".")
    # 45000 limit
    total_num_chars = 0
    ocr_str_list = []
    result_str = ""
    for index in range(len(x)):
        if total_num_chars <= 45000 and (index < len(x) - 1):
            if x[index] != "":
                result_str = result_str + x[index] + "."
            total_num_chars += len(x[index])
        elif total_num_chars > 45000 or (index == len(x) - 1):
            if index == len(x) - 1:
                if x[index] != "":
                    result_str = result_str + x[index] + "."
            ocr_str_list.append(result_str)
            result_str = ""
            total_num_chars = 0

    avg_word_accuracy = 0
    avg_char_accuracy = 0
    sum_total_words = 0
    sum_not_found = 0
    sum_errors = []
    sum_total_chars = 0
    sum_total_chars_of_error_words = 0
    print("Large Ocr Found: %s Segements" % len(ocr_str_list))
    for index, ocr in enumerate(ocr_str_list):
        word_accuracy, char_accuracy, total_words, not_found, errors, total_chars, total_chars_of_error_words = process_ocr(ocr)
        print("Process %s of %s Segements" % (index + 1, len(ocr_str_list)))
        sum_total_words += total_words
        sum_not_found += not_found
        sum_total_chars += total_chars
        sum_total_chars_of_error_words += total_chars_of_error_words

        for error in errors:
            sum_errors.append(error)

    avg_word_accuracy = (1 - (sum_not_found / float(sum_total_words))) * 100
    avg_char_accuracy = (1 - (sum_total_chars_of_error_words / float(sum_total_chars))) * 100
    avg_word_accuracy = round(avg_word_accuracy, 2)
    avg_char_accuracy = round(avg_char_accuracy, 2)
    '''
    print("OCR Word Accuracy: ", avg_word_accuracy, "%")
    print("OCR Character Accuracy: ", avg_char_accuracy, "%")

    print("Total Words: ", sum_total_words)
    print("Total Characters: ", sum_total_chars)

    print("Total Errors: ", sum_not_found)
    print("Total Chars in Errors: ", sum_total_chars_of_error_words)
    '''
    # return results
    return avg_word_accuracy, avg_char_accuracy, sum_total_words, sum_not_found, sum_errors, sum_total_chars, sum_total_chars_of_error_words


# perform ocr anaylsis on given list file paths (files return JSON object)
def analysis_ocr_from_urls(urls, ocr_field_nm):
    ocr_list = []
    for url in urls:
        base_url = url
        if sys.version_info[0] == 2:
            f = urllib.urlopen(base_url)
        elif sys.version_info[0] == 3:
            request = urllib.request.Request(base_url)
            f = urllib.request.urlopen(request)

        data = f.read()
        data = json.loads(data)
        i = 0
        while i < len(ocr_field_nm):
            # dig into field of JSON data
            # if not ocr_field_nm[i] in data.key():
            #    return "field name not valid"
            data = data[ocr_field_nm[i]]
            i += 1
        ocr_list.append(data)
    # Perform OCR Analysis over ocr list
    result_list = analysis_ocr_from_txts(ocr_list)
    return result_list


# perform ocr anaylsis on given list file paths (files return JSON object)
def analysis_ocr_from_files(file_paths, ocr_field_nm):
    ocr_list = []
    # Load JSON data from file
    for file_path in file_paths:
        with open(file_path) as f:
            data = json.load(f)
            i = 0
            while i < len(ocr_field_nm):
                # dig into field of JSON data
                #if not ocr_field_nm[i] in data.key():
                #    return "field name not valid"
                data = data[ocr_field_nm[i]]
                i += 1
            ocr_list.append(data)

    # Perform OCR Analysis over ocr list
    result_list = analysis_ocr_from_txts(ocr_list)
    return result_list


# perform ocr anaylsis on given object from JSON.loads()
def analysis_ocr_from_json(json_data, ocr_field_nm):
    ocr_list = []
    #data = json.loads(json_data)
    data = json_data
    i = 0
    while i < len(ocr_field_nm):
        # dig into field of JSON data
        # if not ocr_field_nm[i] in data:
        #    return "field name not valid"
        try:
            data = data[ocr_field_nm[i]]
        except:
            result_list = []
            result = {}
            result["response"] = False
            result["ocr"] = ""
            result["word_accuracy"] = 0
            result["char_accuracy"] = 0
            result["total_words"] = 0
            result["not_found"] = 0
            result["errors"] = ""
            result["total_chars"] = 0
            result["total_chars_of_error_words"] = 0
            result_list.append(result)
            return result_list
        i += 1
    ocr_list.append(data)
    # Perform OCR Analysis over ocr list
    result_list = analysis_ocr_from_txts(ocr_list)
    return result_list


# perform ocr anaylsis on given list of strings
def analysis_ocr_from_txts(ocr_txts):
    result_list = []
    for ocr in ocr_txts:
        result = {}
        if len(ocr) <= 45000:
            word_accuracy, char_accuracy, total_words, not_found, errors, total_chars, total_chars_of_error_words = process_ocr(ocr)
        else:
            word_accuracy, char_accuracy, total_words, not_found, errors, total_chars, total_chars_of_error_words = process_large_ocr(ocr)

        #print("OCR Word Accuracy: ", word_accuracy, "%")
        # print("OCR Character Accuracy: ", char_accuracy, "%")
        result["response"] = True
        result["ocr"] = ocr
        result["word_accuracy"] = word_accuracy
        result["char_accuracy"] = char_accuracy
        result["total_words"] = total_words
        result["not_found"] = not_found
        result["errors"] = ','.join(errors)
        result["total_chars"] = total_chars
        result["total_chars_of_error_words"] = total_chars_of_error_words
        result_list.append(result)
    return result_list
