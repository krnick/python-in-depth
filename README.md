#Python
# 理解多執行緒、協程
# 生成器、可迭代、迭代器


Python 在處理多工任務主要場景為：

* IO密集
* CPU密集



## 可迭代 Iterable

簡而言之就是可以一個一個拿出來，並不會全部載入至記憶體中，在大量插入或是批次查詢非常有用。

如Python 的物件，字串 (string)、列表 (list)、字典 (dict)、元組 (tuple) 稱為可迭代的物件。

*注意！！非迭代器*，*所謂的可迭代，代表物件裡面有 ```__item__()```*

## 迭代器 Iterator

對比於可迭代的物件，其實就是在物件本身實現了 ```__next__()```，使得不需 ```for``` 的情況下，透過 ```next()``` 就可以一個一個拿
出來。

```python
from collections.abc import Iterator

string_obj = 'Nick'  # 建立可迭代的物件，如字串
test_Iterator = iter(string_obj)  # 藉由iter()，將可迭代物件轉換為迭代器
print(isinstance(test_Iterator, Iterator))  # 判斷是否為迭代器
print(next(test_Iterator))  # N
print(next(test_Iterator))  # i
print(next(test_Iterator))  # c
print(next(test_Iterator))  # k
```

## 生成器 Generator

目的是為了產生對應的下一個值，不要浪費空間，具體作法則是基於迭代器，實現 ```yield```。

```yield```，原理如同我們函數的 ```return```，經過每次 ```for```或是 ```next()```取出一個值後，把這裡值回傳出去並阻塞，等待下一次取值，如此一來就可以大幅度地減少記憶體的使用。

 * 產生 Generator

```python
generator = (x * x for x in range(5))
print(isinstance(L, Generator))
```

對比於迭代器、可迭代物件，生成器並不會把所有值都放入記憶體，而是依靠第一個元素才產生接下來的值。

```python
def generate_yield(name):
    now = 0
    while now < len(name):
        yield name[now]
        now += 1


gen = generate_yield("Nick")

# 可以使用 send()或是 next() 進行產生下一個對應的值
print(gen.send(None))
print(next(gen))
print(gen.send(None))
print(next(gen))
```

## 協程

協程最主要是從 ```yield```這個概念延伸，可以發現在 **Generator** 的地方能實現暫停下來這個功能，那我們是不是可以在暫停下來多做一點事情。

對比於多執行緒，多執行緒透過切換 **Thread** 來達到很多事情，但伴隨而來的 **Context Switch** 和 **Lock** 機制、初始化 Thread 資源耗掉相當多資源。

而 **協程** 則是透過"暫停"這個方法，將程式主控權交給其他人。 

```python
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

```