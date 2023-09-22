def lcs(X, Y):
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


def lcs_multiple_lists(lists):
    if len(lists) < 2:
        raise ValueError("At least two lists are required")

    current_lcs = lcs(lists[0], lists[1])

    for lst in lists[2:]:
        current_lcs = lcs(current_lcs, lst)
        if not current_lcs:
            return []

    return current_lcs

lists = []
# 사용 예시
list1 = ['A', 'B', 'C', 'D', 'M', 'A', 'A', 'U', 'X', 'Y', 'Z']
list2 = ['B', 'C', 'D', 'C', 'A', 'A', 'C', 'X', 'Y', 'Z']
list3 = ['B', 'C', 'D', 'C', 'A', 'Z', 'X', 'Y', 'Z']
list4 = ['B', 'C', 'D', 'C', 'A', 'W', 'X', 'Y', 'Z']

lists.append(list1)
lists.append(list2)
lists.append(list3)
lists.append(list4)

print(lcs_multiple_lists(lists))