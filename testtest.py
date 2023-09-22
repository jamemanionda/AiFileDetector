import pandas as pd

# 주어진 문자열
s = "89504e470d0a1a0a0000000d4948445200000,00000097048597300000,49444154,944415478daec,000000049454e44ae426082"

# 문자열을 ','로 분리
sub_strings = s.split(',')

# 각 문자열에 1부터 증가하는 10진수를 매핑
mapping = {sub_str: i+1 for i, sub_str in enumerate(sub_strings)}

# 데이터프레임으로 변환
df = pd.DataFrame(list(mapping.items()), columns=["Key", "Value"])

# 데이터프레임을 CSV 파일로 저장
df.to_csv('output.csv', index=False)

print("CSV file saved as 'output.csv'")