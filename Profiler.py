# -*- coding: utf-8 -*-
# простейший профайлер
# with Profiler() as p:
#    // your code to be profiled here

import time
 
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print('Время выполнения: {:.3f} сек.'.format(time.time() - self._startTime))
