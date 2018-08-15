import logging

class FirebaseException(Exception):
    def __init__(self,errors):
        self.errors = errors

    def toString(self):
        return ' '.join(self.errors) # str(self.errors).replace('\'','').replace('[','').replace(']','')

class Firebase(object):
    def __init__(self):
        self.args = {'emitter':None,'user':None,'token':None,'cfg':'configuration.cfg','mail':None,'pass':None
                    ,'apiKey':None,'authDomain':None,'databaseURL':None,'projectId':None,'storageBucket':None,'messagingSenderId':None}
        self.admin = None
        self.auth = None
        self.events = {'create-firebase':self.create,'login-firebase':self.login,'logout-firebase':self.logout}

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,data={}):
        errors = []
        config = {}
        if None == self.args.get('apiKey'):
            errors.append('no api key set')
        else:
            config['apiKey'] = self.args.get('apiKey')
        if None == self.args.get('authDomain'):
            errors.append('no authentication domain set')
        else:
            config['authDomain'] = self.args.get('authDomain')
        if None == self.args.get('databaseURL'):
            errors.append('no database url set')
        else:
            config['databaseURL'] = self.args.get('databaseURL')
        if None == self.args.get('projectId'):
            errors.append('no project id set')
        else:
            config['projectId'] = self.args.get('projectId')
        if None == self.args.get('storageBucket'):
            errors.append('no storage bucket set')
        else:
            config['storageBucket'] = self.args.get('storageBucket')
        if None == self.args.get('messagingSenderId'):
            errors.append('no messaging sender id set')
        else:
            config['messagingSenderId'] = self.args.get('messagingSenderId')

        if 0 < len(errors):
            logging.error('firebase configuration has errors. cannot create.')
            logging.error('%s'%', '.join(errors))
            return self

        from pyrebase import initialize_app
        self.admin = initialize_app(config)
        self.auth = self.admin.auth()
        self.database = self.admin.database()

        # all_agents = db.child("agents").get(user['idToken']).val()
        # lana_data = db.child("agents").child("Lana").get(user['idToken']).val()
        # db.child("agents").child("Lana").update({"name": "Lana Anthony Kane"}, user['idToken'])
        # db.child("agents").remove(user['idToken'])
        # db.child("agents").child("Lana").remove(user['idToken'])

        self.storage = self.admin.storage()

        # as admin
        # storage.child("images/example.jpg").put("example2.jpg")
        # as user
        # storage.child("images/example.jpg").put("example2.jpg", user['idToken'])

        # storage.child("images/example.jpg").download("downloaded.jpg")
        # storage.child("images/example.jpg").get_url()

        logging.info('firebase created for %s'%self.args.get('authDomain'))
        return self

    def login(self,data={}):
        keys = data.keys()
        errors = []
        mail = ''
        password = ''
        if not None == self.args.get('mail'):
            mail = self.args.get('mail')
        elif 'mail'in keys:
            mail = self.data.get('mail')
        else:
            errors.append('no username found')
        if not None == self.args.get('pass'):
            password = self.args.get('pass')
        elif 'pass'in keys:
            password = self.data.get('pass')
        else:
            errors.append('no password found')

        if 0 < len(errors):
            logging.error('login error. %s'%', '.join(errors))

        user = self.auth.sign_in_with_email_and_password(mail,password)
        self.args['user'] = user
        self.args['token'] = auth.refresh(user['refreshToken']) # force token refresh, expires after 1 hour
        logging.info('%s logged in to %s.'%(mail,self.args.get('authDomain')))
        # self.auth.get_account_info(self.args.get('token'))
        return self

    def logout(self,data={}):
        logging.info('%s logged out from %s.'%(mail,self.args.get('authDomain')))
        return self