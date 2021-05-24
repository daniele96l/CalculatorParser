

import parserOriginal


while True:
    text = input('basic > ')
    result, error = parserOriginal.run('<stdin>', text)
    #result, error = parserOriginal.run('<stdin>', text)

    if error: print(error.as_string())
    else: pass