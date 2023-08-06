def compare_strings_in_list(lst):

    while True:
        try:
            newlist = []
            list_changed = False
            for i in range(len(lst) - 1):
                second_string = lst[i + 1][:-1]  # 두 번째 문자열은 마지막 글자를 제외한 부분을 추출

                secondlen = len(second_string)
                first_string = lst[i][-secondlen:]   # 첫 문자열은 첫 글자를 제외한 부분을 추출

                # 두 문자열을 비교하고 결과 출력
                if first_string == second_string:
                    remain=lst[i+1][-1]
                    newword = lst[i]+remain
                    lst[i] = newword
                    del lst[i+1]

            if not list_changed:  # 만약 리스트에 변화가 없다면 루프 종료
                break
        except Exception as e:
            pass

    print(lst)

# 예시 리스트
input_list = ['abcde', 'bcdef', 'cdefg', 'zxcvb', 'xcvba','zxbnm']
compare_strings_in_list(input_list)