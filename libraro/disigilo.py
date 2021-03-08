import pickle, os, re, pathlib, json, collections

pre_vortoj = (
    "al anstataŭ antaŭ apud ĉe ĉirkaŭ da de dum ekster el en ĝis inter je kontraŭ "    #preposizioj
    "krom kun laŭ malgraŭ per po por post preter pri pro sen sub super sur trans tra " #preposizioj
    "ĉi for ankoraŭ baldaŭ hodiaŭ hieraŭ morgaŭ jam ĵus nun plu tuj ajn almenaŭ "      #advs
    "ankaŭ apenaŭ des do eĉ ja jen jes ju kvazaŭ mem nur preskaŭ tamen tre tro sen "   #advs
    "al el en mis dis eks ek bo fi ge mal pra re"                                     #prefiksoj
    # "mi ni vi li ŝi ĝi ili oni si ci"                                                  #pronomoj
).strip().split(' ')


pronomoj = "mi ni vi li ŝi ĝi ili oni si ci "
konjuncioj = 'aŭ kaj ke kvankam nek ol se sed ĉar '
prefiksoj = 'al el en mis dis eks ek bo fi ge mal pra re '
aliajVortoj = (
    "ne ĉu ho nu"
    "al anstataŭ antaŭ apud ĉe ĉirkaŭ da de dum ekster el en ĝis inter je kontraŭ "    #preposizioj
    "krom kun laŭ malgraŭ per po por post preter pri pro sen sub super sur trans tra " #preposizioj
    "ĉi for ankoraŭ baldaŭ hodiaŭ hieraŭ morgaŭ jam ĵus nun plu tuj ajn almenaŭ "      #advs
    "ankaŭ apenaŭ des do eĉ ja jen jes ju kvazaŭ mem nur preskaŭ tamen tre tro sen"   #advs
)

pre_vortoj = (aliajVortoj + prefiksoj + pronomoj).strip().split(' ')
nedivideblajVortoj = ('la en ' + aliajVortoj + prefiksoj + pronomoj + konjuncioj).strip().split(' ')


class NekonataVorto(Exception):
    def __init__(self, message):
        super(NekonataVorto, self).__init__(message)

re_verbo = re.compile('(\w+?)([ioa]n{0,1}t){0,1}(is|as|os|us|u|i)$', re.UNICODE)
re_malverbo = re.compile('(\w+?)([aeio])(j{0,1})(n{0,1})$', re.UNICODE)
re_ajnaFinajxo = re.compile('(\w+?)((?:[ioa]n{0,1}t){0,1}(?:is|as|os|us|[ao]jn|[ao]j|[ao]n|en|[aeio])){0,1}$', re.UNICODE)
re_teksto = re.compile("(\S+)(\s*)", re.U|re.IGNORECASE|re.DOTALL|re.MULTILINE)
re_orto = re.compile("(\W*)(\w+?)(\W*)$", re.U|re.I)


re_literoj = [
    (re.compile("cx"), 'ĉ'), # kuracherbo
    (re.compile("gx"), 'ĝ'), # Flughaveno
    (re.compile("h[hx]"), 'ĥ'),
    (re.compile("j[hx]"), 'ĵ'),
    (re.compile("sx"), 'ŝ'),
    (re.compile("ux"), 'ŭ'),
]
def simpligiLitero(vorto):
    for re_litero, litero in re_literoj:
        vorto = re_litero.sub(litero, vorto)
    return vorto



class Disigilo:
    def __init__(self, aliajVortoj={}, aliajRadikoj=None, troviEnLaVortaro=True):
        self.log = ''

        with open('./datoj/vortaro/vortaro.json', 'r') as datumojFile:
            radikoj, vortaro_ = json.load(datumojFile)

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

        for vorto in nedivideblajVortoj:
            vortaro[vorto] = [vorto]

        for ant in ['ki', 'ti', 'i', 'ĉi', 'neni']: #ali
            for post in ['u', 'o', 'a', 'e', 'es', 'en', 'am', 'al', 'el', 'om']:
                vorto = ant+post
                if post in 'uoa':
                    radikaro[vorto] = [vorto]
                vortaro[vorto] = [vorto]

        self.radikaro = radikaro
        self.modelaKorpoj = sorted(radikaro.keys(), key=len, reverse=True)
        if troviEnLaVortaro:
            vortaro_.update(vortaro)
            self.vortaro = vortaro_
        else:
            self.vortaro  = vortaro
        
    
    def simpligi(self, vorto):
        litero = ''

        self.log += f"+Simpligi(vorto='{vorto}')\n"

        finajxoj = []
        bazo = ''
        simplaVorto = vorto

        bazo, finajxo = vorto[:-3], vorto[-3:]
        for x in ['ĉjo', 'njo']:
            if finajxo in x:
                finajxoj.insert(0, finajxo)
                self.log += f"-forigi '{vorto}' --> bazo={bazo}, finajxo='{finajxo}' in ['ĉjo', 'njo']\n"
                return
                yield bazo, finajxoj, vorto

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
            for x in ['n', 'j']:
                bazo, finajxo = vorto[:-1], vorto[-1]
                if finajxo in x:
                    finajxoj.insert(0, finajxo)
                    self.log += f"-forigi '{x}' --> bazo='{bazo}', finajxo='{finajxo}' in ['n', 'j', 'aeiou']\n"
                    litero = x
                    simplaVorto = bazo
                    yield bazo, finajxoj, simplaVorto
            
            bazo, finajxo = vorto[:-1], vorto[-1]
            if finajxo in 'aeiou':
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

        for pre in pre_vortoj:
            if bazo.startswith(pre):
                try:
                    self.log += f"-trovi_pre('{pre}', ('{pre}', '{bazo}'))\n"
                    return [pre, *recursive(pre, bazo)]
                except NekonataVorto:
                    pass
        for rad in self.radikoj:
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
        vorto = simpligiLitero(vorto)

        if vorto[-1] == "'":
            vorto[-1] = 'o'
        self.log = "+disigiVorto('vorto')\n"
        
        self.log += f"-DisVorto Op1.a: {vorto} --> vortaro['{vorto}'] --> {self.vortaro.get(vorto, None)}\n"
        try:
            silaboj = self.vortaro[vorto]
            return silaboj, vorto if len(silaboj) == 1 else self.simplegigi(vorto)
        except KeyError:
            pass

        # Opcio 1: vortaro.
        for bazo, finajxoj, simplaVorto in self.simpligi(vorto):
            try:
                self.log += f"-DisVorto Op1.a: {vorto} --> radikaro['{bazo}'], {finajxoj}'"
                rezulto = [*self.radikaro[bazo], *finajxoj]
                self.log += f" --> {rezulto}\n"
                return rezulto, self.simplegigi(simplaVorto)
            except KeyError:
                try:
                    self.log += f"\n-DisVorto Op1.b: {vorto} --> vortaro['{simplaVorto}'], {finajxoj}"
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
        frzKomenco = True

        for ilo in iloj:
            ilo.disigilo = self
        result = ''
        for parto, spaco in re_teksto.findall(teksto):
            trovitaResulto = re_orto.search(parto)
            if trovitaResulto is None:
                for ilo in iloj:
                    ilo.aldoniAlianVorton(parto, '')
            else:
                orto1, vorto, orto2 = re_orto.search(parto).groups()
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

