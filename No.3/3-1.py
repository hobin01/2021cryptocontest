# -*- coding: utf-8 -*-

import SimpleStack as st
import sys

# 남은 횟수 없을 시 종료
def error_check(cnt):
    if cnt <= 0:
        sys.exit()
    else:
        return

stack, cnt = st.init()

stack, cnt = st.push(stack, cnt)
error_check(cnt)

stack, cnt = st.push(stack, cnt)
error_check(cnt)

stack, cnt = st.add(stack, cnt)
error_check(cnt)

stack, cnt = st.push(stack, cnt)
error_check(cnt)

stack, cnt = st.equal(stack, cnt)
error_check(cnt)

input("엔터를 누르면 종료합니다.")