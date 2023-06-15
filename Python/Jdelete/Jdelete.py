import os
from queue import Queue
import shutil
import stat
import time
import threading

def timer(func):
    def inner(*args, **kwargs):
        begin = time.time()
        print('开始时间: ', '%d-%d-%d %02d:%02d:%02d' % tuple(time.localtime(begin))[:6], '.', str(begin).split('.')[1][:4], sep='')
        a = func(*args, **kwargs)
        end = time.time()
        print('结束时间: ', '%d-%d-%d %02d:%02d:%02d' % tuple(time.localtime(end))[:6], '.', str(end).split('.')[1][:4], sep='')
        print('消耗时间: ', round(end - begin, 4), 's')
        return a
    return inner

class Jdelete:
    @timer
    def __init__(self, mypath, mode=''):
        self.path = mypath
        self.queue = Queue(100000)
        self.num =0
        self.mode = mode
        print('遍历路径:', self.path)
        self.get_files(self.path)

    def get_files(self, mypath):
        try:
            # print(f'attrib -r "{mypath}"')
            os.system(f'attrib -r "{mypath}"')
            _name = os.path.abspath(mypath)
            for i in os.listdir(mypath):
                name = os.path.join(_name, i)
                if os.path.isfile(name):
                    self.queue.put(os.path.abspath(name))
                    self.num += 1
                elif os.path.isdir(name):
                    self.get_files(name)
        except Exception as e:
            print(e)

    def rm_file(self):
        while not self.queue.empty():
            i = self.queue.get()
            try:
                os.remove(i)
            except FileNotFoundError:
                print('error:', i)
            except PermissionError:
                os.chmod(i, stat.S_IWRITE)
                os.remove(i)
            except Exception as e:
                print(e)

    def calc_size(self):
        size = 0
        while not self.queue.empty():
            i = self.queue.get()
            try:
                size += os.path.getsize(i)
            except Exception as e:
                print(e)
                exit()
        return size

    @timer
    def delete(self):
        print('开始删除!')
        threads = []
        for i in range(100):
            t = threading.Thread(target=self.rm_file, name='th-' + str(i), kwargs={})
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def __enter__(self):
        if not os.path.exists(self.path):
            print('路径不存在')
            exit()
        print('文件数量:', self.num)
        print('文件大小:', self.calc_size() >> 20, 'MB')
        return self

    def __exit__(self, type, value, trace):
        a, b, c = type, value, trace
        if a != None:
            print(a, b, c, sep='\n')
        if self.mode == 'delete':
            try:
                if os.path.exists(self.path):
                    for i in os.listdir(self.path):
                        _name = os.path.join(self.path, i)
                        if os.path.isdir(_name):
                            shutil.rmtree(_name)
                        elif os.path.isfile(_name):
                            os.chmod(_name, stat.S_IWRITE)
                            os.remove(_name)
            except Exception as e:
                print(e)
        else:
            pass
            
_path = "F:\\Program_Files\\OriginLab"
with Jdelete(_path, mode='delete') as j:
    pass
