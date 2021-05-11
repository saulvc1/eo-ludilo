from libraro.disigilo import Disigilo


sxablono = '''
{vorto}
\tsimpligi:         {simpligi}
\tmaneDisigiVorton  {mane}
\tdisigiVorton      {disigiVorton} --> {cxuBone}
\tvortaro['{vorto}']: '{EnLaVortaro}'
\tlen(vortaro) {vortLongeco}

Resulto: {resulto}
'''

class ErarSercxilo(Disigilo):
    def __init__(self, aliajVortoj={}, aliajRadikoj=None, troviEnLaVortaro=True):
        super().__init__(aliajVortoj, aliajRadikoj, troviEnLaVortaro)

    def erarSercxiVorton(self, vortoj):
        for vorto in vortoj:
            vorto = vorto.strip()

            d = {
                'vorto': vorto,
                'simpligi':     [x for x in self.simpligi(vorto)],
                'disigiVorton': self.disigiVorton(vorto),
                'EnLaVortaro':  self.vortaro.get(vorto, None),
                'vortLongeco':  len(self.vortaro),
                'resulto':      '·'.join(self.disigiVorton(vorto)[0])
            }

            try:
                d['mane'] = self.maneDisigiVorton(vorto)
            except:
                d['mane'] = 'Nekonata vorto'
            
            
            if vorto in self.nedivideblajVortoj:
                d['cxuBone'] = 'Bone' if vorto == d['disigiVorton'][0][0] else 'Eraro'
            elif vorto in self.vortaro:
                d['cxuBone'] = 'Bone' if self.vortaro[vorto] == d['disigiVorton'][0] else 'Eraro'
            else:
                d['cxuBone'] = 'Ne ekzistas en vortaro. Cxu pravas?'

            print(sxablono.format(**d))
            print(self.log)


# ĵurio jakoben
# ErarSercxilo().erarSercxiVorton(['malantaŭen', 'la', 'viajn'])
ErarSercxilo().erarSercxiVorton(['aĉeti', 'aĉeti'])

