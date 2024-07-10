import argparse
import random
import os

# Dicionário contendo todas as informações do jogo
jogo = {
    "tabuleiro": [],
    "jogador_atual": "p",  # Jogador atual (p = peças pretas, v = peças vermelhas)
    "jogador_escolhido": "p",  # Jogador escolhido no início do jogo
    "mensagens": {
        "movimento_invalido": "Movimento inválido. Tente novamente.",
        "jogo_salvo": "Jogo salvo em",
        "jogo_carregado": "Jogo carregado de",
        "arquivo_nao_encontrado": "Arquivo não encontrado",
        "historico_partidas": "Histórico de Partidas:",
        "nenhum_historico": "Nenhum histórico de partidas disponível.",
        "seu_turno": "Seu turno",
        "comando_invalido": "Comando inválido. Tente novamente.",
        "turno_cpu": "Turno da CPU",
        "cpu_venceu": "Você perdeu! CPU venceu.",
        "jogador_venceu": "Parabéns! Você venceu.",
        "jogo_pausado": "Jogo pausado.",
        "arquivos_salvos": "Arquivos salvos disponíveis:",
        "nenhum_arquivo_salvo": "Nenhum arquivo salvo encontrado.",
        "encerrando_jogo": "Encerrando jogo...",
        "regras_jogo": """
        Regras do Jogo de Damas:
        1. O jogo é jogado em um tabuleiro 8x8 entre dois jogadores.
        2. Um jogador controla as peças brancas ('p') and o outro as peças pretas ('v').
        3. As peças se movem diagonalmente para frente, uma casa por vez.
        4. Capturas são feitas pulando sobre uma peça adversária.
        5. Se uma peça atinge a última linha do adversário, ela é promovida a Dama ('P' or 'V') and pode se mover para frente and para trás.
        6. O jogo termina quando um jogador captura todas as peças do adversário or bloqueia seus movimentos.
        """,
        "creditos_jogo": """
        Jogo de Damas desenvolvido por:
        Gabriel Adriano de Almeida Passos
        Versão 1.4.20
        Features futuras:
        Modo multijogador local.
        Peças coloridas.
        """,
        "bem_vindo": "Bem-vindo ao Jogo de Damas!",
        "opcoes_menu": [
            "1. Iniciar Jogo",
            "2. Carregar Jogo",
            "3. Histórico de Partidas",
            "4. Configurações",
            "5. Ver Regras",
            "6. Créditos",
            "7. Sair",
        ],
        "escolha_invalida": "Escolha inválida. Tente novamente.",
        "use_iniciar": "Use --iniciar para começar o jogo pelo menu principal or consulte --help para mais opções.",
    },
}

# Definir local de salvamento
root_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório raiz do script
save_dir = os.path.join(root_dir, "jogos_salvos")  # Diretório para salvar jogos
if not os.path.exists(save_dir):
    os.makedirs(save_dir)  # Criar diretório se não existir

historico_file = os.path.join(
    root_dir, "historico.txt"
)  # Arquivo de histórico de partidas


def criar_tabuleiro():
    # Cria um tabuleiro 8x8 com peças posicionadas para um jogo de damas
    tabuleiro = [[" " for _ in range(8)] for _ in range(8)]
    for i in range(3):
        for j in range(8):
            if (i + j) % 2 != 0:
                tabuleiro[i][j] = "v"  # Posicionar peças vermelhas
    for i in range(5, 8):
        for j in range(8):
            if (i + j) % 2 != 0:
                tabuleiro[i][j] = "p"  # Posicionar peças pretas
    jogo["tabuleiro"] = tabuleiro
    return tabuleiro


def imprimir_tabuleiro(tabuleiro):
    # Imprime o tabuleiro no console
    print("   " + "   ".join(map(str, range(8))))
    print("  +" + "---+" * 8)
    for i, linha in enumerate(tabuleiro):
        print(f"{i} | " + " | ".join(linha) + " |")
        print("  +" + "---+" * 8)


