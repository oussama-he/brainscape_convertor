#################################################################
#  Created by Oussama  19th Jan 2021
#
#   modified by JLK
#
# This script convert a text.csv file to html.csv file for the website https://www.brainscape.com/
# source file in :  ./input-files/
# destination files: ./result/
#  usage : python script.py
#
################################################################


import csv
import re
from os import listdir
from os.path import isfile, join

suffixes = "(adj\.|adv\.|pron\.|num\.|num\.-m|conj\.|part\.|aux\.|prep\.|n\.|v\.|m\.|phrw\.|name\.)"
base_str1 = """<p style="text-align: center;"><span class="large">%s</span></p>"""
base_str2 = """<p style="text-align: center;"><span class="large">%s </span></p><p style="text-align: center;"><span class="large">%s</span></p>"""
base_str3 = """<p style="text-align: center;"><span class="large">%s </span></p><p style="text-align: center;"><span class="large">%s </span></p><p style="text-align: center;"><span class="large">%s</span></p>"""


def extract_suffix(word):
    """
    convert the "Answer row" into "pinyin", "word functions" and "translation"
    :param word:
    :return:
    """
    regex = f'^(\w+?\s?\w+?\t?)((?:{suffixes}) .*)$'
    return re.sub(regex, "\\1#\\2", word, re.UNICODE).split("#")

def write_html_file(filename,result):
    """
    this function will write the row from result list into the file and return a list
    :param filename: string
    :param result: list
    :return: list
    """
    with open(f'result/{filename}', 'w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output, )
        writer.writerow(['Question', 'Answer'])
        for row in result:
            writer.writerow([row[0], row[1]])
    #print("Wrote file: ", filename)
    result = list()
    return (result)

def convertor():
    """

    :return:
    """
    # Variable definition
    files = []
    files_dir = join('.', 'input-files')
    result = []

    # get the filename from the input directory an put it into a list called files
    for file in listdir(files_dir):
        if isfile(join(files_dir, file)) and file.endswith('.csv'):
            files.append((files_dir, file))

    # go thru the list of files
    for file in files:
        filename = join(*file)
        print("Opening file: ",filename)
        # open the file
        with open(filename, encoding='utf-8') as input_file:
            reader = csv.reader(input_file)
            # skip header like "Question,Answer", which will be added later
            next(reader)
            # go thru every line of the file
            for i, row in enumerate(reader, start=2):
                # Check that no chinese char in the "Answer" part
                #todo will have to be remove, and make sure it does not break the script: extract_suffix()
                ch_letters = re.findall(r'[\u4e00-\u9fff]+', row[1])
                if ch_letters:
                    print(f'This line [{i}] in the file [{file[1]}] does not match the format')
                    exit()
                # convert the "Answer row" into "pinyin", "word functions" and "translation"
                spell_def = extract_suffix(row[1])

                # Create the new string and
                #result.append((base_str1 % row[0], base_str2 % (spell_def[0], spell_def[1])))
                result.append((base_str1 % row[0], base_str3 % (spell_def[0], row[0], spell_def[1])))

        # write html file to the result folder
        result = write_html_file(file[1],result)


if __name__ == '__main__':
    convertor()