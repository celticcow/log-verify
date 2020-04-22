#!/usr/bin/python3

class loge(object):
    """
    a lot entry
    has source / dest / port
    """

    #constructor
    def __init__(self, source="0.0.0.0", dest="0.0.0.0", port="0"):
        self.source = source
        self.dest = dest
        self.port = port
        self.count = 0

    #accessor
    def get_source(self):
        return(self.source)

    def get_dest(self):
        return(self.dest)
    
    def get_port(self):
        return(self.port)

    def get_count(self):
        return(self.count)
    

    #modifiers
    def set_source(self, source):
        self.source = source
    
    def set_dest(self, dest):
        self.dest = dest

    def set_port(self, port):
        self.port = port

    def increment(self):
        self.count = self.count + 1

    #compare
    def compare(self, source, dest, port):
        if((self.source == source) and (self.dest == dest) and (self.port == port)):
            return True
        else:
            return False
    
    def print_log_entry(self):
        print("Log Entry " + self.source + " -> " + self.dest + " : " + self.port + " occured " + str(self.count))
#end of class log_entry