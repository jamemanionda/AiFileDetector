# 각 파일들에서 공통된 요소를 추출하는 것
import binascii
from collections import Counter


import os

class extractHex():
    def __init__(self, parent = None, openAction=None):
        super(extractHex, self).__init__()
        self.main()

    def extract_hex_patterns(self, hex_string, n):
        patterns = []
        lenvalue = len(hex_string)
        for i in range(len(hex_string) - n + 1):
            pattern = hex_string[i:i + n]
            patterns.append(pattern)

        sorted_patterns = Counter(patterns).most_common()

        return sorted_patterns

    def extract_hex_string_from_file(self,file_path):
        hex_string = ""

        with open(file_path, 'rb') as file:
            contents = file.read()
            hex_string = contents.hex()

        return hex_string

    def filter_strings(self,lst):
        min_length = min(len(tup[0]) for tup in lst)
        new_list = [(string, integer) for string, integer in lst if len(string) == min_length]

        for i in range(len(new_list)):
            string, _ = new_list[i]
            for j in range(len(new_list)):
                if i != j:
                    other_string, _ = new_list[j]
                    if string in other_string:
                        break
            else:
                continue
            break
        else:
            return new_list

        return [(string, integer) for string, integer in new_list if string in other_string]

    def find_strings_in_hex(self, file_path, search_strings):
        result = []
        with open(file_path, 'rb') as file:
            hex_data = binascii.hexlify(file.read()).decode()
            for search_string in search_strings:
                search_hex = binascii.hexlify(search_string.encode()).decode()
                index = 0
                while index < len(hex_data):
                    found_index = hex_data.find(search_hex, index)
                    if found_index == -1:
                        break
                    hex_value = hex_data[found_index + len(search_hex):found_index + len(search_hex) + 10]
                    result.append([search_string, hex_value])
                    index = found_index + len(search_hex)
        return result

    def main(self):
        # 대상 폴더 경로 지정
        folder_path = "../unhappy"

        # 폴더 내의 모든 파일 경로 가져오기
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        # 결과 저장할 리스트 초기화
        results = []
        self.newresults=[]
        # 파일별로 작업 수행
        for file_path in file_paths:
            hex_string = self.extract_hex_string_from_file(file_path)

            #n-gram
            n = 8
            result = self.extract_hex_patterns(hex_string, n)

            new_list = [tup for tup in result if tup[1] >= 5]
            new_list = self.filter_strings(new_list)

            list2 = [tup for tup in result if tup[1] >= 0]
            self.newresults.append(list2)
            results.append(new_list)

        # 공통된 키 추출
        all_keys = [key for result in results for key, _ in result]
        key_counts = Counter(all_keys)
        common_keys = [key for key, count in key_counts.items() if count >= 3]

        # 공통된 키 출력
        print(common_keys)

        print(self.newresults)

        newcounter = Counter()

        # 리스트들을 반복하면서 '문자열' 카운트
        for lst in self.newresults:
            newcounter.update(item[0] for item in lst)

        # Counter 객체에서 공통으로 나타나는 '문자열' 필터링
        common_strings = [string for string, count in newcounter.items() if count == len(self.newresults)]

        print("공통: ", common_strings)

        result = common_strings[0]  # 처음 n-gram을 결과에 추가

        # 다음 n-gram부터 반복
        for ng in common_strings[1:]:
            # 다음 n-gram이 현재 n-gram의 일부인지 확인
            if result.endswith(ng[:-1]):
                # 현재 n-gram에 다음 n-gram의 마지막 문자 추가
                result += ng[-1]
            else:
                # 새로운 연속된 n-gram 시작
                result += ', ' + ng

        print('결과 : ',result)



# 사용 예시
        file_path = '../Sample2_조작.m4a'  # 파일 경로
        search_strings = result[:10]  # 찾고자 하는 문자열들

        result = self.find_strings_in_hex(file_path, search_strings)
        print("마지막:",result)

if __name__ == '__main__':

    extractHex()