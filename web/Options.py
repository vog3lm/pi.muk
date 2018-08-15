from Process import ProcessArguments

class Options(ProcessArguments):
    def __init__(self):
        super(Options,self).__init__()
        self.args.update({'gateway=':'g:','socket=':'s:'})
        self.coreOpt = {}
        self.gateOpt = {}
        self.sockOpt = {}
        self.delivery.update({'process-options':self.coreOpt,'gateway-options':self.gateOpt,'socket-options':self.sockOpt})

    def extract(self,string,port):
        if not ':' in string:
            string = '%s:%s'%(string,port)
        split = string.split(':')
        return split[0],split[1]

    def create(self):
        super(Options,self).create()
        for o, a in self.opts:
            if '-g' == o:self.gateOpt['host'],self.gateOpt['port'] = self.extract(a,5000)
            elif '--gateway' == o:self.gateOpt['host'],self.gateOpt['port'] = self.extract(a,5000)
            elif '-s' == o:self.sockOpt['host'],self.sockOpt['port'] = self.extract(a,9002)
            elif '--socket' == o:self.sockOpt['host'],self.sockOpt['port'] = self.extract(a,9002)
        return self
