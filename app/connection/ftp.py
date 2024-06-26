import ftplib
from typing import BinaryIO

from log import logger

FTP_HOSTNAME = "dataprocess.online"
FTP_PORT = 18921
FTP_USERNAME = "avt"
FTP_PASSWORD = "Pl0d9RQYUJCxZPGw6NJUcb8eJ6ZXdNMw"
FTP_WORK_DIR = "/data"


class _FtpConnector:
    def __init__(self) -> None:
        self.ftp_server = ftplib.FTP()
        self.ftp_server.encoding = "utf-8"
        self.connect_status = ""
        self.login_status = ""
        self.connect(FTP_HOSTNAME, FTP_PORT, FTP_USERNAME, FTP_PASSWORD)

    def connect(self, hostname: str, port: int, username: str, password: str):
        self.connect_status = self.ftp_server.connect(hostname, port)
        logger.info(f"FTP connect  to {hostname}: {self.connect_status}")
        self.login_status = self.ftp_server.login(username, password)
        logger.info(f"FTP login by {username}: {self.login_status}")
        self.ftp_server.cwd(FTP_WORK_DIR)
        logger.info(f"cwd to {FTP_WORK_DIR}")

    def upload_file(self, file_path: str, file: BinaryIO) -> bool:
        try:
            self.ftp_server.storbinary(f"STOR {file_path}", file)
            logger.info(f"Write {file_path} successfully!")
            return True
        except Exception as e:
            logger.error(f"FTP write to {file_path} failed. Error: {e}")
            return False

    def download_file(self, file_path: str, file: BinaryIO) -> bool:
        try:
            self.ftp_server.retrbinary(f"RETR {file_path}", file.write)
            logger.info(f"Download {file_path} successfully!")
            return True
        except Exception as e:
            logger.error(f"FTP write to {file_path} failed. Error: {e}")
            return False

    def mkdir(self, dir_path: str) -> bool:
        try:
            if self.ftp_server.mkd(dir_path):
                return True
            return False
        except Exception as e:
            logger.info(f"Creating {dir_path} failed! Please restart program...")
            return False

    def cwd(self, path: str) -> bool:
        current_dir = self.ftp_server.pwd()
        try:
            if self.ftp_server.cwd(path):
                return True
            self.ftp_server.cwd(current_dir)
            return False
        except Exception as e:
            logger.error(e)
            self.ftp_server.cwd(current_dir)
            return False

    def is_dir_existed(self, path: str) -> bool:
        current_dir = self.ftp_server.pwd()
        try:
            if self.ftp_server.cwd(path):
                self.ftp_server.cwd(current_dir)
                return True
            self.ftp_server.cwd(current_dir)
            return False
        except Exception as e:
            logger.error(e)
            self.ftp_server.cwd(current_dir)
            return False

    def close(self):
        self.ftp_server.close()


ftpTransfer = _FtpConnector()
