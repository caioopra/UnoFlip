


def recebe(x):
    x()

for i in range(10):
    recebe(lambda :print(i))