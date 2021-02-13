#소인수분해 함수
def primefactor(num):
    a = 2
    num = int(num)
    answer = []
    while num != 1:
        if num %a != 0:
            a = a+1
        else:
            num = num//a
            answer.append(a)
            a = 2
    return answer

"""
소인수분해 기능 함수입니다.
num 에 넣은 수의 소인수가 answer에 들어갑니다.
Made by 설망래 , 이끼 낀 금화
"""
