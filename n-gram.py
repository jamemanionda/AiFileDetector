# 이은지 작업 중~
import ast
import os
from collections import Counter

class Count():
    def __init__(self, parent = None, openAction=None):
        super(Count, self).__init__()
        self.main()

    def load_common(self):
        self.data_list = []
        self.newlist = []

        # 파일 열기
        with open('text2.txt', 'r') as file:
            # 파일의 각 줄을 반복하여 읽기
            for line in file:
                # 줄의 시작과 끝의 대괄호 제거
                cleaned_line = line.strip('')[1:-1]
                # 쉼표로 분리
                sub_list = cleaned_line.split(',')
                # 메인 리스트에 추가
                self.data_list.append(sub_list)

        for a in sub_list:
            b = a.strip('" \'')
            self.newlist.append(b)

        print(self.newlist)

    def is_substring(self,small, big):
        return small in big


    def merge_lists2(self, ngrams):
        count = 0
        new_list = []
        merged_list=[]
        one_merged_list = []
        previous_gram = ''
        for ngram in ngrams :
            count2 = 0
            for onegram in ngram :
                previous_gram_2=''

                if count == 0:
                    previous_gram = onegram
                    count += 1
                else :
                    lengh = (len(onegram) - 1)
                    previous_gram_2=previous_gram[-lengh:]
                    onegram_2 = onegram[:-1]
                    if previous_gram_2 == onegram_2:
                        previous_gram = previous_gram+onegram[-1]
                        count2 += 1
                    else :
                        previous_gram_2 = ''
                        if count2 != 0:
                            one_merged_list.append(previous_gram)
                        count2 = 0
            merged_list.append(one_merged_list)


        return new_list



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
    def longest_common_subsequence(self, s1, s2):
        m = len(s1)
        n = len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs_length = dp[m][n]
        lcs = [''] * lcs_length
        i = m
        j = n
        index = lcs_length - 1

        while i > 0 and j > 0:
            if s1[i - 1] == s2[j - 1]:
                lcs[index] = s1[i - 1]
                i -= 1
                j -= 1
                index -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return ''.join(lcs)




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

        self.ngrams = self.extract_common_ngram(file_paths, n)
        result=self.find_duplicates_count(self.ngrams)
        self.ngrams = self.extract_2rengram(result)
        common_subsequence = self.ngrams[0]
        for i in range(1, len(self.ngrams)):
            common_subsequence = self.longest_common_subsequence(common_subsequence, self.ngrams[i])

        print(common_subsequence)






if __name__ == '__main__':

    Count()