def gen_range(name):
    index = 0
    while index < len(name):
        # 請分成兩個步驟
        # 1. yield name[index] =>把一個元素彈出去
        # 2. 若有東西被 send 進來，會存到 yield 裡面

        jump = yield name[index]

        print("jump 被賦值"+str(jump))

        if jump is None:
            jump = 1
        index += jump


test_name = gen_range("Nick")
# print(next(test_name))
# print(next(test_name))
# print(next(test_name))
# print(next(test_name))

"""
Output:

N
jump 被賦值None
i
jump 被賦值None
c
jump 被賦值None
k

"""
print(next(test_name))
print(test_name.send(2))  # 現在 index 變成 2
print(next(test_name))  # 這裡應該輸出 'k'

"""
Output:

N
jump 被賦值2
c
jump 被賦值None
k
"""
