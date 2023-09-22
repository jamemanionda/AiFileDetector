import numpy as np


def hash_to_vector(hash_string, max_length):
    # 아스키 코드값을 사용해 문자를 숫자로 변환
    vector = [ord(c) for c in hash_string]

    # 최대 길이를 기준으로 패딩 적용
    while len(vector) < max_length:
        vector.append(0)

    return np.array(vector)[:max_length]


hash_values = ["a4b5c61212467891"]
max_length = max([len(h) for h in hash_values])

vectors = [hash_to_vector(h, max_length) for h in hash_values]
print(vectors)