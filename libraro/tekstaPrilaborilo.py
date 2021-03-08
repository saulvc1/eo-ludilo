

class TekstaPrilaborilo:
    separeo = '·'

    def __init__(self):
        self.buffer = ''

    def aldoniSilabojn(self, simplaVorto, vorto, silaboj, orto=''):
        if len(silaboj) == 0: # Nekonta vorto
            self.buffer += vorto
        else:
            #if finajxo != '':
            #    silaboj.append(finajxo)

            novVorto = self.separeo.join(silaboj)

            # Alĝustigi majusklojn
            if vorto == vorto.lower():
                novVorto = novVorto.lower()
            elif vorto == vorto.title():
                novVorto = novVorto[0].upper() + novVorto[1:].lower()
            elif vorto == vorto.upper():
                novVorto = novVorto.upper()
            
            self.buffer += novVorto + orto

    def aldoniSpacojn(self, spaco):
        self.buffer += spaco

    def aldoniAlianVorton(self, other, orto):
        self.buffer += other + orto

    def process(self):
        pass