import os
from collections import Counter

class Count():
    def __init__(self, parent = None, openAction=None):
        super(Count, self).__init__()
        self.main()

    def is_substring(self,small, big):
        return small in big

    def merge_lists(self, lists):
        result = []
        for lst in lists:
            merge_flag = True
            for item in lst:
                if any(self.is_substring(item, other_item) for other_lst in lists if other_lst != lst for other_item in
                       other_lst):
                    merge_flag = False
                    break
            if merge_flag:
                result.extend(lst)
        return result

    def merge_lists2(self, lists):
        merged_set = set()
        delete_items = set()

        for lst in lists:
            for item in lst:
                if any(item in other_set for other_set in merged_set):
                    delete_items.add(item)
                else:
                    merged_set.add(item)

        # 짧은 문자열을 삭제한 후, 남은 리스트들을 합쳐서 결과 리스트로 만듭니다.
        result = [item for lst in lists for item in lst if item not in delete_items]

        return result

    def extract_common_ngram(self, file_paths, n):
        ngram_sets = []

        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                content = file.read()
                hex_values = content.hex()
                ngrams = [hex_values[i:i + (2 * n)] for i in range(0, len(hex_values), 2 * n)]
                ngram_sets.append(set(ngrams))

        # 공통으로 나타나는 n-gram
        common_ngrams = set.intersection(*ngram_sets)

        # n-gram 빈도수
        ngram_counts = Counter()
        for ngrams in ngram_sets:
            ngram_counts.update(ngrams)

        # 빈도 높은 순 정렬
        sorted_ngrams = sorted(ngram_counts.items(), key=lambda x: x[1], reverse=True)

        return common_ngrams, sorted_ngrams

    # 파일 경로 설정

    def main(self):

        folder_path = "../unhappy"
        self.n5gram =[]
        self.n6gram =[]
        self.n7gram=[]
        # 폴더 내의 모든 파일 경로 가져오기
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        n_sizes = [11, 12, 13]

        for n in n_sizes:

            # 공통으로 나타나는 n-gram 추출
            common_ngrams, sorted_ngrams = self.extract_common_ngram(file_paths, n)

            # 공통으로 나타나는 n-gram 출력
            print(f"공통적으로 나타나는 {n}-gram:")
            for ngram in common_ngrams:
                print(''.join(ngram))

            #빈도수가 가장 높은 n-gram 출력
            print(f"\n빈도수가 가장 높은 {n}-gram:")
            for ngram, count in sorted_ngrams:
                if count > 2 :
                    print(''.join(ngram), count)
            print()

            if n==11:
                values = [item[0] for item in sorted_ngrams]
                self.n5gram =  values
            if n==12:
                values = [item[0] for item in sorted_ngrams]
                self.n6gram = values
            if n==13:
                values = [item[0] for item in sorted_ngrams]
                self.n7gram = values

        #merged_list = self.merge_ngram_lists(self.n5gram, self.n6gram, self.n7gram)

        # 결과 출력
        # print("병합된 n-gram 리스트:")
        # for ngram in merged_list:
        #     if len(ngram) == 10 :
        #         print(ngram)

        merged_list = self.merge_lists2([self.n5gram, self.n6gram, self.n7gram])
        print(merged_list)
if __name__ == '__main__':

    Count()