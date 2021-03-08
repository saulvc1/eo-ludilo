import re
import urllib.request

u2 = urllib.request.urlopen('https://www.gutenberg.org/browse/languages/eo')
rcompiled = re.compile('ebooks\/(\d+)')


for line in u2.readlines():
    match = rcompiled.search(line.decode('utf-8'))
    if match:
        number = match.group(1)
        txtUrl = f'https://www.gutenberg.org/files/{number}/{number}-0.txt'
        print(f'>>> {txtUrl}')
        try:
            u3 = urllib.request.urlopen(txtUrl)
        except urllib.error.HTTPError:
            continue
        filename = f'{number}.txt'
        with open(filename, 'wb') as f:
            f.write(u3.read())
        print (filename)

print('Done!')