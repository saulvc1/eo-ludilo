from libraro.statiskaPrilaborilo import StatiskaPrilaborilo
from libraro.disigilo import Disigilo, NekonataVorto
import unittest, json

from collections import defaultdict
from random import shuffle


disigilo = Disigilo(troviEnLaVortaro=False)
with open('./datoj/vortaro/datumoj.json', 'r') as datumojFile:
    prefiksoj, sufiksoj, radikoj, nedividebloj, vortaro_ = json.load(datumojFile)
    vortaro = {k.lower():v for k,v in vortaro_.items()}
    del vortaro['blabla!']

vortoj = []

class TestSum(unittest.TestCase):

    def test_1(self):
        global vortoj

        d = disigilo.vortaro
        #disigilo.vortaro = {}

        count = 0
        print(f'1. Provo de disigado (op2 kaj op3). Nur 5 malsamaj disigoj (el {len(vortaro)}) estas permestaj.')
        for vorto, (silaboj,origino) in vortaro.items():
            if vorto in ['ien']:
                continue

            if vorto.endswith('j'):
                continue

            if ' 'in vorto:
                continue
            a = [
                silabo.lower()
                for silabo in silaboj
            ]
            #if vorto == 'abrahamo':
            #    breakpoint()
            try:
                b, simplaVorto = disigilo.disigiVorton(vorto)
            except NekonataVorto as error:
                breakpoint()

            if a != b:
                print(f'--- silaboj:{a} - disigxita {b} ---')
                count += 1
            else:
                vortoj.append(simplaVorto)

        self.assertTrue(count <= 5)

    def test_2(self):
        global vortoj

        print('2. Provo de kalkulado de vortoj.')

        buffer = ''
        kalkulo = defaultdict(lambda: 0)
        for vorto in vortoj:
            if '-' not in vorto:
                kalkulo[vorto] += 1
                buffer += vorto + ' '

        sp = StatiskaPrilaborilo()
        disigilo.kuru(buffer, iloj = [sp])
        for k,v in kalkulo.items():
            if len(k) > 1 and sp.vortaro[k] != v:
                self.assertEqual(sp.vortaro[k], v, k)
        

if __name__ == '__main__':
    unittest.main()