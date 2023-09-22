class Count2():
    def __init__(self, parent = None, openAction=None):
        super(Count2, self).__init__()
        self.main()

    def generate_ngrams(text, n):
        """문자열에서 n-gram 목록 생성하기"""
        return [text[i:i + n] for i in range(len(text) - n + 1)]

    def find_common_ngrams(s1, s2, s3, n):
        """세 문자열에서 공통 n-gram 찾기"""
        # 각 문자열에 대한 n-gram 생성


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
    def main(self):






if __name__ == '__main__':

    Count2()