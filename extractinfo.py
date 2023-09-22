import os

#라벨 당 적용

class extractinfo():
    def __init__(self, parent=None, openAction=None):
        super(extractinfo, self).__init__()
        self.main()

    def get_files_info(self):
        results = {}
        self.all_result = []
        self.count = -1
        # Iterate over each file in the directory
        for fname in self.file_paths:
            self.count += 1
            full_path = os.path.join(self.dpath, fname)
            if os.path.isfile(full_path):
                results = self.extract_infos(full_path)
                self.all_result.append(results)

        return self.all_result


    def extract_infos(self, fpath):
        file_type = ""
        res = {}

        res['name'] = os.path.basename(fpath)

        fp = open(fpath, 'rb')
        buf = fp.read(100)

        check_opcode = self.mergelist

        # 데이터 추출
        count = 0
        tempvalue = ''
        for i in range(len(check_opcode[0]) + 1):
            for j in range(len(self.ngrams_list[0])):
                try:
                    nowvalue = self.ngrams_list[0][j]
                    if nowvalue in check_opcode[0][i]:
                        count += 1
                    elif count != 0:
                        testvalue = j + len(nowvalue)
                        for kn in range(j + len(nowvalue), testvalue + len(nowvalue) * 3, len(nowvalue)):
                            tempvalue += self.ngrams_list[self.count][kn]
                        res[check_opcode[0][i]] = tempvalue
                        tempvalue = ''
                        count = 0
                except Exception as e:
                    if count != 0:
                        res[check_opcode[0][i - 1]] = 1

        self.reres = res
        return res


    def main(self):
        folder_path = "unhappy"

        self.ngrams = []
        result = []
        # 폴더 내의 모든 파일 경로 가져오기
        self.file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                self.file_paths.append(os.path.join(root, file))

        n = 8

        path = '/base'
        file_name = os.path.basename(path)
        dpath = os.path.dirname(path)

        fp = open('123' + '_pe2.csv', 'wt', encoding='utf-8')

        x = self.get_files_info()  # 실제 임시파일명은 입력 X

        header = ','.join(x[0].keys())
        headersave = header.replace('name,','')
        fp.write(header + '\n')
        count = 0

        for k in range(len(x)):
            data = ','.join([str(t) for t in x[k].values()])
            fp.writelines(data + '\n')
        csv_path = file_name + '.csv'

        return csv_path


if __name__ == '__main__':

    extractinfo()