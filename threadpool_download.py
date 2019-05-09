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
