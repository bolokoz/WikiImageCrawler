import multiprocessing as mp
import time

def foo_pool(x):
    time.sleep(2)
    return x*x

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def apply_async_with_callback():
    pool = mp.Pool()
    for i in range(20):
        pool.apply_async(foo_pool, args = (i, ), callback = log_result)
    pool.close()
    pool.join()
    print(result_list)

if __name__ == '__main__':
    apply_async_with_callback(),

    def parallel_attribute(f):
    def easy_parallize(f, sequence):
        # I didn't see gains with .dummy; you might
        from multiprocessing import Pool
        pool = Pool(processes=8)
        #from multiprocessing.dummy import Pool
        #pool = Pool(16)

        # f is given sequence. Guaranteed to be in order
        result = pool.map(f, sequence)
        cleaned = [x for x in result if not x is None]
        cleaned = asarray(cleaned)
        # not optimal but safe
        pool.close()
        pool.join()
        return cleaned
    from functools import partial
    # This assumes f has one argument, fairly easy with Python's global scope
    return partial(easy_parallize, f)