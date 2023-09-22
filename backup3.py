import os


class makecsv():
    def __init__(self, parent=None, openAction=None):
        super(makecsv, self).__init__()
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

    def extract_ngram(self, file_paths, n):
        ngram_sets = []
        self.ngrams_list = []
        for file_path in file_paths:

            with open(file_path, 'rb') as file:
                content = file.read()
                self.hex_values = content.hex()
                ngrams = []
                for i in range(len(self.hex_values) - n + 1):
                    ngram = self.hex_values[i:i + n]
                    ngrams.append(ngram)

            self.ngrams_list.append(ngrams)

    def lcs(self, X, Y):
        m = len(X)
        n = len(Y)

        # memoization table을 초기화한다.
        L = [[0] * (n + 1) for _ in range(m + 1)]

        # X[0..m-1]와 Y[0..n-1]의 LCS를 계산한다.
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

    def get_file_info(self, fname, dpath):
        print(dpath)
        x = self.extract_infos(dpath + f'/{fname}')
        return x

    def merge_lists2(self, ngram):
        count = 0
        new_list = []
        merged_list = []
        one_merged_list = []
        previous_gram = ''
        count2 = 0
        onecount = 0
        for onegram1 in ngram:

            previous_gram_2 = ''
            if previous_gram == onegram1:
                one_merged_list.append(onegram1)
                onecount += 1
                pass
            else:

                if count == 0:

                    previous_gram = onegram1
                    count += 1
                else:
                    lengh = (len(onegram1) - 1)
                    previous_gram_2 = previous_gram[-lengh:]
                    onegram_2 = onegram1[:-1]

                    if previous_gram_2 == onegram_2:
                        previous_gram = previous_gram + onegram1[-1]
                        count2 += 1
                    else:

                        previous_gram_2 = ''
                        if count2 != 0:
                            one_merged_list.append(previous_gram)

                            count = 0
                            count2 = 0
                        else:
                            one_merged_list.append(previous_gram)

                        previous_gram = onegram1
                if onecount == len(ngram) - 1:
                    one_merged_list.append(previous_gram)
                    break

                onecount += 1
        merged_list.append(one_merged_list)

        return merged_list

    def extract_infos(self, fpath):
        file_type = ""
        res = {}

        res['name'] = os.path.basename(fpath)

        fp = open(fpath, 'rb')
        buf = fp.read(100)

        check_opcode = self.mergelist

        # 데이터 추출
        count = 0
        for i in range(len(check_opcode[0]) + 1):
            for j in range(len(self.ngrams_list[0])):
                try:

                    nowvalue = self.ngrams_list[0][j]
                    if nowvalue in check_opcode[0][i]:
                        count += 1
                        pass
                    elif count != 0:
                        res[check_opcode[0][i]] = self.ngrams_list[0][j + len(nowvalue)]
                        count = 0


                except Exception:
                    if count != 0:
                        res[check_opcode[0][i - 1]] = 1
                    pass

        self.reres = res
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

        basenum = int(len(ngrams) * 0.7)

        result70 = [key for key, value in element_count.items() if value >= basenum]
        result100 = [key for key, value in element_count.items() if value >= int(len(ngrams))]

        # 중복이 없는 교집합 리스트
        return result100

    def main(self):
        folder_path = "happy"
        self.n5gram = []
        self.n6gram = []
        self.n7gram = []
        self.ngrams = []
        result = []
        # 폴더 내의 모든 파일 경로 가져오기
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        n = 8
        self.extract_ngram(file_paths, n)
        self.load_common()
        self.extract_2rengram(self.newlist)
        result = self.lcs_multiple_lists(self.intersection_lists)
        self.mergelist = self.merge_lists2(result)

        path = '/base'
        file_name = os.path.basename(path)
        dpath = os.path.dirname(path)

        # fp = open('feature_dict.csv', 'wt', encoding='utf-8')
        # fp.writelines(feature_dict + '\n')
        # fp.close()

        fp = open('123' + '_pe.csv', 'wt', encoding='utf-8')

        for path2 in file_paths:
            x = self.get_file_info(path2, 'C:\\Users\\SKKU-DF\\PycharmProjects\\AiFileDetector\\')  # 실제 임시파일명은 입력 X

        header = ','.join(x.keys())
        fp.write(header + '\n')
        count = 0

        data = ','.join([str(t) for t in x.values()])
        fp.writelines(data + '\n')
        csv_path = file_name + '.csv'

        return csv_path


if __name__ == '__main__':
    makecsv()