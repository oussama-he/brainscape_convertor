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
    :type word: str
    :param word: the answer row
    :rtype: list
    :return: Returns a list like: ['pinyin', 'suffix.', 'translation']
    """
    regex = f'^(\w+?\s?\w+?\t?)((?:{suffixes}) .*)$'
    return re.sub(regex, "\\1#\\2", word, re.UNICODE).split("#")


def write_html_file(filename,result):
    """
    this function will write the row from result list into the file
    :type filename: str
    :param filename: the name of the output file
    :type result: list
    :param result: The list of html strings
    """
    with open(f'result/{filename}', 'w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output, )
        writer.writerow(['Question', 'Answer'])
        for row in result:
            writer.writerow([row[0], row[1]])
    print("Wrote file: ", filename)


def make_html_strings(reader, file_path):
    """
    This function will return the html strings in a list of tuples
    :type reader: _csv.reader
    :param reader: A csv reader object
    :type file_path: tuple
    :param file_path: A tuple like this ('path', 'filename.csv')
    :rtype: list
    :return: The list of html strings
    """
    result = []
    # go thru every line of the file
    for i, row in enumerate(reader, start=2):
        # Check that no chinese char in the "Answer" part
        # todo will have to be remove, and make sure it does not break the script: extract_suffix()
        ch_letters = re.findall(r'[\u4e00-\u9fff]+', row[1])
        if ch_letters:
            print(f'This line [{i}] in the file [{file_path[1]}] does not match the format')
            exit()
        # convert the "Answer row" into "pinyin", "word functions" and "translation"
        spell_def = extract_suffix(row[1])

        # Create the new string and append to the result list
        result.append((base_str1 % row[0], base_str3 % (spell_def[0], row[0], spell_def[1])))
    return result


def convertor():
    """
    The main function, where we get the list of input files, read them one by one and write to output files
    """
    # Variable definition
    files = []
    files_dir = join('.', 'input-files')

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
            result = make_html_strings(reader, file)

        # write html file to the result folder
        write_html_file(file[1], result)


if __name__ == '__main__':
    convertor()
