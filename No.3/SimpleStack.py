# -*- coding: utf-8 -*-

# 초기화
def init():
    print("덧셈 연산 결과와 주어진 결과를 비교합니다. ")
    stack = []
    cnt = 5
    return stack, cnt

# 남은 카운트 프린트
def print_cnt(cnt):
    if cnt <= 0:
        print("남은 기회가 없습니다.")
    else:
        print("남은 기회 : ", cnt)
    return

# 스택 내용 프린트
def print_stack(stack):
    if len(stack) == 0:
        print("stack is empty")
    
    else:
        print("========== stack ===========")
        print("top ----> ", stack[-1])
        for i in range(len(stack) - 2, -1, -1):
            print("============================")
            print("          ", stack[i])
        print('============================\n')
    return

def push(stack, cnt):
    print("push 연산입니다.")
    
    while True:
        try:
            print_cnt(cnt)
            if cnt <= 0:
                break
        
            num = int(input("정수를 입력하세요 : "))
        except : 
            print("정수가 아닙니다.")
            cnt -= 1
        else:
            stack.append(num)
            print_stack(stack)
            break
    
    return stack, cnt

def add(stack, cnt):
    print("덧셈 연산입니다.")

    while True:
        try:
            print_cnt(cnt)
            if cnt <= 0:
                break
            
            oper = input("ADD를 입력하세요.")
            
            possible_case = ["ADD", "Add", "add", "+"]
            if oper in possible_case:
                num1 = stack.pop()
                num2 = stack.pop()
                num = num1 + num2
                stack.append(num)
                print_stack(stack)
                break
            else:
                print("잘못 입력하였습니다.")
                cnt -= 1
        except:
            print("잘못 입력하였습니다.")
            cnt -= 1
        
    return stack, cnt

def equal(stack, cnt):
    print("비교 연산입니다.")

    while True:
        try:
            print_cnt(cnt)
            if cnt <= 0:
                break
            
            oper = input("EQUAL을 입력하세요.")
            
            possible_case = ["EQUAL", "Equal", "equal", "==", "="]
            if oper in possible_case:
                num1 = stack.pop()
                num2 = stack.pop()
                if num1 == num2:
                    stack.append("True")
                else:
                    stack.append("False")
                print_stack(stack)
                break
            else:
                print("잘못 입력하였습니다.")
                cnt -= 1
        except:
            print("잘못 입력하였습니다.")
            cnt -= 1
    
    return stack, cnt
            