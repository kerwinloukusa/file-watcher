import os
import sys 
import time

class Watcher(object):
    running = True
    refresh_delay_secs = 1
    # Constructor
    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs
        file_list = open(watch_file, "r")
        l = []
        for file_name in file_list:
            l.append(file_name.strip('\n'))
        self.cache = {key:0 for key in l}
        self.file_name_list = l


    # Look for changes
    def look(self):
        
        for file in self.file_name_list:
            stamp = os.stat(file).st_mtime
            if stamp != self.cache[file]:
                self.cache[file] = stamp
                # File has changed, so do something...
                print('File changed')
                if self.call_func_on_change is not None:
                    self.call_func_on_change(*self.args, **self.kwargs)

    # Keep watching in a loop        
    def watch(self):
        while self.running: 
            try: 
                # Look for changes
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                print('\nDone') 
                break 
            except FileNotFoundError:
                # Action on file not found
                pass
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])

# Call this function each time a change happens
def custom_action(text):
    os.system(file_to_run) 


#read in file list to watch from users
watch_file = sys.argv[1]
file_to_run = sys.argv[2]

# watcher = Watcher(watch_file)  # simple
watcher = Watcher(watch_file, custom_action(file_to_run), text='yes, changed')  # also call custom action function
watcher.watch()  # start the watch going

