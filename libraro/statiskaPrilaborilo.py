from collections import defaultdict 

class StatiskaPrilaborilo:
    def __init__(self):
        self.konataro    = defaultdict(lambda: 0)
        self.nekonataro  = defaultdict(lambda: 0)
        self.vortaro     = defaultdict(lambda: 0)

    def update(self, sp):
        listo = [
            (sp.konataro,   self.konataro),
            (sp.nekonataro, self.nekonataro),
            (sp.vortaro,    self.vortaro),
        ]
        for fonto, destino in listo:
            for k, v in fonto.items():
                destino[k] += v

    def aldoniSilabojn(self, simplaVorto, vorto, silaboj, finajxo='', orto=''):
        for silabo in silaboj:
            if len(silabo) > 1:
                self.konataro[silabo] += 1
        self.vortaro[simplaVorto] += 1

    def aldoniSpacojn(self, spaco):
        pass

    def aldoniAlianVorton(self, other, orto):
        self.nekonataro[other] += 1

    def process(self):
        konatoj   = ', '.join([f'{k}:{v}' for k,v in self.konataro.items()]) 
        nekonatoj = ', '.join([f'{k}:{v}' for k,v in self.nekonataro.items()])
        vortoj    = ', '.join([f'{k}:{v}' for k,v in self.vortaro.items()])
        totalo = len(self.konataro) + len(self.nekonataro)

        self.statistikoj = (
            f'Totalo de konataj vortoj: {len(self.konataro)}\n'
            f'Totalo de konataj vortoj: {len(self.nekonataro)}\n'
            f'Totalo de vortoj: {totalo}\n\n'
            f'Kalkulo de konataj vortoj: {konatoj}\n\n'
            f'Kalkulo de nekonataj vortoj: {nekonatoj}\n\n\n'
            f'Kalkulo de simplaj vortoj: {vortoj}\n\n\n'
        )

    def montriStatiskoj(self):
        print(self.konataro)

    def konProporcio(self):
        # elcento en dekumoj
        if len(self.konataro) > 0:
            totalo = len(self.konataro) + len(self.nekonataro)
            if totalo > 0:
                return len(self.konataro) / totalo
            else:
                return 0
        else:
            return 0