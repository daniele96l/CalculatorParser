

import parserOriginal


while True:

    print("Let's first run each part of the code to know that everything works")
    print("Input test: z+a+c+a*b+func(x)")
    try:
        result, error = parserOriginal.Test()
        if error:
            print(error.as_string())
        else:
            pass
    except:
        print("Wrong syntax")

    text = input('basic > ')


    try:
        result, error = parserOriginal.run('<stdin>', text)
        if error:
            print(error.as_string())
        else:
            pass
    except:
        print("Wrong syntax")







    #result, error = parserOriginal.run('<stdin>', text)

