import threading
import queue
import random
import time

# Constants as per the assignment
LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Thread-safe queue for the buffer
buffer = queue.Queue(maxsize=BUFFER_SIZE)

# Lock for writing to files
file_lock = threading.Lock()

# Condition variable for synchronization
condition = threading.Condition()

# Counters
produced_count = 0
consumed_count = 0

def producer():
    global produced_count
    with open('all.txt', 'w') as f_all:
        while produced_count < MAX_COUNT:
            num = random.randint(LOWER_NUM, UPPER_NUM)
            with condition:
                if not buffer.full():
                    buffer.put(num)
                    produced_count += 1
                    f_all.write(f"{num}\n")
                    condition.notify_all()
                else:
                    condition.wait()

def consumer(consume_even):
    global consumed_count
    file_name = 'even.txt' if consume_even else 'odd.txt'
    with open(file_name, 'w') as f:
        while consumed_count < MAX_COUNT:
            with condition:
                if not buffer.empty():
                    num = buffer.queue[-1]  # Peek at the last element
                    if (num % 2 == 0) == consume_even:
                        num = buffer.get()  # Actually remove the number
                        with file_lock:
                            f.write(f"{num}\n")
                        consumed_count += 1
                        condition.notify_all()
                    else:
                        condition.wait()
                else:
                    condition.wait()

# Measure start time
start_time = time.time()

# Starting threads
producer_thread = threading.Thread(target=producer)
consumer_thread_even = threading.Thread(target=consumer, args=(True,))
consumer_thread_odd = threading.Thread(target=consumer, args=(False,))

producer_thread.start()
consumer_thread_even.start()
consumer_thread_odd.start()

# Waiting for threads to complete
producer_thread.join()
consumer_thread_even.join()
consumer_thread_odd.join()

# Measure end time and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Program completed successfully in {elapsed_time:.2f} seconds.")

