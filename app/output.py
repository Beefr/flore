

class Output(object):


    def __init__(self):
        self._content= { "nom": "salut", "prenom": "aurevoir", "age": "non" }

    @property
    def content(self):
        return self._content

  
    @content.setter
    def content(self, elem):
        self._content+elem

  