
import hmac
def tuple2str(tp):
    return " ".join([str(item) for item in tp])


def str2tuple(s):
    lst = s.split(" ")
    return lst

def make_digest(key,chall):
    return hmac.new(key.encode(), chall.encode("utf-8")).hexdigest()

def pack(msg):
    return str.encode(msg,'utf-8')

def unpack(msg):
    return bytes.decode(msg,'utf-8')


def fmt_hostport(sock):
    hn, port = sock.getsockname()
    return str(hn + ":" + str(port))

packet_size = 1024
as_port = 65000
com_port = 65001
edu_port = 65002

tlds_map = { 'com':65001, 'edu': 65002}