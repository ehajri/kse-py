import multiprocessing, time

def worker(num):
    "worker function"
    print("worker %d" % num)
    if num == 2:
        time.sleep(10)
        worker(num)
    return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()
