import pickle, os, re, pathlib, json, collections


class NekonataVorto(Exception):
    def __init__(self, message):
        super(NekonataVorto, self).__init__(message)

re_verbo = re.compile('(\w+?)([ioa]n{0,1}t){0,1}(is|as|os|us|u|i)$', re.UNICODE)
re_malverbo = re.compile('(\w+?)([aeio])(j{0,1})(n{0,1})$', re.UNICODE)
re_ajnaFinajxo = re.compile('(\w+?)((?:[ioa]n{0,1}t){0,1}(?:is|as|os|us|[ao]jn|[ao]j|[ao]n|en|[aeio])){0,1}$', re.UNICODE)
re_teksto = re.compile("(\S+)(\s*)", re.U|re.IGNORECASE|re.DOTALL|re.MULTILINE)
re_orto = re.compile("(\W*)([\wĉĝĥĵŝŭ’']+)(\W*)$", re.U|re.I)


re_literoj = [
    (re.compile("cx"), 'ĉ'), # kuracherbo
    (re.compile("gx"), 'ĝ'), # Flughaveno
    (re.compile("h[hx]"), 'ĥ'),
    (re.compile("j[hx]"), 'ĵ'),
    (re.compile("sx"), 'ŝ'),
    (re.compile("ux"), 'ŭ'),

    (re.compile("ĉ"), 'ĉ'), # c+̂
    (re.compile("ĝ"), 'ĝ'), # g+̂
    (re.compile("ĥ"), 'ĥ'), # h+̂
    (re.compile("ĵ"), 'ĵ'), # j+̂
    (re.compile("ŝ"), 'ŝ'), # s+̂
    (re.compile("ŭ"), 'ŭ'), # u+̆
]
def simpligiLiteron(vorto):
    for re_litero, litero in re_literoj:
        vorto = re_litero.sub(litero, vorto)
    return vorto

