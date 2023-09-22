# 이은지 작업 중~

import os
from collections import Counter

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
        ngrams_list = []
        for file_path in file_paths:

            with open(file_path, 'rb') as file:
                content = file.read()
                self.hex_values = content.hex()
                ngrams = []
                for i in range(len(self.hex_values) - n + 1):
                    ngram = self.hex_values[i:i + n]
                    ngrams.append(ngram)

            ngrams_list.append(ngrams)

        return ngrams_list

    def find_duplicates_count(self, ngrams):

        duplicates = []

        element_count = {}

        # 모든 리스트에서 요소의 출현 횟수를 카운트
        for lst in ngrams:
            for item in lst:
                if item in element_count:
                    element_count[item] += 1
                else:
                    element_count[item] = 1

        # 출현 횟수가 2번 이상인 요소만을 선택

        basenum = int(len(ngrams)*0.7)

        result70 = [key for key, value in element_count.items() if value >= basenum]
        result100 = [key for key, value in element_count.items() if value >= int(len(ngrams))]

        #중복이 없는 교집합 리스트
        return result100


    def extract_2rengram(self, ngrams, result):

        intersection_lists =[]

        for ngram in ngrams: #ngram은 초기에 뽑은 각 파일의 ngram
            intersection_list = []
            for onegram in ngram:
                for a in result :  #중복이 없는 교집합 리스트
                    if a in onegram :
                        intersection_list.append(a)

            intersection_lists.append(intersection_list)



        return intersection_lists




    def main(self):

        folder_path = "happy"
        self.n5gram =[]
        self.n6gram =[]
        self.n7gram=[]
        # 폴더 내의 모든 파일 경로 가져오기
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        n = 8

        # 공통으로 나타나는 n-gram 추출
        common_ngrams = self.extract_common_ngram(file_paths, n)

        # 공통으로 나타나는 n-gram 출력
        print(f"공통적으로 나타나는 {n}-gram:")
        for ngram in common_ngrams:
            print(ngram)

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

        common_ngrams = list(common_ngrams)
        common_ngrams2 = self.find_duplicates_count(common_ngrams)
        selective = self.extract_2rengram(common_ngrams, common_ngrams2)

        f = open('text.txt', 'w')
        f.write(str(selective))
        f.close()

        # merge_selective = self.merge_lists2(selective)
        #
        # # f = open('text2.txt', 'w')
        # # f.write(str(selective))
        # # f.close()
        #
        # print(merge_selective)




if __name__ == '__main__':

    Count()