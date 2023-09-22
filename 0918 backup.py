import csv
import os
import pickle
import re

import pandas as pd
import tensorflow as tf
from tensorflow.python.client import device_lib
from simhash import Simhash

device_lib.list_local_devices()

os.environ["CUDA_VISIBLE_DEVICES"]="1"
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

with tf.device('/GPU:0'):
    class makecsv():
        def __init__(self, parent = None, openAction=None):
            super(makecsv, self).__init__()
            self.main()

        def load_common(self):
            self.data_list2 = []
            self.newlist2 = []

            # 파일 열기
            with open('text2.txt', 'r') as file:
                # 파일의 각 줄을 반복하여 읽기
                for line in file:
                    # 줄의 시작과 끝의 대괄호 제거
                    cleaned_line = line.strip('')[1:-1]
                    # 쉼표로 분리
                    sub_list = cleaned_line.split(',')
                    # 메인 리스트에 추가
                    self.data_list2.append(sub_list)

            for a in sub_list:
                b = a.strip('" \'')
                self.newlist2.append(b)

            print(self.newlist2)

        def extract_ngram(self, n, file_paths):
            ngram_sets = []
            self.ngrams_list = []
            self.hex_lists=[]


            for file_path in file_paths:
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.hex_values = content.hex()
                    ngrams = []

                    for i in range(len(self.hex_values) - n + 1):
                        ngram = self.hex_values[i:i + n]
                        ngrams.append(ngram)


                self.hex_lists.append(self.hex_values)
                self.ngrams_list.append(ngrams)

        def lcs(self, X, Y):
            m = len(X)
            n = len(Y)

            # memoization table을 초기화한다.
            L = [[0] * (n + 1) for _ in range(m + 1)]

            # X[0..m-1]와 Y[0..n-1] LCS 계산
            for i in range(m + 1):
                for j in range(n + 1):
                    if i == 0 or j == 0:
                        L[i][j] = 0
                    elif X[i - 1] == Y[j - 1]:
                        L[i][j] = L[i - 1][j - 1] + 1
                    else:
                        L[i][j] = max(L[i - 1][j], L[i][j - 1])

            # LCS를 구축한다.
            index = L[m][n]
            lcs_list = [None] * index

            i = m
            j = n
            while i > 0 and j > 0:
                if X[i - 1] == Y[j - 1]:
                    lcs_list[index - 1] = X[i - 1]
                    i -= 1
                    j -= 1
                    index -= 1
                elif L[i - 1][j] > L[i][j - 1]:
                    i -= 1
                else:
                    j -= 1

            return lcs_list

        def lcs_multiple_lists(self, lists):
            if len(lists) < 2:
                raise ValueError("At least two lists are required")

            current_lcs = self.lcs(lists[0], lists[1])

            for lst in lists[2:]:
                current_lcs = self.lcs(current_lcs, lst)
                if not current_lcs:
                    return []

            return current_lcs

        def get_files_value(self):
            results = {}
            self.all_result = []
            self.count = -1
            # 폴더 내 모든 파일에 대해 수행
            for fname in self.file_paths:
                self.count += 1
                full_path = os.path.join(self.dpath, fname)
                if os.path.isfile(full_path):
                    results = self.extract_value(full_path)
                    self.all_result.append(results)


            return self.all_result

        def merge_lists2(self, ngram):
            count = 0
            new_list = []
            merged_list=[]
            one_merged_list = []
            previous_gram = ''
            count2 = 0
            onecount = 0
            for onegram1 in ngram :

                if previous_gram == onegram1 and onegram1 != '00000000':
                    one_merged_list.append(onegram1)
                    onecount += 1
                    pass
                else :

                    if count == 0:
                        previous_gram = onegram1
                        count += 1
                    else :
                        lengh = (len(onegram1) - 1)
                        previous_gram_2=previous_gram[-lengh:]
                        onegram_2 = onegram1[:-1]

                        if previous_gram_2 == onegram_2 and onegram1 != '00000000':
                            previous_gram = previous_gram+onegram1[-1]
                            #count2 += 1
                        else :
                            previous_gram_2 = ''
                            if count2 != 0 and onegram1 != '00000000':
                                one_merged_list.append(previous_gram)
                                count = 0
                                #count2 = 0
                            else :
                                if previous_gram != '00000000':
                                    one_merged_list.append(previous_gram)


                            previous_gram = onegram1
                    if onecount == len(ngram)-1:
                        if previous_gram != '00000000':
                            one_merged_list.append(previous_gram)
                        break

                    onecount += 1

            merged_list.append(one_merged_list)


            return merged_list
        def extract_value(self, fpath):
            file_type = ""
            res = {}
            self.reres = []
            self.ngrams_list[0] = [x for x in self.ngrams_list[0] if x != '00000000']
            res['name'] = os.path.basename(fpath)

            fp = open(fpath, 'rb')

            check_opcode = self.mergelist
            #mvalue = 0
            # 데이터 추출
            count = 0
            tempvalue = ''
            for i in range(len(check_opcode[0]) + 1):
                for j in range(len(self.ngrams_list[0])):
                    try:
                        nowvalue = self.ngrams_list[0][j]
                        headerfeat = check_opcode[0][i]
                        if nowvalue in headerfeat:
                            count += 1
                        elif count != 0:
                            lennowvalue = len(nowvalue)
                            testvalue = j+lennowvalue
                            for kn in range(testvalue, testvalue+(len(nowvalue)*2), lennowvalue):
                                tempvalue+=self.ngrams_list[self.count][kn]

                            res[check_opcode[0][i]] = tempvalue
                            tempvalue = ''
                            count = 0
                            #mvalue = j
                            #break

                    except Exception as e:
                        if count != 0:
                            res[check_opcode[0][i-1]] = 1

            self.reres.append(res)
            return res


        def extract_2rengram(self, result):
            self.intersection_lists = []

            for ngram in self.ngrams_list:  # ngram은 초기에 뽑은 각 파일의 ngram
                intersection_list = []
                for onegram in ngram:
                    for a in result:  # 중복이 없는 교집합 리스트
                         if a in onegram:
                            intersection_list.append(a)

                self.intersection_lists.append(intersection_list)

            return self.intersection_lists

        def find_duplicates_count(self):

            self.data_list = []
            self.newlist = []
            duplicates = []

            element_count = {}

            # 모든 리스트에서 요소의 출현 횟수를 카운트
            for lst in self.ngrams_list:
                for item in lst:
                    if item in element_count:
                        element_count[item] += 1
                    else:
                        element_count[item] = 1

            # 출현 횟수가 2번 이상인 요소만 선택
            basenum = int(len(self.ngrams_list)*0.7)

            result70 = [key for key, value in element_count.items() if value >= basenum]
            self.newlist = [key for key, value in element_count.items() if value >= int(len(self.ngrams_list))]
            with open("commonlist.pkl", "wb") as fw: #
                pickle.dump(self.newlist, fw)


            #중복이 없는 교집합 리스트


        def add_string_if_not_exists(self, filename, target_string):
            # 파일 읽기
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 문자열이 파일 내용에 없으면 추가
                if target_string not in content:
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(target_string)

            except Exception as e :
                with open(filename, 'a', encoding='utf-8') as file:
                    file.write(target_string)

        def feature_dictionary(self, hexa):

            array10 = []

            dictpkl = (self.extension, "_dict.pkl")
            with open(dictpkl, 'rb') as f:
                newdict = pickle.load(f)

            result = hexa


            for key, value in newdict.items():
                if value in result:
                    array10.append(str(key))

            self.sequencedem = array10

            self.sequencedem = ", ".join(self.sequencedem)
            self.sequencedem = self.simhash(self.sequencedem)

        def save_lists_of_10_to_csv(self, data_list, file_name):
            with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)

                row = [j for j in range(1, len(data_list[0])+1)]
                csv_writer.writerow(row)

                for row in data_list:
                    csv_writer.writerow(row)

        #value로 key찾기
        def find_key_by_value(self, dictionary, value):
            for key, val in dictionary.items():
                if val == value:
                    return key
            return None  # 해당 값과 일치하는 키가 없을 경우 None을 반환


        #Feature 딕셔너리 업데이트 or 딕셔너리 추가
        #기존 딕셔너리 없으면 생성, 있으면 업데이트
        def save_lists_of_10_to_csv_featuredict(self, data_list):
            data_list = data_list.split(",")
            data_list.remove('name')
            data_set = list(dict.fromkeys(data_list).keys())
            newdict= {}

            try:
                #기존 딕셔너리 사전 열기
                with open('mp4_dict.pkl', 'rb') as f:
                    newdict = pickle.load(f)
                #값이 기존 딕셔너리 value에 존재하지 않으면 추가

                if newdict:
                    last_key = max(newdict.keys())
                else:
                    last_key = 0

                for idata in data_set:
                    if idata not in newdict.values():
                        new_key = last_key + 1
                        newdict[new_key] = idata

                dictpkl = str(self.extension+ "_dict.pkl")
                with open(dictpkl, "wb") as fw:
                    pickle.dump(newdict, fw)

            except Exception as e:

                for i, item in enumerate(data_set, start=1):
                    newdict[i] = item

                dictpkl = str(self.extension+ "_dict.pkl")
                with open(dictpkl, "wb") as fw:
                    pickle.dump(newdict, fw)

            self.makearray(data_list, newdict)

        def make_features(self, input_str):
            """break the long input string into features, with length = 3
            """
            length = 3
            input_str = input_str.lower()
            out_str = re.sub(r'[^\w]+', '', input_str)
            return [out_str[i:i + length] for i in range(max(len(out_str) - length + 1, 1))]
        def simhash(self, input_str):
            features = self.make_features(input_str)
            return Simhash(features).value
        def headersimhash(self, input_list):
            string_result = ''.join(map(str, input_list))
            self.simhash(string_result)
        def makearray(self, featurelist, newdict):
            newlist2 = []

            newlist = []
            # 피쳐를 딕셔너리 사전의 10진수값에 매핑
            for item in featurelist:
                a = newdict.values()
                if item in newdict.values():
                    newlist.append(self.find_key_by_value(newdict, item))

            newlist2 =[self.file_paths]
            newlist2.append(newlist)

            with open("vectordb.pkl", "wb") as fw:

                pickle.dump(newlist2, fw)

        #def save_lists_of_10_to_csv_featuredict(self, data_list, file_name):

        def save_list_of_indivi_to_csv(self, data_list, file_name): #헤더를 csv에 저장하기

            with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                sub_strings = data_list.split(',')
                csv_writer.writerow(sub_strings)
        def file_exists(self, folder_path, filename):
            file_path = os.path.join(folder_path, filename)
            return os.path.isfile(file_path)

        def folderpath(self, folder_path):
            #folder_path = "unhappy"
            result = []
            # 폴더 내의 모든 파일 경로 가져오기
            self.file_paths = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    self.file_paths.append(os.path.join(root, file))
            self.dpath = 'C:\\Users\\SKKU-DF\\PycharmProjects\\AiFileDetector'
            self.extension = (self.file_paths[0].split('.'))[1]

        def extract_value_tocsv(self, choice):
            x = self.get_files_value()  # 실제 임시파일명은 입력 X
            header = ','.join(x[0].keys())
            if choice == 1 :
                extractvalue = str(self.extension+ "extractvalues_header.csv")#헤더추출용
                commonheader2csv = str(self.extension + "common2_header.csv")
                self.save_list_of_indivi_to_csv(header, commonheader2csv)
            elif choice == 2:#인풋파일들에 대한 value 추출
                extractvalue = str(self.extension+ "extractvalues.csv")

            fp = open(extractvalue, 'wt', encoding='utf-8')

            self.save_lists_of_10_to_csv_featuredict(header)


            fp.write(header + '\n')
            count = 0

            for k in range(len(x)):
                data = ','.join([str(t) for t in x[k].values()])
                fp.writelines(data + '\n')

            fp.close()

            return header
        def main(self):

            self.ngrams = []

            while True:
                print("메뉴를 선택하세요:")
                print("1. 항목 1")
                print("2. 항목 2")
                print("4. 종료")

                choice =2


                folder_path = os.getcwd()  # 폴더 경로
                filename = 'lcsdata.pkl'  # 확인하고 싶은 파일 이름

                a = self.file_exists(folder_path, filename)

                # folder_path = "unhappy"
                # result = []
                # # 폴더 내의 모든 파일 경로 가져오기
                # self.file_paths = []
                # for root, dirs, files in os.walk(folder_path):
                #     for file in files:
                #         self.file_paths.append(os.path.join(root, file))
                # self.dpath = 'C:\\Users\\SKKU-DF\\PycharmProjects\\AiFileDetector'
                # self.extension = self.file_paths[0]

                if choice == 1:#기준 피처를 만들기 위함, 10개 이내의 파일로 파일형식의 피처 생성

                    self.folderpath("unhappy")
                    if a==False: #lcs pkl 파일이 없으면 생성

                        n = 8
                        self.extract_ngram(n, self.file_paths)
                        pklname = str(self.extension + "ngramlist.pkl")
                        with open(pklname, "wb") as fw:
                            pickle.dump(self.ngrams_list, fw)

                        hexlistpkl = str(self.extension+ "hexlist.pkl")
                        with open(hexlistpkl, "wb") as fw:
                            pickle.dump(self.hex_lists, fw)

                        self.find_duplicates_count()
                        self.extract_2rengram(self.newlist)
                        result = self.lcs_multiple_lists(self.intersection_lists)

                        lcsdatapkl = str(self.extension+ "lcsdata(2).pkl")
                        with open(lcsdatapkl, "wb") as fw:
                            pickle.dump(result, fw)


                    else: #lcs pkl 파일이 있으면 열기
                        lcsdatapkl = str(self.extension+ "lcsdata(2).pkl")
                        with open(lcsdatapkl, 'rb') as f:
                            result = pickle.load(f)

                    self.mergelist = self.merge_lists2(result)

                    mergepkl = (self.extension+ "mergelist.pkl")
                    with open(mergepkl, "wb") as fw:
                        pickle.dump(self.mergelist, fw)

                    path = '/base'
                    file_name = os.path.basename(path)
                    dpath = os.path.dirname(path)

                    # fp = open('feature_dict.csv', 'wt', encoding='utf-8')
                    # fp.writelines(feature_dict + '\n')
                    # fp.close()

                    commonheadercsv = (self.extension+ "common_header.csv")
                    self.save_lists_of_10_to_csv(self.mergelist, commonheadercsv)
                    print(f"{filename} exists in {folder_path}")

                    #헤더딕셔너리(기존딕셔너리에 없으면 추가하기 위함)

                    header = self.extract_value_tocsv(choice)
                    headersave = header.replace('name,', '')
                    filename = str(self.extension+ 'header.txt')
                    self.add_string_if_not_exists(filename, headersave)


                    break


                elif choice == 2:

                    self.folderpath("inputfile")

                    n = 8
                    #for file_path in self.file_paths:

                    mergepkl = str(self.extension + "mergelist.pkl")
                    with open(mergepkl, 'rb') as f:
                        self.mergelist = pickle.load(f)


                    self.extract_ngram(n, self.file_paths)

                    inputngramspkl = str(self.extension+"inputngrams.pkl")
                    with open(inputngramspkl, "wb") as fw:
                        pickle.dump(self.ngrams_list, fw)

                    inputhexlist = str(self.extension+ "hexlist.pkl")
                    with open(inputhexlist, "wb") as fw:
                        pickle.dump(self.hex_lists, fw)

                    self.extract_value_tocsv(choice)

                    break



                elif choice == 4:
                    # 파일을 순서딕셔너리와 비교하여 1-2-3-4, 2-3-1-4 등 순서 리스트를 만들고, 이를 심해시화
                    with open('hexlist.pkl', 'rb') as f:
                        hexvalues = pickle.load(f)
                    self.feature_dictionary(hexvalues[2])
                    print(self.sequencedem)

                    break

                elif choice ==5:
                    print("종료")
                    break
                else:
                    print("잘못된 선택입니다. 다시 선택하세요.")





    if __name__ == '__main__':

        makecsv()