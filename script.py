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

suffixes = "(adj\.|adv\.|pron\.|num\.|num\.-m|conj\.|part\.|aux\.|prep\.|n\.|v\.|m\.|phrw\.|\.\.\.)"
base_str1 = """<p style="text-align: center;"><span class="large">%s</span></p>"""
base_str2 = """<p style="text-align: center;"><span class="large">%s </span></p><p style="text-align: center;"><span class="large">%s</span></p>"""


def extract_suffix(word):
    # Return a pinyin that is like wordsfx. or fword swordsfx. as: ['word', 'sfx.'] or ['fword', 'sword', 'sfx.']
    regex = f'^(\w+?\s?\w+?\t?)((?:{suffixes}) .*)$'
    return re.sub(regex, "\\1#\\2", word, re.UNICODE).split("#")


def get_file_list(dir):
    """
    Return list of CSV files
    """
    files = list()
    for file in listdir(dir):
        if isfile(join(dir, file)) and file.endswith('.csv'):
            files.append((dir, file))
    return files


def read_file(file):
    result = list()
    filename = join(*file)
    print("Opening file: ", filename)
    with open(filename, encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        # skip header
        next(reader)
        for i, row in enumerate(reader, start=2):
            ch_letters = re.findall(r'[\u4e00-\u9fff]+', row[1])
            # log the line that doesn't match the format and exit
            if ch_letters:
                print(f'This line [{i}] in the file [{file[1]}] does not match the format')
                exit()
            spell_def = extract_suffix(row[1])
            result.append((base_str1 % row[0], base_str2 % (spell_def[0], spell_def[1])))
    return result


def write_file(file, data):
    with open(f'result/html-{file[1]}', 'w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output,)
        writer.writerow(['Question', 'Answer'])
        for row in data:
            writer.writerow([row[0], row[1]])


def main():
    files_dir = join('.', 'input-files')
    files = get_file_list(files_dir)

    for file in files:
        data = read_file(file)
        write_file(file, data)


if __name__ == '__main__':
    main()
