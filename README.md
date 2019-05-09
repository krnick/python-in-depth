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

## 那麼什麼時候可以用到協程呢


* 大量網路IO
* 大量硬碟IO

可以透過暫停的技巧，讓我們開始做一個 IO時，就讓程式暫停一下，我們可以就去做其他事情。

1. 協程是在一個行程裡面做程式流的切換
2. 不需要 Lock 的機制
3. 實現容易

## 用法

```yield from``` 加上可迭代物件或是迭代器，生成器，yield from 後的結果會產生一個產生器。

例如字串：

```python
string_obj = "Nick"

list_obj = ["N", "i", "c", "k"]

dict_obj = {"name": "Nick", "age": 24, "hobby": "computer"}

generator_obj = (i for i in range(0, 5))


def yield_from(args):
    yield from args


result = yield_from(generator_obj)

print(next(result))
print(next(result))
print(next(result))
```

透過 ```yield from``` 代替單獨的```yield```，可以讓程式變得更加優雅，且 ```yield from``` 在例外捕捉的部份做的相當多，因此若我們只有使用 ```yield``` 需要自己去做這些額外的例外捕捉。

## ```yield from``` 實際用法

通常會依靠三個概念

1. 子生成器 (放在代理生成器後面的函數)
2. 代理生成器 (做雙向溝通)
3. 調用者 (做 ```send``` 資料和接收 ```yield``` 回來的參數)

在程式碼加入了可辨識的英文，大家可以跟著英文找尋程式執行的路線。

```python
def download_from_url(url):
    url = str(url)
    print("Downloading:"+url)


def average_gen():
    """
    子生成器
    """
    url = "預設值"

    print("A")

    while True:
        print("B")
        # 接收 send 過來的值
        new_url = yield url  
        print("C")
        # 輸出 send 過來的值
        download_from_url(new_url)  

        if new_url is None:
            break

    # 每一次return，代表這個協程結束
    return "ok"


def proxy_gen():
    """
    代理生成器

    只有子生成器要結束 return了，yield from
    左邊的變數 result 才會被賦值，後面的程式才會被執行
    """
    print("D")
    while True:
        print("E")

        result = yield from average_gen()
        print("F")
        print(result)


def main():
    """
    調用者
    """
    web_download = proxy_gen()
    next(web_download)                  # 啟動
    web_download.send("www.gmail.com")  # 下載第一個網頁
    web_download.send(None)             # 結束協程
    """
    這裡若是在web_download.send("text")，由於上一個
    協程已經結束，這裡會重新啟動一個新的
    """


if __name__ == '__main__':
    main()
```