def movimento_valido(tabuleiro, jogador_atual, x_inicial, y_inicial, x_final, y_final):
    # Verifica se o movimento é válido de acordo com as regras do jogo de damas
    if x_final < 0 or x_final >= 8 or y_final < 0 or y_final >= 8:
        return False
    if tabuleiro[x_final][y_final] != " ":
        return False
    peca = tabuleiro[x_inicial][y_inicial].lower()
    if peca != jogador_atual:
        return False
    if peca == "p" and x_final >= x_inicial:
        return False
    if peca == "v" and x_final <= x_inicial:
        return False
    if abs(x_final - x_inicial) == 1 and abs(y_final - y_inicial) == 1:
        return True
    if abs(x_final - x_inicial) == 2 and abs(y_final - y_inicial) == 2:
        x_meio = (x_inicial + x_final) // 2
        y_meio = (y_inicial + y_final) // 2
        if (
            tabuleiro[x_meio][y_meio].lower() != jogador_atual
            and tabuleiro[x_meio][y_meio] != " "
        ):
            return True
    return False


def mover(tabuleiro, jogador_atual, x_inicial, y_inicial, x_final, y_final):
    # Realiza o movimento de uma peça no tabuleiro
    if not movimento_valido(
        tabuleiro, jogador_atual, x_inicial, y_inicial, x_final, y_final
    ):
        print(jogo["mensagens"]["movimento_invalido"])
        return False
    tabuleiro[x_final][y_final] = tabuleiro[x_inicial][y_inicial]
    tabuleiro[x_inicial][y_inicial] = " "
    if abs(x_final - x_inicial) == 2:
        x_meio = (x_inicial + x_final) // 2
        y_meio = (y_inicial + y_final) // 2
        tabuleiro[x_meio][y_meio] = " "
    promover_dama(tabuleiro, x_final, y_final)
    autosave(tabuleiro, jogador_atual)
    return True


def promover_dama(tabuleiro, x, y):
    # Promove uma peça a dama se atingir a última linha do adversário
    if tabuleiro[x][y] == "p" and x == 0:
        tabuleiro[x][y] = "P"
    elif tabuleiro[x][y] == "v" and x == 7:
        tabuleiro[x][y] = "V"


def trocar_jogador(jogador_atual):
    # Troca o jogador atual
    return "v" if jogador_atual == "p" else "p"


def movimentos_possiveis(tabuleiro, jogador):
    # Retorna uma lista de movimentos possíveis para o jogador
    movimentos = []
    for x in range(8):
        for y in range(8):
            if tabuleiro[x][y].lower() == jogador:
                for dx in [-1, 1]:
                    for dy in [-1, 1]:
                        if movimento_valido(tabuleiro, jogador, x, y, x + dx, y + dy):
                            movimentos.append((x, y, x + dx, y + dy))
                        if movimento_valido(
                            tabuleiro, jogador, x, y, x + 2 * dx, y + 2 * dy
                        ):
                            movimentos.append((x, y, x + 2 * dx, y + 2 * dy))
    return movimentos


def movimento_cpu(tabuleiro, jogador_atual):
    # Realiza um movimento para a CPU
    movimentos = movimentos_possiveis(tabuleiro, "v")
    capturas = [
        movimento for movimento in movimentos if abs(movimento[2] - movimento[0]) == 2
    ]
    if capturas:
        movimento = random.choice(capturas)
    else:
        movimento = random.choice(movimentos)
    x_inicial, y_inicial, x_final, y_final = movimento
    mover(tabuleiro, jogador_atual, x_inicial, y_inicial, x_final, y_final)


def salvar_jogo(tabuleiro, jogador_atual, nome_arquivo):
    # Salva o estado atual do jogo em um arquivo
    if not nome_arquivo.endswith(".save"):
        nome_arquivo += ".save"
    nome_arquivo = os.path.join(save_dir, nome_arquivo)
    with open(nome_arquivo, "w") as arquivo:
        estado_jogo = "".join(["".join(linha) for linha in tabuleiro])
        arquivo.write(estado_jogo + "\n")
        arquivo.write(jogo["jogador_atual"] + "\n")
    print(f"{jogo['mensagens']['jogo_salvo']} {nome_arquivo}")


def carregar_jogo(nome_arquivo):
    # Carrega o estado do jogo a partir de um arquivo
    if not nome_arquivo.endswith(".save"):
        nome_arquivo += ".save"
    nome_arquivo = os.path.join(save_dir, nome_arquivo)
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()
            estado_jogo = linhas[0].strip()
            tabuleiro = [list(estado_jogo[i : i + 8]) for i in range(0, 64, 8)]
            jogador_atual = linhas[1].strip()
            jogo["tabuleiro"] = tabuleiro
            jogo["jogador_atual"] = jogador_atual
        print(f"{jogo['mensagens']['jogo_carregado']} {nome_arquivo}")
        return True, tabuleiro, jogador_atual
    else:
        print(f"{jogo['mensagens']['arquivo_nao_encontrado']} {nome_arquivo}")
        return False, [], ""


