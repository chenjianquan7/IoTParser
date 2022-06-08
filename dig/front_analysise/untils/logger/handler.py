
import logging
from logging.handlers import RotatingFileHandler 
import colorlog  
import time
import datetime
import os

cur_path = os.path.dirname(os.path.realpath(__file__))  
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  
logName = os.path.join(log_path, '%s.log' % time.strftime('%Y-%m-%d'))  
log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

class Log():
    def __init__(self, logName=logName):
        self.logName = logName
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s',
            log_colors=log_colors_config)  
        self._writeformatter = logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s")
        
    def get_file_sorted(self, file_path):
        """最后修改时间顺序升序排列 os.path.getmtime()->获取文件最后修改时间"""
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
            return dir_list
    def TimeStampToTime(self, timestamp):
        """格式化时间"""
        timeStruct = time.localtime(timestamp)
        return str(time.strftime('%Y-%m-%d', timeStruct))
    def handle_logs(self):
        """处理日志过期天数和文件数量"""
        
        dir_list = ['logs']  
        for dir in dir_list:
            dirPath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), dir)  
            file_list = self.get_file_sorted(dirPath)  
            if file_list:  
                for i in file_list:
                    file_path = os.path.join(dirPath, i)  
                    t_list = self.TimeStampToTime(os.path.getctime(file_path)).split('-')
                    now_list = self.TimeStampToTime(time.time()).split('-')
                    t = datetime.datetime(int(t_list[0]), int(t_list[1]),
                                          int(t_list[2]))  
                    now = datetime.datetime(int(now_list[0]), int(now_list[1]), int(now_list[2]))
                    
                    if (now - t).days > 5:  
                        self.delete_logs(file_path)
                
                if len(file_list) > 4:
                    file_list = file_list[0:-4]
                    for i in file_list:
                        file_path = os.path.join(dirPath, i)
                        print(file_path)
                        self.delete_logs(file_path)
    def delete_logs(self, file_path):
        try:
            os.remove(file_path)
        except PermissionError as e:
            Log().warning('删除日志文件失败：{}'.format(e))
    def __console(self, level, message):
        
        
        fh = RotatingFileHandler(filename=self.logName, mode='a', maxBytes=1024 * 1024 * 100, backupCount=5,
                                 encoding='utf-8')  
        fh.setLevel(logging.INFO)
        fh.setFormatter(self._writeformatter)
        self.logger.addHandler(fh)
        
        ch = colorlog.StreamHandler()
        
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()  
    def debug(self, message):
        self.__console('debug', message)
    def info(self, message):
        self.__console('info', message)
    def warning(self, message):
        self.__console('warning', message)
    def error(self, message):
        self.__console('error', message)
log = Log()
if __name__ == "__main__":
    log = Log()
    log.debug("---测试开始----")
    log.info("操作步骤")
    log.warning("----测试结束----")
    log.error("----测试错误----")
