from collections import defaultdict 

class Silabo:
    def __init__(self, silabo, krampita=False):
        self.silabo = silabo
        self.krampita = krampita
        self.majuskligo = lambda a: a.lower()

    def __str__(self):
        silabo = self.majuskligo(self.silabo)
        return f'<{silabo}>' if self.krampita else silabo

class Vorto:
    def __init__(self, silaboj):
        self.silaboj = silaboj
    
    def lower(self):
        for s in self.silaboj:
            s.majuskligo = lambda a: a.lower()
        return ''.join([str(s) for s in self.silaboj])

    def upper(self):
        for s in self.silaboj:
            s.majuskligo = lambda a: a.upper()
        return ''.join([str(s) for s in self.silaboj])

    def title(self):
        self.silaboj[0].majuskligo = lambda a: a.title()
        for s in self.silaboj[1:]:
            s.majuskligo = lambda a: a.lower()
        return ''.join([str(s) for s in self.silaboj])

    def __str__(self):
        return ''.join([s.silabo for s in self.silaboj])

class Tradukilo:
    def __init__(self):
        wokitaboDic = {}
        with open('./datoj/vortaro/wokitabo.csv', "rt", encoding="utf-8", errors="replace") as wokitaboFile:
            wokitaboFile.readline()
            for line in wokitaboFile:
                du, eo, *_ = line.strip().split(',')
                if du == eo:
                    continue
                wokitaboDic[eo] = du.replace('/', '')

        self.wokitaboDic = wokitaboDic
        self.teksto = ''
        self.lingvaStatiskoj = {}

    def konvertigiLiterojn(self, vorto):

        return vorto\
            .replace('sv', 'sw')\
            .replace('ŝv', 'sw')\
            .replace('ŝp', 'sp')\
            .replace('ŝk', 'sk')\
            .replace('ŝt', 'st')\
            .replace('kv', 'kw')\
            .replace('gv', 'gw')\
            .replace('j', 'y')\
            .replace('ĉ', 'c')\
            .replace('ŝ', 'c')\
            .replace('ĝ', 'j')\
            .replace('ĵ', 'j')\
            .replace('ŭ', 'w')


    def aldoniSilabojn(self, simplaVorto, vorto, silaboj, orto=''):
        if len(silaboj)==0 and vorto != '':
            print(f"Averto: {vorto}")
            self.aldoniAlianVorton(vorto)
            return

        wokitaboDic = self.wokitaboDic
        novSilaboj = []
        for silabo in silaboj:
            if silabo in wokitaboDic:
                novSilaboj.append(Silabo(wokitaboDic[silabo]))
            else:
                novSilabo = self.konvertigiLiterojn(silabo)
                novSilaboj.append(Silabo(novSilabo, krampita=True))
        novVorto = Vorto(novSilaboj)

        # Alĝustigi majusklojn
        if vorto == vorto.lower():
            novVorto = novVorto.lower()
        elif vorto == vorto.title():
            # novVorto = novVorto[0].upper() + novVorto[1:].lower()
            if len(novVorto.silaboj) == 0:
                breakpoint()
            novVorto = novVorto.title()
        elif vorto == vorto.upper():
            novVorto = novVorto.upper()
        else:
            novVorto = str(novVorto)

        self.teksto += novVorto

    def aldoniSpacojn(self, spacoj):
        self.teksto += spacoj

    def aldoniAlianVorton(self, other, orto):
        self.teksto += self.konvertigiLiterojn(f'«{other}»{orto}')

    def process(self):
        self.lingvaStatiskoj = lingvaStatiskoj = {
            'eR': 0,
            'dR': 0,
            'vortoj': len(self.disigilo.vortaro)
        }
        for radiko in self.disigilo.radikoj:
            lingvaStatiskoj['dR' if radiko in self.wokitaboDic else 'eR'] += 1

        self.statistikoj = f'''Esparantaj radikoj: {lingvaStatiskoj["eR"]}
Wokitablaj radikoj: {lingvaStatiskoj["dR"]}
Totalo de vortoj en Esperanta vortaro: {lingvaStatiskoj["vortoj"]}
'''

