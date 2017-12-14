#!/usr/bin/env python


class TaskManager():
    def __init__(self,maxTasks,maxThreads):
        #最大任务书，也就是Queue的容量
        self._maxTasks = maxTasks;
        #线程池中线程数量    
        self._maxThreads = maxThreads;
        #业务代码
        #任务池
        self._taskQueue = Queue.Queue(maxTasks);
        #线程池，使用列表实现
        self._threads = [];

        #在__init__中调用方法
        self.initThreads();
        self.initTaskQueue();

    #初始化任务池
    def initTaskQueue(self):
        while True:
        #业务代码
            if not self._taskQueue.full():
                getTasks(self._maxTasks - self._taskQueue.qsize());
                for task in taskMap["tasks"]:
                self._taskQueue.put(task);
                time.sleep(1);

    #初始化线程池
    def initThreads(self):
        for i in range(self._maxThreads):
        #调用每个线程执行的具体任务
        self._threads.append(Work(self,self._reportUrl));

    def getTask(self):
        return self._taskQueue.get();

#具体执行的任务
class Work(threading.Thread):
    def __init__(self,taskmgr):
        threading.Thread.__init__(self);
        self._logger = logging.getLogger("");
        self.start();

    def run(self):
        while True:
            try:
                #取出任务并执行相关操作
                self._taskmgr.getTask();
                ……
                ……

                time.sleep(1);
            except Exception,e:
                self._logger.exception(e); 