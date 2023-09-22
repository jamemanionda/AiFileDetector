import csv
import hashlib

# CSV 내용을 읽어옵니다.
input_data = """
name,89504e470d0a1a0a0000000d4948445200000,00000097048597300000,49444154,944415478daec,000000049454e44ae426082
file1.png,52000003200000310000031b,7300000e300000ec00000ec4,94441547444154784415478d,478daec578daec5b8daec5b4,1
file2.png,52000003200000310000031b,7300000e300000ec00000ec4,94441547444154784415478d,478daec578daec5b8daec5b4,1
file3.png,52000003200000310000031b,7300000e300000ec00000ec4,94441547444154784415478d,478daec578daec5b8daec5b4,1
"""

def hash_string(s):
    """주어진 문자열을 해시값으로 반환합니다."""
    return hashlib.sha256(s.encode()).hexdigest()

rows = list(csv.reader(input_data.strip().split("\n")))
new_rows = []

# 모든 행과 열에 대해서 처리합니다.
for row in rows:
    new_row = []
    for idx, col in enumerate(row):
        # 첫번째 컬럼 (name) 이면 해시 처리하지 않습니다.
        if idx == 0:
            new_row.append(col)
        else:
            new_row.append(hash_string(col))
    new_rows.append(new_row)

# 완성된 결과를 새로운 CSV 파일에 저장합니다.
output_filename = "output.csv"
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(new_rows)

print(f"Data has been written to {output_filename}")
