class DNSEntry:
    hostname = str()
    ip = str()
    qtype = str()

    # construcor for tuple
    def __init__(self, item):
        self.hostname, self.ip,self.qtype = item

    def __init__(self, hn, ip, type):
        self.hostname = hn
        self.ip = ip
        self.qtype = type

    def __str__(self):
        return self.hostname + " " + self.ip + " " + " " + self.qtype

    def __repr__(self):
        return self.hostname + " " + self.ip + " "  + " " + self.qtype

    def __eq__(self, other):
        if (self.hostname, self.ip, self.qtype) == (other.hostname, other.ip, other.qtype):
            return True
        else:
            return False

    @staticmethod
    def from_str(entry : str):
        entry = entry.rstrip(" []\n\r").lstrip(" []\n\r")  # clear out junk in the string
        #hn, ip, port, type = entry.split(' ')  # split into its fields
        entry = entry.split(' ')
        entry = [e for e in entry if e != '']
        print(entry)
        #port = int(port)  # port must be an int
        return DNSEntry(entry[0], entry[1], entry[3])