class Disigilo:
    def __init__(self, aliajVortoj={}, aliajRadikoj=None, troviEnLaVortaro=True):
        self.log = ''

        datumDosiero = pathlib.Path(__file__).parent.parent / 'datoj' / 'vortaro' / 'datumoj.json'
        with datumDosiero.open('r') as datumojFile:
            self.prefiksoj, self.sufiksoj, radikoj, self.nedivideblajVortoj, vortaro_ = json.load(datumojFile)
            # radikoj, vortaro_ = json.load(datumojFile)
            vortaro_ = {k.lower():[x.lower() for x in v] for k,(v,w) in vortaro_.items()}
            radikoj = [x.lower() for x in radikoj]

        for k, v in aliajVortoj.items():
            radikaro_[k.lower()] = v
        
        radikoj = [r for r in radikoj if len(r) > 1]
        radikoj.append('ĉj')
        if aliajRadikoj is not None:
            radikoj.extend(aliajRadikoj)
        
        self.radikoj = radikoj  = sorted(set(radikoj), key=len, reverse=True)
        self.longecoDic = longecoDic = {}
        for i, radiko in enumerate(radikoj):
            len_ = len(radiko)
            if len_ not in longecoDic:
                longecoDic[len_] = i
        
        tmpDic = collections.defaultdict(list)
        vortaro = {}
        radikaro = {}
        self.radikaro = {}
        self.modelaKorpoj = []
        for k, v in vortaro_.items():
            if v[-1] in ['io']:
                vortaro[k] = v
                continue

            novDisigo = v[:]

            if novDisigo[-1] == 'n':
                novDisigo.pop()

            if novDisigo[-1] == 'j':
                novDisigo.pop()

            if novDisigo[-1] in ['a', 'e', 'o', 'i', 'u', 'is', 'as', 'os', 'us']:
                novDisigo.pop()

            tmpDic[''.join(novDisigo)].append((k, novDisigo))

        # Kelo de pruvo
        for simpligitaVorto, v in tmpDic.items():
            # Du vortoj povus sxaini simila sed ili ne estas el la sama origino:
            # ekzemple: Senegal-o, sen-egal-a.  len(v) == 2

            if len(v) == 1:
                radikaro[simpligitaVorto] = v[0][1]
            
            # [('milita', ['milit']), ('militi', ['milit']), ('milito', ['milit'])]
            # [('senegala', ['sen', 'egal']), ('senegalo', ['senegal'])]
            ss = {'-'.join(x[1]) for x in v}
            if len(ss) == 1:
                radikaro[simpligitaVorto] = v[0][1]
            elif not troviEnLaVortaro:
                # La vortaro estas malplena, do la vorto devindas esti inkludita.
                for vv in v:
                    vorto = vv[0]
                    vortaro[vorto] = vortaro_[vorto]

        for vorto in self.nedivideblajVortoj:
            vortaro[vorto] = [vorto]

        # Ambaux "am" ne havas la saman signifon: Ki-am kaj am-i
        '''
        for ant in ['ki', 'ti', 'i', 'ĉi', 'neni']: #ali
            for post in ['u', 'o', 'a', 'e', 'es', 'en', 'am', 'al', 'el', 'om']:
                vorto = ant+post
                if post in 'uoa':
                    radikaro[vorto] = [vorto]
                vortaro[vorto] = [vorto]
        '''

        self.radikaro = radikaro
        self.modelaKorpoj = sorted(radikaro.keys(), key=len, reverse=True)
        if troviEnLaVortaro:
            vortaro_.update(vortaro)
            self.vortaro = vortaro_
        else:
            self.vortaro  = vortaro
        
    
    def simpligi(self, vorto):
        litero = ''
        
        if len(vorto) == 1:
            return [vorto], None

        self.log += f"+Simpligi(vorto='{vorto}')\n"

        finajxoj = []
        bazo = ''
        simplaVorto = vorto

        cxuVerbo = False
        for x in ['is', 'as', 'os', 'us']:
            bazo, finajxo = vorto[:-2], vorto[-2:]
            if finajxo in x:
                finajxoj.insert(0, finajxo)
                self.log += f"-forigi {vorto} --> bazo='{bazo}', finajxo='{finajxo}' in ['is', 'as', 'os', 'us']\n"
                litero = 'i'
                cxuVerbo = True
                simplaVorto = bazo
                yield bazo, finajxoj, bazo + litero

        if not cxuVerbo:
            if vorto[-1] == 'n':
                bazo, finajxo = vorto[:-1], vorto[-1]
                finajxoj.insert(0, finajxo)
                self.log += f"-forigi '{x}' --> bazo='{bazo}', finajxo='{finajxo}'=='n'\n"
            else:
                bazo = vorto
            #print('========', vorto, bazo)
            if bazo[-1] == 'j':
                bazo, finajxo = bazo[:-1], bazo[-1]
                finajxoj.insert(0, finajxo)
                self.log += f"-forigi '{x}' --> bazo='{bazo}', finajxo='{finajxo}'=='j'\n"

            if len(finajxoj) > 0:
                yield bazo, finajxoj, bazo

            bazo, finajxo = bazo[:-1], bazo[-1]
            if finajxo in "aeiou'’":
                finajxoj.insert(0, finajxo)
                self.log += f"-forigi '{x}' --> bazo='{bazo}', finajxo='{finajxo}' in ['n', 'j', 'aeiou']\n"
                litero = finajxo
                simplaVorto = bazo + litero
                yield bazo, finajxoj, simplaVorto

        bazo, finajxo = simplaVorto[:-3], simplaVorto[-3:]
        if finajxo in ['int', 'ant', 'ont']:
            finajxoj.insert(0, finajxo)
            self.log += f"-forigi '{simplaVorto}') --> bazo={bazo}, finajxo={finajxo} in *nt\n"
            yield bazo, finajxoj, bazo + litero
        else:
            bazo, finajxo = simplaVorto[:-2], simplaVorto[-2:]
            if finajxo in ['it', 'at', 'ot']:
                finajxoj.insert(0, finajxo)
                self.log += f"-forigi {simplaVorto}' --> bazo={bazo}, {finajxo} in *t\n"
                yield bazo, finajxoj, bazo + litero

    def maneDisigiVorton(self, bazo):
        if len(bazo) == 1:
            if bazo in 'aeiouj':
                self.log += f"-Pivote('{bazo}')\n"
                return [bazo]
            else:
                #dis-d (disde). Petu la tutan vorton
                raise NekonataVorto(bazo)

        def recursive(silabo, vorto):
            cetero = vorto[len(silabo):]
            if cetero == '':
                return []
            self.log += f"-recursive('{vorto}')\n"
            return self.maneDisigiVorton(cetero)

        for pre in self.prefiksoj:
            if bazo.startswith(pre):
                try:
                    self.log += f"-trovi_pre('{pre}', ('{pre}', '{bazo}'))\n"
                    return [pre, *recursive(pre, bazo)]
                except NekonataVorto:
                    pass
        for morfemoj in [self.radikoj, self.sufiksoj]:
            for rad in morfemoj:
                if bazo.startswith(rad):
                    try:
                        self.log += f"-trovi_rad('{rad}', ('{rad}', '{bazo}'))\n"
                        return [rad, *recursive(rad, bazo)]
                    except NekonataVorto:
                        litero = bazo[len(rad)]
                        if litero in 'aeoi':
                            try:
                                self.log += f"-trovi_rad_litero('{rad}', '{litero}', ('{rad+litero}', '{bazo}'))\n"
                                return [rad, litero, *recursive(rad+litero, bazo)]
                            except NekonataVorto:
                                pass
        if bazo in self.nedivideblajVortoj:
            self.log += f"-uzi_ne_dividebla -->'{bazo}'\n"
            return [bazo]
        raise NekonataVorto(bazo)

    def simplegigi(self, simplaVorto):
        if simplaVorto[-1] in 'jn':
            for i in range(len(simplaVorto)-1, -1, -1):
                if simplaVorto[i] not in 'jn':
                    v = simplaVorto[:i+1]
                    if len(v) > 1:
                        return v 
        return simplaVorto

    def disigiVorton(self, vorto):
        vorto = simpligiLiteron(vorto)

        if vorto[-1] == "'":
            vorto = vorto[:-1] + 'o'
        self.log = "+disigiVorto('vorto')\n"
        
        
        if vorto in self.nedivideblajVortoj:
            self.log += f"-DisVorto Op1.a nedividebla: --> '{vorto}'\n"
            return [vorto], vorto
        try:
            silaboj = self.vortaro[vorto]
            self.log += f"-DisVorto Op1.b: {vorto} --> vortaro['{vorto}'] --> {self.vortaro.get(vorto, None)}\n"
            # return silaboj, vorto if len(silaboj) == 1 else self.simplegigi(vorto)
            return silaboj, vorto
        except KeyError:
            pass

        # Opcio 1: vortaro.
        for bazo, finajxoj, simplaVorto in self.simpligi(vorto):
            try:
                self.log += f"-DisVorto Op1.c: {vorto} --> radikaro['{bazo}'], {finajxoj}'"
                rezulto = [*self.radikaro[bazo], *finajxoj]
                self.log += f" --> {rezulto}\n"
                return rezulto, self.simplegigi(simplaVorto)
            except KeyError:
                try:
                    self.log += f"\n-DisVorto Op1.d: {vorto} --> vortaro['{simplaVorto}'], {finajxoj}"
                    rezulto = [*self.vortaro[simplaVorto], *finajxoj]
                    self.log += f" --> {rezulto}'\n"
                    return rezulto, self.simplegigi(simplaVorto)
                except KeyError:
                    self.log = '\n'
                    continue

        # Opcio 2: vortaro + automata disigo
        for bazo, finajxoj, simplaVorto in self.simpligi(vorto):
            for mKorpo in self.modelaKorpoj:
                if bazo.startswith(mKorpo):
                    cetero = bazo[len(mKorpo):]
                    try:
                        self.log += f"-DisVorto Op2.a: [*radikaro[mKorpo], *maneDisigiVorton(cetero), *finajxoj] --> [*{self.radikaro[mKorpo]}, *maneDisigiVorton('{cetero}'), *{finajxoj}]\n"
                        if cetero == '': # agit
                            return [*self.radikaro[mKorpo], *finajxoj], self.simplegigi(simplaVorto)
                        else:
                            return [*self.radikaro[mKorpo], *self.maneDisigiVorton(cetero), *finajxoj], self.simplegigi(simplaVorto)
                    except NekonataVorto: # ien
                        continue

        # Opcio 3: automata disigo
        for bazo, finajxoj, simplaVorto in self.simpligi(vorto):
            try:
                self.log += f"-DisVorto Op3: {vorto} {bazo}-{finajxoj}\n"
                return [*self.maneDisigiVorton(bazo), *finajxoj], self.simplegigi(simplaVorto)
            except NekonataVorto:
                pass
        return self.maneDisigiVorton(vorto), self.simplegigi(vorto)

    def kuru(self, teksto, iloj=[]):
        for ilo in iloj:
            ilo.disigilo = self
        result = ''
        for parto, spaco in re_teksto.findall(teksto):
            trovitaResulto = re_orto.search(parto)
            if trovitaResulto is None:
                for ilo in iloj:
                    ilo.aldoniAlianVorton(parto, '')
            else:
                orto1, vorto, orto2 = trovitaResulto.groups()
                if orto1 != '':
                    for ilo in iloj:
                        ilo.aldoniSpacojn(orto1)    
                try:
                    silaboj, simplaVorto = self.disigiVorton(vorto.lower())
                except NekonataVorto as error:
                    for ilo in iloj:
                        ilo.aldoniAlianVorton(vorto, orto2)
                else:
                    for ilo in iloj:
                        ilo.aldoniSilabojn(simplaVorto, vorto, silaboj, orto2)

            for ilo in iloj:
                ilo.aldoniSpacojn(spaco)
        for ilo in iloj:
            ilo.process()
        return result

'''
class BL_Disigilo(Disigilo):
    def __init__(self):
        self.blMorfemaro = {}
        with open('./datoj/vortaro/datumoj.json', 'r') as datumojFile:
            self.blVortaro = {}
            for k, v in json.load(datumojFile).items():
                self.blVortaro[k] = v[1][0] if len(v[1]) == 1 else [*v[1][0], f'(BL:{k})']
        for k,v in self.blVortaro.items():
            if len(v[0]) <= 2:
                self.blMorfemaro[v[0]] = self.blVortaro[k] = v[0] if len(v) == 1 else [*v[0], f'(BL:{k})']
        super.__init__(self)

    def disigiVorton(self, vorto):
        silaboj, simplaVorto = super().disigiVorton(vorto.lower())
        for i in range(len(silaboj)):
            if silaboj[i] in blMorfemoj:
                silaboj[i] = blMorfemoj[silaboj[i]]
        return silaboj, simplaVorto
'''


