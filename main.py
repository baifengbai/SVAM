from creation_center.sister import ContentMaker
import time
from multiprocessing import Process,Pool

def test(count):
    maker = ContentMaker()
    maker.sister(1)
if __name__ == "__main__":
    test(1)
    # p = Pool(24)
    # for i in range(1):
    #     p.apply_async(test,args=(1,))
    # p.close()
    # p.join()