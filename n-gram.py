# 이은지 작업 중~

import os
from collections import Counter

class Count():
    def __init__(self, parent = None, openAction=None):
        super(Count, self).__init__()
        self.main()

    def is_substring(self,small, big):
        return small in big


    def merge_lists2(self, strings):
        merged_strings = []
        for string in strings:
            merge_flag = False
            for merged_string in merged_strings:
                if len(string) == len(merged_string) + 1 and string[1:] == merged_string:
                    merged_strings.remove(merged_string)
                    merged_strings.append(string)
                    merge_flag = True
                    break
                elif len(string) + 1 == len(merged_string) and string == merged_string[1:]:
                    merge_flag = True
                    break
            if not merge_flag:
                merged_strings.append(string)

        return merged_strings

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
 # 중복을 제거한 리스트를 저장할 빈 리스트


        return ngrams_list




    def find_and_add_strings(self, search_list):
        result_list = []
        original_str = self.hex_values
        i = 0  # 문자열에서 검색 시작 위치를 나타내는 인덱스
        while i < len(original_str):
            found = False
            for word in search_list:
                if original_str[i:i + len(word)] == word:
                    result_list.append(word)
                    i += 1
                    found = True
                    break
            if not found:
                i += 1

        return result_list
    # 파일 경로 설정

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
        common_ngrams, sorted_ngrams = self.extract_common_ngram(file_paths, n)

        # 공통으로 나타나는 n-gram 출력
        print(f"공통적으로 나타나는 {n}-gram:")
        for ngram in common_ngrams:
            print(ngram)

        #빈도수가 가장 높은 n-gram 출력
        print(f"\n빈도수가 가장 높은 {n}-gram:")
        for ngram, count in sorted_ngrams:
            if count > 2 :
                #print(''.join(ngram), count)
                pass
        print()


        #merged_list = self.merge_ngram_lists(self.n5gram, self.n6gram, self.n7gram)

        # 결과 출력
        # print("병합된 n-gram 리스트:")
        # for ngram in merged_list:
        #     if len(ngram) == 10 :
        #         print(ngram)

        common_ngrams = list(common_ngrams)
        common_ngrams = self.find_and_add_strings(common_ngrams)
        print(common_ngrams)




if __name__ == '__main__':

    Count()