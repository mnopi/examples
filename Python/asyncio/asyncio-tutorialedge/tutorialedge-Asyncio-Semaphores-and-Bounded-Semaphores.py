#
import asyncio

# prueba: 1 - Semaphores
"""
What Are Semaphores?
Semaphores were originally a key part of railway system architecture and it 
was the famous Dijkstra that translated this real-world concept into our computing world.

These semaphores have an internal counter that is incremented and decremented 
whenever either an acquire or a release call is made.

Say we protected a block of code with a semaphore, and set the semaphore’s initial 
value to 2. If one worker acquired the semaphore, the value of our semaphore would be decremented to 1, 
if a second worker comes along the semaphore’s value would be decremented to 0.

At this point if another worker comes along and tries again it would be denied. 
The value of these semaphores is that they allow us to protect resources from being overused.

Implementation
Now that we have a basic understanding of what semaphores are let us now look at 
how we can work with them in our Asyncio based Python programs.

In this example we will create a simple instance of a semaphore and then create 
3 worker functions that will try to acquire said semaphore. The initial value of this semaphore will be 2 and as 
such we will see 2 of our worker functions successfully acquire the semaphore 
before then releasing it and allowing our third worker to then acquire it.
"""
import time


async def myWorker(semaphore):
    await semaphore.acquire()
    print("Successfully acquired the semaphore")
    await asyncio.sleep(3)
    print("Releasing Semaphore")
    semaphore.release()
    semaphore.release()


async def main(loop):
    mySemaphore = asyncio.Semaphore(value=2)
    await asyncio.wait([myWorker(mySemaphore), myWorker(mySemaphore), myWorker(mySemaphore)])
    print("Main Coroutine")


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
print("All Workers Completed")
# loop.close()

"""
Output
When we run this we should see that our first 2 workers are able to acquire the 
semaphore before then releasing it and allowing our third worker to then go on and acquire it for itself.
"""

# # prueba: 2 - Bounded Semaphores
# """
# Bounded Semaphores
# There lies a very subtle difference between a normal semaphore and a bounded-semaphore.
# A bounded semaphore only differs in terms of not allowing more releases to be made than acquires.
# If it does exceed the value then a ValueError is raised.
# """
#
#
# async def myWorker(semaphore):
#     await semaphore.acquire()
#     print("Successfully acquired the semaphore")
#     await asyncio.sleep(3)
#     print("Releasing Semaphore")
#     semaphore.release()
#     semaphore.release()
#
#
# async def main(loop):
#     mySemaphore = asyncio.BoundedSemaphore(value=2)
#     await asyncio.wait([myWorker(mySemaphore), myWorker(mySemaphore), myWorker(mySemaphore)])
#     print("Main Coroutine")
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))
# print("All Workers Completed")
# loop.close()


if __name__ == '__main__':
    # prueba: 1 -

    # prueba: 2 -

    # prueba: 3 -

    # prueba: 4 -

    exit(0)
