import time


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
        new_url = yield url  # 接收 send 過來的值
        print("C")

        download_from_url(new_url)  # 輸出 send 過來的值

        if new_url is None:
            break

    # 每一次return，代表這個協程結束
    return "ok"


def proxy_gen():
    """
    代理生成器
    """
    print("D")
    while True:
        print("E")
        # 只有子生成器要結束 return了，yield from左邊的變數 result 才會被賦值，後面的程式才會被執行
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

    # 這裡若是在web_download.send("text")，由於上一個協程已經結束，這裡會重新啟動一個新的


if __name__ == '__main__':
    main()
