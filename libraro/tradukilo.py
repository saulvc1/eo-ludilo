from collections import defaultdict 
from pathlib import Path

class Morfemoj:
    def __init__(self, disigilo):
        self.disigilo = disigilo

    def __get__(self, obj, objtype=None):
        # ['' for prefikso in self.disigilo.prefiksoj]
        # self.sufiksoj, radikoj, self.nedivideblajVortoj
        l = []
        with open('uvortaro.txt', 'rt', encoding='utf-8') as dosiero:
            for line in dosiero:
                vorto, signifo = line.split(' ', 1)
                vorto = vorto.replace('’', '')
                
                if vorto in self.disigilo.prefiksoj:
                    vorto_ = f'{vorto}-'
                elif vorto in self.disigilo.sufiksoj:
                    vorto_ = f'-{vorto}'
                elif vorto in self.disigilo.radikoj:
                    vorto_ = f'-{vorto}-'
                elif vorto in self.disigilo.nedivideblajVortoj:
                    vorto_ = f'{vorto}'
                l.append((f'{vorto}', signifo))
        return l

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
        self.tradukoj = []
        wokitaboDic = {}
        p = Path(__file__).parent.parent / Path('datoj/vortaro/wokitabo.csv')
        with p.open("rt", encoding="utf-8", errors='ignore') as wokitaboFile:
            wokitaboFile.readline()
            for line in wokitaboFile:
                eo, du, *_ = line.strip().split(',')

                if eo == '' or eo == du or '?' in du or '?' in eo:
                    continue

                if eo[0] == '·':
                    eo = eo[1:]
                if du[0] == '·':
                    du = du[1:]
                if eo[-1] == '·':
                    eo = eo[:-1]
                if du[-1] == '·':
                    du = du[:-1]

                if '·' in eo:
                    cxuRadiko = False
                elif eo[-1] == du[-1] and eo[-1] in 'aioe' and len(eo) > 2 and len(du) > 2:
                    eo = eo[:-2] # Ekz: 'mal·sat·a' --> 'mal·sat' '·a'
                    du = du[:-2]
                    cxuRadiko = True
                elif eo[-1] in 'aeio' and du[-1]  in 'aeio':
                    cxuRadiko = False
                else:
                    cxuRadiko = True
                    
                if cxuRadiko:
                    try:
                        wokitaboDic[eo] = du.split('·')
                    except ValueError:
                        breakpoint()
                else:
                    self.tradukoj.append([f'·{eo}·', f'·{du}·'])

        self.wokitaboDic = wokitaboDic
        self.teksto = ''
        self.lingvaStatiskoj = {}

    def konvertigiLiterojn(self, vorto):
        return (
            vorto
            .replace('sv', 'sw')
            .replace('ŝv', 'sw')
            .replace('ŝp', 'sp')
            .replace('ŝk', 'sk')
            .replace('ŝt', 'st')
            .replace('kv', 'kw')
            .replace('gv', 'gw')
            .replace('j', 'y')
            .replace('ĉ', 'c')
            .replace('ŝ', 'c')
            .replace('ĝ', 'j')
            .replace('ĵ', 'j')
            .replace('ŭ', 'w')
            )

    def tradukiMorfemoj(self, morfemoj):
        novMorfemoj = []
        wokitaboDic = self.wokitaboDic

        for morfemo in morfemoj:
            if morfemo in wokitaboDic:
                for novMorfemo in wokitaboDic[morfemo]:
                    novMorfemoj.append(novMorfemo)
            else:
                novMorfemo = self.konvertigiLiterojn(morfemo)
                novMorfemoj.append(novMorfemo)
        
        return novMorfemoj

    def aldoniSilabojn(self, simplaVorto, vorto, silaboj, orto=''):
        #breakpoint()
        if len(silaboj)==0 and vorto != '':
            print(f"Averto: {vorto}")
            self.aldoniAlianVorton(vorto)
            return

        vorto_ = '·' + '·'.join(silaboj) + '·'
        for eo, du in self.tradukoj:
            vorto_ = vorto_.replace(eo, du)
        silaboj = vorto_[1:-1].split('·')


        wokitaboDic = self.wokitaboDic
        novSilaboj = []
        for silabo in silaboj:
            if silabo in wokitaboDic:
                for novSilabo in wokitaboDic[silabo]:
                    novSilaboj.append(Silabo(novSilabo))
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

