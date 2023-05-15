from datetime import datetime
import pathlib
import os

class Logger:
    logger_path: str
    
    @classmethod
    def set_logger_path(cls, path: pathlib.Path) -> None:
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        try:
            with open(path, "w") as log_file:
                log_file.write(f"[{log_time}]Logger created at -> {path}\n")
        except FileNotFoundError:
            directory_path = path.parent
            os.makedirs(directory_path)
            
            with open(path, "w") as log_file:
                log_file.write(f"[{log_time}]Logger created at -> {path}\n")
        
        print(f"[{log_time}]Logger created at -> {path}")
        cls.logger_path = path
    
    @classmethod
    def info(cls, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        with open(cls.logger_path, "a") as log_file:
            log_file.write(f"[{log_time}][INFO] {message}\n")
        print(f"[{log_time}][INFO] {message}")

    @classmethod
    def warn(cls, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        with open(cls.logger_path, "a") as log_file:
            log_file.write(f"[{log_time}][WARN] {message}\n")    
        print(f"[{log_time}][INFO] {message}")

    @classmethod
    def error(cls, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        with open(cls.logger_path, "a") as log_file:
            log_file.write(f"[{log_time}][ERROR] {message}\n")   
        print(f"[{log_time}][INFO] {message}")
