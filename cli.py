import re
from utils import clear_screen, pause, le_int
from validator import MegaSenaValidator
from downloader import download_and_process

def run_cli():
    """Executa o menu interativo da aplicação."""

    validator = MegaSenaValidator()
    
    while True:
        clear_screen()
        # Cabeçalho estilo "terminal sci-fi"
        print('\033[1;96m╔' + '═' * 46 + '╗\033[0m')
        print('\033[1;96m║\033[1;95m' + ' MEGA-SENA TOOLS V.2.0 '.center(46) + '\033[1;96m║\033[0m')
        print('\033[1;96m╠' + '═' * 46 + '╣\033[0m')
        print(f"\033[1;94m║ 1)\033[0m \033[1;97mGerar apostas".ljust(24) + '║')
        print(f"\033[1;94m║ 2)\033[0m \033[1;97mGerar apostas com pesos".ljust(24) + '║')
        print(f"\033[1;94m║ 3)\033[0m \033[1;97mValidar apostas em Excel".ljust(24) + '║')
        print(f"\033[1;94m║ 4)\033[0m \033[1;97mChecar resultado de apostas".ljust(24) + '║')
        print(f"\033[1;94m║ 5)\033[0m \033[1;97mBaixar e processar resultados".ljust(24) + '║')
        print(f"\033[1;94m║ 0)\033[0m \033[1;91mSair do programa".ljust(24) + '║')
        print('\033[1;96m╚' + '═' * 46 + '╝\033[0m')

        opc = input('\033[1;93mEscolha ▶ \033[0m').strip()
        
        if opc == '1':
            n = le_int("Quantas apostas? ", 1, 500)
            d = le_int("Quantas dezenas por aposta (6–20)? ", 6, 20)
            print('\n\033[1;92m⏳ Gerando apostas…\033[0m')
            aps = validator.gerar_apostas(n, d)
            fn = validator.salvar_apostas(aps, n, d)
            print(f"\033[1;92m✔ Salvo em: {fn}\033[0m")
            pause()

        elif opc == '2':
            n = le_int("Quantas apostas? ", 1, 500)
            d = le_int("Quantas dezenas por aposta (6–20)? ", 6, 20)
            print('\n\033[1;92m⏳ Gerando apostas com pesos…\033[0m')
            aps = validator.gerar_apostas_pesos(n, d)
            fn = validator.salvar_apostas(aps, n, d)
            print(f"\033[1;92m✔ Salvo em: {fn}\033[0m")
            pause()

        elif opc == '3':
            path = input("\033[1;93mCaminho do Excel ▶ \033[0m").strip()
            print('\n\033[1;92m🔍 Validando arquivo…\033[0m')
            validator.validar_arquivo(path)
            pause()

        elif opc == '4':
            path = input("\033[1;93mCaminho do Excel ▶ \033[0m").strip()
            entrada = input("\033[1;93mResultado (6 números separados) ▶ \033[0m")
            nums = [int(x) for x in re.split(r'[\s,;]+', entrada) if x.isdigit()]
            if len(nums) != 6:
                print("\033[1;91m✖ Informe exatamente 6 números.\033[0m")
            elif any(n < 1 or n > 60 for n in nums):
                print("\033[1;91m✖ Todos os números devem estar entre 1 e 60.\033[0m")
            elif len(nums) != len(set(nums)):
                print("\033[1;91m✖ Não repita números. Informe 6 valores distintos.\033[0m")
            else:
                print('\n\033[1;92m🔍 Checando resultado…\033[0m')
                validator.checar_resultado(path, nums)
            pause()

        elif opc == '5':
            print('\n\033[1;92m🌐 Baixando e processando…\033[0m')
            download_and_process()
            pause()

        elif opc == '0':
            print('\n\033[1;91m🔒 Encerrando Mega-Sena Tools. Até a próxima!\033[0m')
            import sys
            sys.exit(0)

        else:
            print('\033[1;91m✖ Opção inválida.\033[0m')
            pause() 