def listar_saves():
    # Lista todos os arquivos de save disponíveis
    return [f for f in os.listdir(save_dir) if f.endswith(".save")]


def autosave(tabuleiro, jogador_atual):
    # Realiza um salvamento automático do jogo
    salvar_jogo(tabuleiro, jogador_atual, "autosave.save")


def adicionar_historico(vencedor):
    # Adiciona uma entrada ao histórico de partidas
    with open(historico_file, "a") as arquivo:
        arquivo.write(f"Vencedor: {vencedor}\n")


def ver_historico():
    # Exibe o histórico de partidas
    if os.path.exists(historico_file):
        with open(historico_file, "r") as arquivo:
            historico = arquivo.readlines()
        if historico:
            print(jogo["mensagens"]["historico_partidas"])
            for entrada in historico:
                print(entrada.strip())
        else:
            print(jogo["mensagens"]["nenhum_historico"])
    else:
        print(jogo["mensagens"]["nenhum_historico"])


def jogar(tabuleiro, jogador_atual):
    # Função principal de jogo, controla o fluxo do jogo
    while True:
        imprimir_tabuleiro(tabuleiro)
        if jogo["jogador_atual"] == "p":
            print(jogo["mensagens"]["seu_turno"])
            comando = input(
                "Digite seu movimento (ex: 2 3 3 4), 'pausar' para pausar o jogo: "
            )
            if comando.lower() == "pausar":
                jogador_atual = menu_pausa(tabuleiro, jogo["jogador_atual"])
                if jogador_atual is None:
                    return
                continue
            else:
                if comando.count(" ") == 3:
                    movimentos = comando.split()
                    if all(mov.isdigit() for mov in movimentos):
                        x_inicial, y_inicial, x_final, y_final = map(int, movimentos)
                        if mover(
                            tabuleiro,
                            jogo["jogador_atual"],
                            x_inicial,
                            y_inicial,
                            x_final,
                            y_final,
                        ):
                            jogo["jogador_atual"] = trocar_jogador(
                                jogo["jogador_atual"]
                            )
                    else:
                        print(jogo["mensagens"]["comando_invalido"])
                else:
                    print(jogo["mensagens"]["comando_invalido"])
        else:
            print(jogo["mensagens"]["turno_cpu"])
            movimento_cpu(tabuleiro, jogo["jogador_atual"])
            jogo["jogador_atual"] = trocar_jogador(jogo["jogador_atual"])
        if not movimentos_possiveis(tabuleiro, "p"):
            print(jogo["mensagens"]["cpu_venceu"])
            adicionar_historico("CPU")
            break
        if not movimentos_possiveis(tabuleiro, "v"):
            print(jogo["mensagens"]["jogador_venceu"])
            adicionar_historico("Jogador")
            break


def menu_pausa(tabuleiro, jogador_atual):
    # Exibe o menu de pausa durante o jogo
    while True:
        print(jogo["mensagens"]["jogo_pausado"])
        print("1. Continuar")
        print("2. Salvar jogo")
        print("3. Carregar jogo")
        print("4. Voltar para o Menu Principal")
        print("5. Encerrar jogo sem salvar")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            return jogador_atual
        elif escolha == "2":
            nome_arquivo = input("Digite o nome do arquivo para salvar: ")
            salvar_jogo(tabuleiro, jogador_atual, nome_arquivo)
        elif escolha == "3":
            saves = listar_saves()
            if saves:
                print(jogo["mensagens"]["arquivos_salvos"])
                for i, save in enumerate(saves, 1):
                    print(f"{i}. {save}")
                escolha = input("Escolha um arquivo pelo número: ")
                if escolha.isdigit() and 1 <= int(escolha) <= len(saves):
                    nome_arquivo = saves[int(escolha) - 1]
                    sucesso, tabuleiro, jogador_atual = carregar_jogo(nome_arquivo)
                    if sucesso:
                        return jogador_atual
                else:
                    print(jogo["mensagens"]["escolha_invalida"])
            else:
                print(jogo["mensagens"]["nenhum_arquivo_salvo"])
        elif escolha == "4":
            return None
        elif escolha == "5":
            print(jogo["mensagens"]["encerrando_jogo"])
            exit()
        else:
            print(jogo["mensagens"]["escolha_invalida"])


