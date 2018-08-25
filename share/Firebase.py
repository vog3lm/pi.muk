import logging

class FirebaseException(Exception):
    def __init__(self,errors):
        self.errors = errors

    def toString(self):
        return ' '.join(self.errors) # str(self.errors).replace('\'','').replace('[','').replace(']','')

class FirebaseClient(object):
    def __init__(self):
        self.args = {'emitter':None,'user':None,'uid':None,'token':None,'cfg':'configuration.cfg','mail':None,'pass':None,'path':'configuration.cfg'
                    ,'apiKey':None,'authDomain':None,'databaseURL':None,'projectId':None,'storageBucket':None,'messagingSenderId':None}
        self.admin = None
        self.auth = None
        self.events = {'create-firebase-client':self.create,'configurate-firebase-client':self.configurate
                      ,'login-firebase-client':self.login,'logout-firebase-client':self.logout}

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def configurate(self,data={}):
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.optionxform=str
        parser.read(self.args.get('path'))
        firebase = {}
        tmp = parser['firebase']
        for key in tmp:
            firebase[key] = str(tmp[key])
        tmp = parser['user']
        for key in tmp:
            firebase[key] = str(tmp[key])
        self.decorate(firebase)
        return self

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

        logging.debug('firebase created for %s'%self.args.get('authDomain'))
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

        from requests.exceptions import HTTPError
        try:
            logging.debug('%s logs in to %s.'%(mail,self.args.get('authDomain')))
            user = self.auth.sign_in_with_email_and_password(mail,password)
            self.args['user'] = user
            self.auth.refresh(user['refreshToken']).get('idToken') # force token refresh, expires after 1 hour
            self.args['token'] = user.get('idToken')
            self.args['uid'] = user.get('localId')
            logging.debug('%s logged in to %s.'%(mail,self.args.get('authDomain')))
            # self.auth.get_account_info(self.args.get('token'))

        except HTTPError as e:
            from ast import literal_eval 
            errobj = literal_eval(e.strerror).get('error')
            logging.error('%s error while login %s (%s)'%(errobj.get('code'),mail,errobj.get('message')))
        return self

    def logout(self,data={}):
        logging.debug('%s logged out from %s.'%(mail,self.args.get('authDomain')))
        return self

class FirebaseServer(object):
    def __init__(self):
        self.args = {'emitter':None,'path':'jay-sidis-a93484ec6cff.json'}
        self.events = {}
        self.admin = None
        self.auth = None

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,data={}):
        from firebase_admin.credentials import Certificate
        cred = Certificate(self.args.get('path'))
        from firebase_admin import initialize_app, auth
        self.admin = initialize_app(cred)
        self.auth = auth

        # self.auth.verify_id_token(id_token)

        return self