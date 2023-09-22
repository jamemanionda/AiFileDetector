
import ast
import os
from collections import Counter
class Count2():
    def __init__(self, parent = None, openAction=None):
        super(Count2, self).__init__()
        self.main()
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

    def preprocess_pattern(self, pattern):
        # 패턴의 각 문자와 그 위치를 저장하는 딕셔너리를 생성합니다.
        pattern_dict = {}
        for i, char in enumerate(pattern):
            if char not in pattern_dict:
                pattern_dict[char] = [i]  # 중복 문자의 위치를 리스트로 저장
            else:
                pattern_dict[char].append(i)  # 중복 문자의 위치를 추가
        return pattern_dict

    def find_common_pattern(self, strings):
        pattern_dicts=[]
        if not strings:
            return []

        # 각 문자열 리스트의 패턴 딕셔너리를 생성합니다.
        for onestring in strings:
            pattern_dicts.append([self.preprocess_pattern(onestring)])

        for string in strings[1:]:
            pattern_dicts.append(self.preprocess_pattern(string))

        # 모든 문자열 리스트에서 공통적으로 나타나는 패턴을 찾습니다.
        common_pattern = []
        for char in pattern_dicts[0]:
            if all(char in pattern_dict for pattern_dict in pattern_dicts):
                positions_lists = [pattern_dict[char] for pattern_dict in pattern_dicts]
                min_positions = min(positions_lists, key=len)
                common_pattern.extend([char] * len(min_positions))

        return common_pattern

    def merge_lists2(self, ngram):
        count = 0
        new_list = []
        merged_list=[]
        one_merged_list = []
        previous_gram = ''
        count2 = 0
        onecount = 0
        for onegram1 in ngram :

            previous_gram_2=''
            if previous_gram == onegram1:
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

                    if previous_gram_2 == onegram_2:
                        previous_gram = previous_gram+onegram1[-1]
                        count2 += 1
                    else :

                        previous_gram_2 = ''
                        if count2 != 0:
                            one_merged_list.append(previous_gram)

                            count = 0
                            count2 = 0
                        else :
                            one_merged_list.append(previous_gram)

                        previous_gram = onegram1
                if onecount == len(ngram)-1:
                    one_merged_list.append(previous_gram)
                    break

                onecount += 1
        merged_list.append(one_merged_list)


        return merged_list
    def main(self):

        folder_path = "unhappy"
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
    # 여러 문자열로 이루어진 리스트
        string_lists =self.find_duplicates_count(self.ngrams)
        string_lists = self.extract_2rengram(string_lists)
        print("string pattern:", string_lists)
        common_pattern = self.find_common_pattern(string_lists)
        print("Common pattern:", common_pattern)

        print(self.merge_lists2(common_pattern))

if __name__ == '__main__':

    Count2()