def ver_regras():
    # Exibe as regras do jogo
    print(jogo["mensagens"]["regras_jogo"])


def ver_creditos():
    # Exibe os créditos do jogo
    print(jogo["mensagens"]["creditos_jogo"])


def configuracoes():
    # Permite ao jogador configurar o jogo, alterando a cor das peças
    while True:
        print(
            f"Você está jogando com as peças: {'Pretas' if jogo['jogador_escolhido'] == 'p' else 'Brancas'}"
        )
        escolha = input("Deseja mudar a cor das suas peças? (s/n): ").lower()
        if escolha == "s":
            jogo["jogador_escolhido"] = "v" if jogo["jogador_escolhido"] == "p" else "p"
            print(
                f"Agora você está jogando com as peças: {'Pretas' if jogo['jogador_escolhido'] == 'p' else 'Brancas'}"
            )
        elif escolha == "n":
            break
        else:
            print(jogo["mensagens"]["escolha_invalida"])


def menu_inicial():
    # Exibe o menu inicial do jogo
    while True:
        print(jogo["mensagens"]["bem_vindo"])
        for opcao in jogo["mensagens"]["opcoes_menu"]:
            print(opcao)
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            tabuleiro = criar_tabuleiro()
            jogo["jogador_atual"] = jogo["jogador_escolhido"]
            jogar(tabuleiro, jogo["jogador_atual"])
        elif escolha == "2":
            saves = listar_saves()
            if saves:
                print(jogo["mensagens"]["arquivos_salvos"])
                for i, save in enumerate(saves, 1):
                    print(f"{i}. {save}")
                escolha = input("Escolha um arquivo pelo número: ")
                if escolha.isdigit() and 1 <= int(escolha) <= len(saves):
                    nome_arquivo = saves[int(escolha) - 1]
                    sucesso, tabuleiro, jogador_atual = carregar_jogo(nome_arquivo)
                    if sucesso:
                        jogar(tabuleiro, jogo["jogador_atual"])
                else:
                    print(jogo["mensagens"]["escolha_invalida"])
            else:
                print(jogo["mensagens"]["nenhum_arquivo_salvo"])
        elif escolha == "3":
            ver_historico()
        elif escolha == "4":
            configuracoes()
        elif escolha == "5":
            ver_regras()
        elif escolha == "6":
            ver_creditos()
        elif escolha == "7":
            print(jogo["mensagens"]["encerrando_jogo"])
            exit()
        else:
            print(jogo["mensagens"]["escolha_invalida"])


def main():
    # Função principal que trata os argumentos de linha de comando and inicia o jogo
    parser = argparse.ArgumentParser(description="Jogo de Damas")
    parser.add_argument("--iniciar", action="store_true", help="Iniciar o jogo")
    parser.add_argument(
        "--novo", action="store_true", help="Inicia novo jogo sem passar pelo menu."
    )
    parser.add_argument("--carregar", action="store_true", help="Carregar jogo")
    parser.add_argument(
        "--config", action="store_true", help="Vai direto para as configurações."
    )
    parser.add_argument(
        "--regras", action="store_true", help="Vai direto para as regras."
    )
    parser.add_argument(
        "--creditos", action="store_true", help="Vai direto para os créditos."
    )
    parser.add_argument("--file", type=str, help="Arquivo para carregar jogo")

    args = parser.parse_args()

    if args.iniciar:
        menu_inicial()
    elif args.novo:
        tabuleiro = criar_tabuleiro()
        jogo["jogador_atual"] = jogo["jogador_escolhido"]
        jogar(tabuleiro, jogo["jogador_atual"])
    elif args.carregar:
        if args.file:
            sucesso, tabuleiro, jogador_atual = carregar_jogo(args.file)
            if sucesso:
                jogar(tabuleiro, jogo["jogador_atual"])
        else:
            print("Especifique o arquivo para carregar usando --file.")
    elif args.config:
        configuracoes()
    elif args.regras:
        ver_regras()
    elif args.creditos:
        ver_creditos()
    else:
        print(jogo["mensagens"]["use_iniciar"])


if __name__ == "__main__":
    main()
