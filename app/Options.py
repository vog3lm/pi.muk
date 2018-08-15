from Process import ProcessArguments

class Options(ProcessArguments):
    def __init__(self):
        super(Options,self).__init__()
        self.args.update({'port=':'p:','host=':'h:'})
        self.appOpt = {}
        self.socOpt = {}
        self.delivery.update({'process-options':self.appOpt,'socket-options':self.socOpt})

    def create(self):
        super(Options,self).create()
        for o, a in self.opts:
            if '-p' == o:self.socOpt['port'] = a
            elif '--port' == o:self.socOpt['port'] = a
            elif '-h' == o:self.socOpt['host'] = a
            elif '--host' == o:self.socOpt['host'] = a
        return self
