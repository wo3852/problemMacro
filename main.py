import back
import programers

while True:
    n = input("1: 백준알고리즘    2: 프로그래머스   3: 종료")
    if n == "1":
        back.start()
    elif n == "2":
        programers.start()
    elif n == "3":
        print("종료 합니다")
        break
    else: print("다시 입력해 주세요")