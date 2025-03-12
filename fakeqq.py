import time
import string
import secrets
import random
import fake_useragent
import requests


class FakeQQ:
    def __init__(self, buffern=1024):
        # self.dictionary = dictionary
        self.buffern = buffern
        self.bufferarea = []
        self.numlist = list("0123456789")
        self.characters = string.ascii_letters + string.digits

    @staticmethod
    def group(n):
        return str(random.randint(10**(n-1), 10**n - 1))

    def randid(self):
        return "".join([self.group(2), self.group(2), self.group(2), self.group(2), self.group(2)])

    def randpwd(self):
        # with open(self.dictionary, "r") as dictfile:
        #     passwords = [passwd.strip() for passwd in dictfile.readlines() if passwd != "\n" and passwd]
        # return random.choice(passwords)
        return ''.join(secrets.choice(self.characters) for _ in range(random.randint(10, 16)))

    def buffer(self, data):
        if len(self.bufferarea) >= self.buffern:
            self.bufferarea = []
        if data not in self.bufferarea:
            self.bufferarea.append(data)

        return None

    def process(self):
        result = self.randid(), self.randpwd()
        self.buffer(result)
        return result

n = 1
fake_qq = FakeQQ(1024)

while True:
    userid, passwd = fake_qq.process()
    url = "http://lnioce.work/data"
    headers = {
        "Host": "lnioce.work",
        "Content-Length": "114",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": fake_useragent.UserAgent().random,
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://lnioce.work",
        "Referer": "http://lnioce.work/step_in/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive"
    }
    data = {
        "sv": '{"act":"sv","data":{"user":"%s","pass":"%s"}}' %(userid, passwd)
    }

    response = requests.post(url, headers=headers, data=data)
    print(f"第{n}条QQ注入记录，{response.status_code}\n{response.text}")
    print(f"UserID:{userid}, Passwd:{passwd}")
    if response.status_code != 200:
        print(response.status_code, response.text)
        break
    n += 1
    time.sleep(120)



