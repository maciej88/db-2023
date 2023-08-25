from asyncio import create_task, sleep, gather, run
from random import random


# async with errors/exceptions


async def foo(x: int) -> int:
    await sleep(random())
    if x == 0:
        raise RuntimeError('meh')
    return x


async def main():
    tasks = []
    tasks.append(create_task(foo(1)))
    tasks.append(create_task(foo(2)))
    tasks.append(create_task(foo(0)))


    for t in tasks:
        try:
            g = await t
            print(g)
        except RuntimeError as e:
            print(e)

if __name__ == '__main__':
    run(main())
