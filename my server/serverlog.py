import logging,time,os
# log_path是存放日志的路径

class Log(object):

    def __init__(self):
        cur_path = os.path.dirname(os.path.realpath(__file__))

        self.log_path = cur_path + '\logs'
        # 如果不存在这个logs文件夹，就自动创建一个
        if not os.path.exists(self.log_path): os.mkdir(self.log_path)
        self.deletefile()
        # 文件的命名
        self.logname = os.path.join(self.log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - server - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        ##fh = handlers.TimedRotatingFileHandler(filename=self.logname, when='S', backupCount=3, encoding='utf-8')
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
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
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def deletefile(self):
        path = self.log_path
        for eachfile in os.listdir(path):
            filename = os.path.join(path, eachfile)
            if os.path.isfile(filename):
                lastmodifytime = os.stat(filename).st_mtime
                N = 3
                endfiletime = time.time() - 3600 * 24 * N  # 设置删除多久之前的文件

                if endfiletime > lastmodifytime:
                    if filename[-4:] == ".log":

                        os.remove(filename)
                        print ("删除文件 %s 成功" % filename)
            elif os.path.isdir(filename):  # 如果是目录则递归调用当前函数
                self.deletefile()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)
