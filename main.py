import os
while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    print("MINISTÉRIO DO MEIO AMBIENTE")
    nivel = input("""Insira seu nível de acesso: 
                  [1] - ACESSO LIVRE
                  [2] - ACESSO LIMITADO
                  [3] - ACESSO RESTRITO                  
-->""")
    match nivel:
        case "1":
            print("Nivel 1 de acesso")
            input("Aperte Qualquer Coisa para continuar")
        case "2":
            print("Nivel 2 de acesso")
            input("Aperte Qualquer Coisa para continuar")
        case "3":
            print("Nivel 3 de acesso")
            input("Aperte Qualquer Coisa para continuar")
        case _:
            print("Insira uma opção valida")
            input("Aperte Qualquer Coisa para continuar")



