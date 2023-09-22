# 이은지 6-gram.?

import os
from collections import Counter
from functools import reduce
class Count():
    def __init__(self, parent = None, openAction=None):
        super(Count, self).__init__()
        self.main()

    def is_substring(self,small, big):
        return small in big


    def merge_lists2(self, ngrams):
        new_list = []
        merged_list = []
        for ngram in ngrams :
            for i in range(len(ngram) - 1):  # 마지막 문자열은 다음 문자열이 없으므로 제외
                first_string = ngram[i][1:]  # 첫 문자 제외
                second_string = ngram[i + 1][:-1]  # 마지막 문자 제외

                if first_string == second_string:
                    merged_word = ngram[i][0] + first_string + ngram[i + 1][-1]
                    merged_list.append(merged_word)

            new_list.append(merged_list)



    def extract_common_ngram(self, file_paths, n):
        ngram_sets = []

        self.ngrams = []
        for file_path in file_paths:
            ngrams2 = []
            with open(file_path, 'rb') as file:
                content = file.read()
                self.hex_values = content.hex()
                for i in range(len(self.hex_values) - n + 1):
                    ngram = self.hex_values[i:i + n]
                    ngrams2.append(ngram)

            self.ngrams.append(ngrams2)


    def find_duplicates_count(self):

        sets = [set(lst) for lst in self.ngrams]

        # reduce를 사용하여 여러 set의 교집합을 구함
        intersection_set = reduce(lambda x, y: x & y, sets)

        return list(intersection_set)




    def extract_2rengram(self, result):

        intersection_lists =[]

        for ngram in self.ngrams: #ngram은 초기에 뽑은 각 파일의 ngram
            intersection_list = []
            for onegram in ngram:
                for a in result :  #중복이 없는 교집합 리스트
                    if a in onegram:
                        intersection_list.append(a)

            intersection_lists.append(intersection_list)



        return intersection_lists

    def extract_3rengram(self, intersection_lists):
        sumvalue = 1
        result_list = []
        templist = {}
        longest = len(self.find_longest_sublist(intersection_lists))
        for i in range(1,len(intersection_lists)+1):
            sumvalue *= i*2+1


        for j in range(len(intersection_lists[2])):


            count = 0



            for i in range(len(intersection_lists)):
                try:
                    now = intersection_lists[i][j]
                    if now in templist:
                        templist[now] *= ((i+1)*2)+1
                    else :
                        templist[now] = ((i+1)*2)+1

                    for key, value in templist.items():
                        if value == sumvalue:
                            result_list.append(key)
                            del templist[key]

                except Exception as e:
                    print(e)
                    lasttemp = templist
                    pass



        return result_list

    def find_longest_sublist(self, double_list):
        max_length = 0
        longest_sublist = []

        for sublist in double_list:
            if len(sublist) > max_length:
                max_length = len(sublist)
                longest_sublist = sublist

        return longest_sublist

    def main(self):

        folder_path = "happy"
        self.n5gram =[]
        self.n6gram =[]
        self.n7gram=[]
        self.ngrams = []
        # 폴더 내의 모든 파일 경로 가져오기
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        n = 8

        # 공통으로 나타나는 n-gram 추출

        self.extract_common_ngram(file_paths, n)
        # 공통으로 나타나는 n-gram 출력
        print(f"공통적으로 나타나는 {n}-gram:")
        for ngram in self.ngrams:
            print(ngram)

        f = open('text.txt', 'w')
        f.write(str(self.ngrams))
        f.close()
        # #빈도수가 가장 높은 n-gram 출력
        # print(f"\n빈도수가 가장 높은 {n}-gram:")
        # for ngram, count in sorted_ngrams:
        #     if count > 2 :
        #         #print(''.join(ngram), count)
        #         pass
        # print()


        #merged_list = self.merge_ngram_lists(self.n5gram, self.n6gram, self.n7gram)

        # 결과 출력
        # print("병합된 n-gram 리스트:")
        # for ngram in merged_list:
        #     if len(ngram) == 10 :
        #         print(ngram)

        common_ngrams = list(self.ngrams)
        common_ngrams2 = self.find_duplicates_count()



        selective = self.extract_2rengram(common_ngrams2)

        f = open('text2.txt', 'w')
        f.write(str(common_ngrams2))
        f.close()

        #templist = self.extract_3rengram(selective)

        # merge_selective = self.merge_lists2(selective)
        #
        # # f = open('text2.txt', 'w')
        # # f.write(str(selective))
        # # f.close()
        #
        # print(merge_selective)




if __name__ == '__main__':

    Count()