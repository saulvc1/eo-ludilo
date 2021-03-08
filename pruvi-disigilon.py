from libraro.statiskaPrilaborilo import StatiskaPrilaborilo
from libraro.disigilo import Disigilo
import unittest, json

from collections import defaultdict
from random import shuffle


disigilo = Disigilo(troviEnLaVortaro=False)
with open('./datoj/vortaro/vortaro.json', 'r') as datumojFile:
    radikoj, vortaro = json.load(datumojFile)

vortoj = []

class TestSum(unittest.TestCase):

    def test_1(self):
        global vortoj

        d = disigilo.vortaro
        #disigilo.vortaro = {}

        count = 0
        for vorto, silaboj in vortaro.items():
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
            b, _ = disigilo.disigiVorton(vorto)

            if a != b:
                print(f'--- silaboj:{a} - disigxita {b} ---')
                count += 1
            else:
                vortoj.append(vorto)

        self.assertTrue(count <= 5)
        print(f'\nKontrolitaj vortoj: {count}. Farita!\n')

    def test_2(self):
        global vortoj

        print('Provo de kalkulo.')

        buffer = ''
        kalkulo = defaultdict(lambda: 0)
        for silaboj in vortoj:
            for silabo in silaboj:
                kalkulo[silabo] += 1
                buffer += silabo + ' '
        
        print('Kalkulanta.')

        sp = StatiskaPrilaborilo()
        disigilo.kuru(buffer, iloj = [sp])
        for k,v in kalkulo.items():
            if len(k) > 1 and sp.statistikojDic[k] != v:
                self.assertEqual(sp.statistikojDic[k], v, k)
        

if __name__ == '__main__':
    unittest.main()