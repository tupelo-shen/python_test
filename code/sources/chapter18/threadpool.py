# -*- coding: UTF-8 -*-
"""
易于使用的面向对象的线程池框架

线程池是维护管理着一堆工作线程，这些工作线程往往并行地执行一些比较耗时的操作。
它通过一个工作请求队列管理着要分派给线程的工作，工作线程在后台执行请求操作，并
把结果放到另一个队列中。
一旦来自结果队列里的结果可用，或所有的线程已经完成它们的工作，线程池对象就会收集
这些结果。也可以定义回调函数处理每一个结果。
基本概念和一些代码摘自“Python in a Nutshell，2nd edition”一书中的第14.5节-
“Threaded Program Architecture”，该书由作者Alex Martelli编写, O'Reilly 在
2006出版, 编号是ISBN 0-596-10046-9。在ThreadPool类中添加了主要程序逻辑。另外，
还添加了WorkRequest类和callback回调函数，且对代码各处不合适的地方进行了修改。

基本使用方法::
    >>> pool = ThreadPool(poolsize)
    >>> requests = makeRequests(some_callable, list_of_args, callback)
    >>> [pool.putRequest(req) for req in requests]
    >>> pool.wait()
在本模块代码的最后，有一个简短的，注释的使用例程
项目地址: http://chrisarndt.de/projects/threadpool/
"""
__docformat__ = "restructuredtext en"

__all__ = [
    'makeRequests',
    'NoResultsPending',
    'NoWorkersAvailable',
    'ThreadPool',
    'WorkRequest',
    'WorkerThread'
]

__author__ = "Christopher Arndt"
__version__ = '1.3.2'
__license__ = "MIT license"


# 导入标准库模块
import sys
import threading
import traceback

try:
    import Queue            # Python 2
except ImportError:
    import queue as Queue   # Python 3


# exceptions
class NoResultsPending(Exception):
    """所有的工作请求都已被处理."""
    pass

class NoWorkersAvailable(Exception):
    """No worker threads available to process remaining requests."""
    pass


# internal module helper functions
def _handle_thread_exception(request, exc_info):
    """Default exception handler callback function.

    This just prints the exception info via ``traceback.print_exception``.

    """
    traceback.print_exception(*exc_info)


# utility functions
def makeRequests(callable_, args_list, callback=None,
        exc_callback=_handle_thread_exception):
    """Create several work requests for same callable with different arguments.

    Convenience function for creating several work requests for the same
    callable where each invocation of the callable receives different values
    for its arguments.

    ``args_list`` contains the parameters for each invocation of callable.
    Each item in ``args_list`` should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    See docstring for ``WorkRequest`` for info on ``callback`` and
    ``exc_callback``.

    """
    requests = []
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(
                WorkRequest(callable_, item[0], item[1], callback=callback,
                    exc_callback=exc_callback)
            )
        else:
            requests.append(
                WorkRequest(callable_, [item], None, callback=callback,
                    exc_callback=exc_callback)
            )
    return requests


# classes
class WorkerThread(threading.Thread):
    """工作者线程运行于后台，从一个队列中取出工作请求，并将结果再存入一个队列，
    直到该线程被放弃
    """

    def __init__(self, requests_queue, results_queue, poll_timeout=5, **kwds):
        """
        设置线程为守护模式，并且立刻启动它。
        requests_queue和results_queue是Queue.Queue的实例，Queue.Queue是由ThreadPool类
        创建一个新的工作者线程时传递而来。
        """
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self._requests_queue = requests_queue
        self._results_queue = results_queue
        self._poll_timeout = poll_timeout
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """重复处理工作队列直到被告知退出"""
        while True:
            if self._dismissed.isSet():
                # 被抛弃,跳出循环
                break
            # 得到下一个工作请求。如果在固定时间（self._poll_timout秒）内不能从队列中
            # 得到一个新的请求。如果没有，调到循环开始处，给线程一个机会退出
            try:
                request = self._requests_queue.get(True, self._poll_timeout)
            except Queue.Empty:
                continue
            else:
                if self._dismissed.isSet():
                    # 被摒弃, 把请求放回队列中，然后退出循环
                    self._requests_queue.put(request)
                    break
                try:
                    result = request.callable(*request.args, **request.kwds)
                    self._results_queue.put((request, result))
                except:
                    request.exception = True
                    self._results_queue.put((request, sys.exc_info()))

    def dismiss(self):
        """
        当现在的工作完成后，设置标志，告知线程退出
        """
        self._dismissed.set()


class WorkRequest:
    """
    @param callable_:       用户自定义的，执行具体业务的函数
    @param args：            列表参数
    @param kwds：            字典参数
    @param requestID：       id，用于标识对象
    @param callback:        用户自定义，处理resultQueue队列元素的函数
    @param exc_callback:    用户自定义，处理异常的函数
    """
    def __init__(self, callable_, args=None, kwds=None, requestID=None,
            callback=None, exc_callback=_handle_thread_exception):
        # 如果没有指定requestID，调用id内建函数取其自身ID；否则，requestID必须为hash数
        if requestID is None:
            self.requestID = id(self)
        else:
            try:
                self.requestID = hash(requestID)
            except TypeError:
                raise TypeError("requestID must be hashable.")
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}
        print self.__str__()

    def __str__(self):
        return "<WorkRequest id=%s args=%r kwargs=%r exception=%s>" % \
            (self.requestID, self.args, self.kwds, self.exception)

