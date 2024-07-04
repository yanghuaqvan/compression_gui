import os
import sys
import py7zr
import hashlib
from PyQt5.QtCore import QThread, pyqtSignal

class CompressThread(QThread):

    processSignal = pyqtSignal(int) #0-100
    stateSignal = pyqtSignal(int) #0-idle 1-process

    def __init__(self, path, method, parent=None):
        super(CompressThread, self).__init__(parent)
        self.path = path
        self.method = method

    def run(self):
        self.stateSignal.emit(1)
        file_list = os.listdir(self.path)
        file_cnt = len(file_list)
        for i,file in enumerate(file_list,start=1):
            target_file = os.path.join(self.path, file)
            if(os.path.isfile(target_file)):
                hash_code = hash(target_file, self.method)
                zip_path = os.path.join(self.path, hash_code + '.7z')
                archive = py7zr.SevenZipFile(zip_path, mode='w', password=hash_code, header_encryption=True)
                archive.write(target_file, file)
                archive.close()
                if zip_path==target_file:
                    continue
            self.processSignal.emit(int(i/file_cnt*100))
        self.stateSignal.emit(0)

def hash(file, method):
    if not os.path.isdir(file):
        f = open(file, 'rb')
        sum = ""
        if method == "sha1":
            sum = hashlib.sha1(f.read()).hexdigest()
        elif method == "sha224":
            sum = hashlib.sha224(f.read()).hexdigest()
        elif method == "sha256":
            sum = hashlib.sha256(f.read()).hexdigest()
        elif method == "sha384":
            sum = hashlib.sha384(f.read()).hexdigest()
        elif method == "sha512":
            sum = hashlib.sha512(f.read()).hexdigest()
        elif method == "md5":
            sum = hashlib.md5(f.read()).hexdigest()
        f.close()
        return sum
    else:
        return "dir"