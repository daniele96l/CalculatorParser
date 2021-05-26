

import parserOriginal


while True:
    text = input('basic > ')
    try:
        result, error = parserOriginal.run('<stdin>', text)
        if error:
            print(error.as_string())
        else:
            pass
    except:

        print("wrong syntax")

    #result, error = parserOriginal.run('<stdin>', text)

