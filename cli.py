import re
from utils import clear_screen, pause, le_int
from validator import MegaSenaValidator
from lotofacil_validator import LotofacilValidator
from quina_validator import QuinaValidator
from downloader import (
    download_and_process,
    download_and_process_lotofacil,
    download_and_process_quina,
)
from utils import get_last_concurso

def run_cli(mega_concurso=None, loto_concurso=None, quina_concurso=None):
    """Executa o menu interativo da aplicação.

    Args:
        mega_concurso: último concurso disponível da Mega-Sena.
        loto_concurso: último concurso disponível da Lotofácil.
        quina_concurso: último concurso disponível da Quina.
    """

    validator = MegaSenaValidator()
    lf_validator = LotofacilValidator()
    qn_validator = QuinaValidator()

    def gerar_menu(nome, validador, min_dz, max_dz, res_len):

        width = 46
        while True:
            clear_screen()
            print('\033[1;96m╔' + '═' * width + '╗\033[0m')
            print('\033[1;96m║\033[1;95m' + f'★ {nome.upper()} ★'.center(width) + '\033[1;96m║\033[0m')
            print('\033[1;96m╟' + '─' * width + '╢\033[0m')
            print(f"\033[1;94m║ 1)\033[0m \033[1;97mGerar apostas".ljust(width) + '\033[1;96m║\033[0m')
            print(f"\033[1;94m║ 2)\033[0m \033[1;97mGerar apostas com pesos".ljust(width) + '\033[1;96m║\033[0m')
            print(f"\033[1;94m║ 3)\033[0m \033[1;97mChecar resultados".ljust(width) + '\033[1;96m║\033[0m')
            print(f"\033[1;94m║ 0)\033[0m \033[1;91mVoltar".ljust(width) + '\033[1;96m║\033[0m')
            print('\033[1;96m╚' + '═' * width + '╝\033[0m')


            opc = input('\033[1;93mEscolha ▶ \033[0m').strip()

            if opc == '1':
                n = le_int("Quantas apostas? ", 1, 500)
                d = le_int(f"Quantas dezenas por aposta ({min_dz}–{max_dz})? ", min_dz, max_dz)
                print('\n\033[1;92m⏳ Gerando apostas…\033[0m')
                aps = validador.gerar_apostas(n, d)
                fn = validador.salvar_apostas(aps, n, d)
                print(f"\033[1;92m✔ Salvo em: {fn}\033[0m")
                pause()

            elif opc == '2':
                n = le_int("Quantas apostas? ", 1, 500)
                d = le_int(f"Quantas dezenas por aposta ({min_dz}–{max_dz})? ", min_dz, max_dz)
                print('\n\033[1;92m⏳ Gerando apostas com pesos…\033[0m')
                aps = validador.gerar_apostas_pesos(n, d)
                fn = validador.salvar_apostas(aps, n, d)
                print(f"\033[1;92m✔ Salvo em: {fn}\033[0m")
                pause()

            elif opc == '3':
                path = input("\033[1;93mCaminho do Excel ▶ \033[0m").strip()
                entrada = input(f"\033[1;93mResultado ({res_len} números separados) ▶ \033[0m")
                nums = [int(x) for x in re.split(r'[\s,;]+', entrada) if x.isdigit()]
                if len(nums) != res_len:
                    print(f"\033[1;91m✖ Informe exatamente {res_len} números.\033[0m")
                elif any(n < 1 or n > (60 if res_len == 6 else (25 if res_len == 15 else 80)) for n in nums):
                    lim = 60 if res_len == 6 else (25 if res_len == 15 else 80)
                    print(f"\033[1;91m✖ Todos os números devem estar entre 1 e {lim}.\033[0m")
                elif len(nums) != len(set(nums)):
                    print("\033[1;91m✖ Não repita números.\033[0m")
                else:
                    print('\n\033[1;92m🔍 Checando resultado…\033[0m')
                    validador.checar_resultado(path, nums)
                pause()

            elif opc == '0':
                break
            else:
                print('\033[1;91m✖ Opção inválida.\033[0m')
                pause()


    width = 46
    while True:
        clear_screen()
        print('\033[1;96m╔' + '═' * width + '╗\033[0m')
        print('\033[1;96m║\033[1;95m' + '✦ MEGA-SENA TOOLS V.2.0 ✦'.center(width) + '\033[1;96m║\033[0m')
        print('\033[1;96m╟' + '─' * width + '╢\033[0m')

        print('\033[1;92mJogos atualizados para os últimos concursos!\033[0m')
        if mega_concurso:
            print(f'Mega-sena: Concurso {mega_concurso}')
        else:
            print('Mega-sena: ?')
        if loto_concurso:
            print(f'Lotofácil: Concurso {loto_concurso}')
        else:
            print('Lotofácil: ?')
        if quina_concurso:
            print(f'Quina: Concurso {quina_concurso}')
        else:
            print('Quina: ?')
        print('\nSelecione o jogo:')
        print(' 1) Mega Sena')
        print(' 2) Lotofácil')
        print(' 3) Quina')
        print(' 4) Atualizar banco de dados')
        print(' 0) Sair')

        opc = input('\033[1;93mEscolha ▶ \033[0m').strip()

        if opc == '1':
            gerar_menu('Mega-Sena', validator, 6, 20, 6)
        elif opc == '2':
            gerar_menu('Lotofácil', lf_validator, 15, 20, 15)
        elif opc == '3':
            gerar_menu('Quina', qn_validator, 5, 15, 5)
        elif opc == '4':
            print('\n\033[1;92m🌐 Atualizando base de dados…\033[0m')
            m_path = download_and_process()
            l_path = download_and_process_lotofacil()
            q_path = download_and_process_quina()
            mega_concurso = get_last_concurso(m_path)
            loto_concurso = get_last_concurso(l_path)
            quina_concurso = get_last_concurso(q_path)
            print('\033[1;92m✔ Bases atualizadas.\033[0m')
            pause()
        elif opc == '0':
            print('\n\033[1;91m🔒 Encerrando Mega-Sena Tools. Até a próxima!\033[0m')
            import sys
            sys.exit(0)
        else:
            print('\033[1;91m✖ Opção inválida.\033[0m')
            pause()
