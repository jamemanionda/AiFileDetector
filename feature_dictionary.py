import csv
import pandas as pd
#한 라벨의 헤더 피처 딕셔너리화

# 주어진 문자열
with open('123_pe(mp4원본+위조).csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    # 헤더 행을 건너뜁니다. (이 경우 'Key', 'Value')

    for row in reader:
        row = row
        break

sub_strings = row[1:]

mapping = {}
count = 1

for sub_str in sub_strings:
    if sub_str not in mapping:
        mapping[sub_str] = count
        count += 1

# 데이터프레임으로 변환
df = pd.DataFrame(list(mapping.items()), columns=["Key", "Value"])

# 데이터프레임을 CSV 파일로 저장
df.to_csv('pngfeature.csv', index=False)

print("CSV file saved as 'pngfeature.csv'")
print(df)