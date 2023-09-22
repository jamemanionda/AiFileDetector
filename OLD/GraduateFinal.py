from collections import Counter

def extract_hex_patterns(hex_string, n):
    patterns = {}  # 패턴을 저장할 딕셔너리

    # 입력된 16진수 문자열을 n-gram으로 분할하고 패턴 딕셔너리에 추가
    for i in range(len(hex_string) - n + 1):
        pattern = hex_string[i:i + n]
        if pattern in patterns:
            patterns[pattern] += 1
        else:
            patterns[pattern] = 1

    # 패턴을 빈도수에 따라 내림차순으로 정렬
    sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)

    return sorted_patterns


def extract_hex_string_from_file(file_path):
    hex_string = ""

    # 파일 열기
    with open(file_path, 'rb') as file:
        # 파일 내용 읽기
        contents = file.read()

        # 16진수 문자열 추출
        hex_string = contents.hex()

    return hex_string


def filter_strings(lst):
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


# 파일 경로
file_path = "../happy/file1.png"

# 파일에서 16진수 문자열 추출
hex_string = extract_hex_string_from_file(file_path)
print("Extracted Hex String:", hex_string)

n = 8
result = extract_hex_patterns(hex_string, n)
newnew = []
print(f"{n}-gram patterns:")

# 2-gram을 추출하는 경우
n = 10
result.extend(extract_hex_patterns(hex_string, n))
print(f"{n}-gram patterns:")

new_list = [tup for tup in result if tup[1] >= 10]

new_list = filter_strings(new_list)

print(new_list)
# for pattern, frequency in newlist:
#     if frequency > 10 :
#         print(f"Pattern: {pattern}, Frequency: {frequency}")

def extract_string(data):
    sorted_data = sorted(data, key=lambda x: len(x[0]), reverse=True)
    target_string = sorted_data[0][0]
    data.remove(sorted_data[0])

    while len(data) > 0:
        for i in range(len(data)):
            if data[i][0].startswith(target_string):
                data[i] = (data[i][0][len(target_string):], data[i][1])
                break
        else:
            break

    return target_string

target_string_1 = extract_string(new_list)
target_string_2 = extract_string(new_list)

print(target_string_1)  # '49444154'
print(target_string_2)  # '12345678'


def create_data_tuples(file_data, target_value):
    tuples = []
    start_index = 0
    while True:
        # Find the index of the target value
        index = file_data.find(target_value, start_index)
        if index == -1:
            break
        # Get the data before the target value
        data = file_data[start_index:index]
        # Create a tuple with the target value and the data
        data_tuple = (target_value, data)
        # Add the tuple to the list
        tuples.append(data_tuple)
        # Update the start index for the next iteration
        start_index = index + len(target_value)
    return tuples

# Example usage
target_value = target_string_1
result = create_data_tuples(hex_string, target_value)
print(result)



