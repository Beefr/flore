

class Ticket(object):


    def __init__(self, application, couloir, typeTicket, train=None):
        self._application= application
        self._couloir= couloir
        self._train= train
        self._typeTicket=typeTicket
        # il faut aller chercher les autres datas dans la BDD à partir de ces trois infos

    @property
    def application(self):
        return self._application

  
    @application.setter
    def application(self, application):
        self._application=application

    @property
    def couloir(self):
        return self._couloir

  
    @couloir.setter
    def couloir(self, couloir):
        self._couloir=couloir

    @property
    def typeTicket(self):
        return self._typeTicket

  
    @typeTicket.setter
    def typeTicket(self, typeTicket):
        self._typeTicket=typeTicket

    @property
    def train(self):
        return self._train

  
    @train.setter
    def train(self, train):
        self._train=train

  