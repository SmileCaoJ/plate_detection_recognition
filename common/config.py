import configparser
import logging
import logging.config
import os
import time

work_dir = os.path.abspath('')
logging_conf_file_dir = os.path.join(work_dir, "conf")
logging_conf_file_path = os.path.join(logging_conf_file_dir, "logging.conf")
logging.config.fileConfig(logging_conf_file_path)
logger = logging.getLogger(__name__)


class ServerConfig:
    def __init__(self):
        logger.info("work_dir: %s", work_dir)
        configpath = os.path.join(work_dir, "conf")
        logger.info("config dir: %s", configpath)
        configpath = os.path.join(configpath, "server.ini")
        logger.info("config file path: %s", configpath)
        self.cf = configparser.RawConfigParser()
        self.cf.read(configpath, encoding='utf-8')

    def get_common(self, param):
        value = self.cf.get("common", param)
        return value

    def get_video_processor(self, param):
        value = self.cf.get("video_processor", param)
        return value

    def get_detect_server(self, param):
        value = self.cf.get("detect_server", param)
        return value


server_config = ServerConfig()


def _get_web_dir():
    http_dir = os.path.join(work_dir, "http_svc")
    logger.info("http_dir: %s", http_dir)
    web_dir = os.path.join(http_dir, "web")
    logger.info("web_dir: %s", web_dir)
    return web_dir


web_dir = _get_web_dir()
