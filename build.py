# Crea index.html: versione autonoma (senza account Claude) da aprire o pubblicare ovunque.
src = open('app.html', encoding='utf-8').read()
head = ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Palestra">\n</head>\n<body>\n')
open('index.html', 'w', encoding='utf-8').write(head + src + '\n</body>\n</html>\n')
print('index.html creato')