class ThreadPool:
    """
    一个线程池，分配工作请求和收集结果。
    """

    def __init__(self, num_workers, q_size=0, resq_size=0, poll_timeout=5):
        """
        设置线程池并启动num_workers个工作线程。
        
        "num_workers"是初始启动时的工作者线程数
        q_size, 如果大于0，工作请求队列的大小就会被限制且队列满的时候且试图加入更多
        工作请求到队列中时，线程池发生阻塞。参见putRequest方法，除非你也为putRequest
        传递timeout值。
        resq_size, 如果大于0，结果队列的大小就会被限制且队列满的时候且试图加入更多
        新的结果到队列中时，线程池发生阻塞。

        .. 警告:
            如果设置q_size和resq_size不等于0,且结果队列没有及时处理，导致工作请求队列
            存放更多的工作，这时候就会有发生死锁的地方。
        """
        self._requests_queue = Queue.Queue(q_size)
        self._results_queue = Queue.Queue(resq_size)
        self.workers = []
        self.dismissedWorkers = []
        self.workRequests = {}
        self.createWorkers(num_workers, poll_timeout)

    def createWorkers(self, num_workers, poll_timeout=5):
        """
        添加num_workers个工作线程到线程池中。    
        poll_timout设置了线程多久检查一次他们是否被摒弃或等待请求的时间       
        """
        for i in range(num_workers):
            self.workers.append(WorkerThread(self._requests_queue,
                self._results_queue, poll_timeout=poll_timeout))

    def dismissWorkers(self, num_workers, do_join=False):
        """通知num_workers个工作线程做完它们当前任务后，退出"""
        dismiss_list = []
        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismiss_list.append(worker)

        if do_join:
            for worker in dismiss_list:
                worker.join()
        else:
            self.dismissedWorkers.extend(dismiss_list)

    def joinAllDismissedWorkers(self):
        """join所用被摒弃的线程"""
        for worker in self.dismissedWorkers:
            worker.join()
        self.dismissedWorkers = []

    def putRequest(self, request, block=True, timeout=None):
        """把工作请求放入工作队列，并保存它们的ID"""
        assert isinstance(request, WorkRequest)
        # 不要重新使用旧的工作请求
        assert not getattr(request, 'exception', None)
        self._requests_queue.put(request, block, timeout)
        self.workRequests[request.requestID] = request

    def poll(self, block=False):
        """处理结果队列中任何新的内容"""
        while True:
            # 是否还有结果未处理?
            if not self.workRequests:
                raise NoResultsPending
            # 是否还有工作者在处理剩余的工作请求?
            elif block and not self.workers:
                raise NoWorkersAvailable
            try:
                # 取下一个结果
                request, result = self._results_queue.get(block=block)
                # 是否有异常发生?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                # 如果有结果，传递给callback
                if request.callback and not \
                       (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except Queue.Empty:
                break

    def wait(self):
        """等待结果，阻塞，直到所有的都到达"""
        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break
#################################FOR TEST##############################

if __name__ == '__main__':
    import random
    import time

    # 线程必须做的工作（在我们的例子中相当微不足道）
    def do_something(data):
        time.sleep(random.randint(1,5))
        result = round(random.random() * data, 5)
        # 仅仅抛出异常，不做任何处理
        if result > 5:
            raise RuntimeError("Something extraordinary happened!")
        return result

    # 打印结果
    def print_result(request, result):
        print("**** Result from request #%s: %r" % (request.requestID, result))

    # 线程内有异常时，处理异常，这里做的比默认异常处理还要简单
    def handle_exception(request, exc_info):
        if not isinstance(exc_info, tuple):
            # 肯定有错误发生
            print(request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % \
          (request.requestID, exc_info))

    
    # 产生一个具有20个元素的列表，元素大小范围为（1,10），作为每项工作的参数
    data = [random.randint(1,10) for i in range(20)]
    # 为data中的每一项构建一个工作请求对象
    requests = makeRequests(do_something, data, print_result, handle_exception)
    # 如果想要使用默认异常处理，则注释掉这条语句，使用下面这条语句
    #requests = makeRequests(do_something, data, print_result)

    # or the other form of args_lists accepted by makeRequests: ((,), {})
    data = [((random.randint(1,10),), {}) for i in range(20)]
    requests.extend(
        makeRequests(do_something, data, print_result, handle_exception)
    )
    #requests += makeRequests(do_something, data, print_result, handle_exception)

    # 创建拥有 3个工作线程的线程池
    print("Creating thread pool with 3 worker threads.")
    main = ThreadPool(3)

    # 把工作请求加入到队列中
    for req in requests:
        main.putRequest(req)
        print("Work request #%s added." % req.requestID)
    # 或使用更短语句:
    # [main.putRequest(req) for req in requests]

    # ...and wait for the results to arrive in the result queue
    # by using ThreadPool.wait(). This would block until results for
    # all work requests have arrived:
    # main.wait()

    # instead we can poll for results while doing something else:
    i = 0
    while True:
        try:
            time.sleep(0.5)
            main.poll()
            print("主线程工作中...")
            print("(激活的工作线程个数是: %i)" % (threading.activeCount()-1, ))
            if i == 10:
                print("**** 添加了三个工作线程...")
                main.createWorkers(3)
            if i == 20:
                print("**** 摒弃了2个工作线程...")
                main.dismissWorkers(2)
            i += 1
        except KeyboardInterrupt:
            print("**** 中断!")
            break
        except NoResultsPending:
            print("**** 没有待处理的结果。")
            break
    if main.dismissedWorkers:
        print("等待所有被摒弃的线程执行完毕...")
        main.joinAllDismissedWorkers()