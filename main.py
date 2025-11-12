"""Menu interativo para o sistema acadêmico didático.

Uso:
 - python main.py           # abre o menu interativo
 - python main.py --demo    # executa um fluxo de demonstração não interativo
"""

import sys
from academicos import (
    cadastrar_curso,
    cadastrar_disciplina,
    cadastrar_professor,
    cadastrar_aluno,
    lancar_nota,
    relatorio_aluno_completo,
    relatorio_alunos,
    relatorio_professores,
    relatorio_cursos,
    relatorio_disciplinas,
    relatorio_alunos_por_curso,
    relatorio_alunos_por_disciplina,
    emitir_certificado,
)


def demo():
    """Executa um pequeno fluxo de demonstração (não-interativo)."""
    print("Executando demo rápida...")
    cadastrar_curso('C01', 'Ciência da Computação')
    cadastrar_curso('C02', 'Engenharia')
    cadastrar_disciplina('D01', 'Algoritmos')
    cadastrar_disciplina('D02', 'Cálculo')
    cadastrar_aluno('A100', 'Maria', 'C01')
    cadastrar_aluno('A101', 'João', 'C01')
    cadastrar_professor('P01', 'Prof. Ana', 'D01', 'C01')
    lancar_nota('A100', 'D01', 8.5)
    lancar_nota('A100', 'D02', 6.0)
    lancar_nota('A101', 'D01', 5.5)
    print('\nRelatório aluno completo (A100):')
    print(relatorio_aluno_completo('A100'))
    print('\nRelatório alunos:')
    print(relatorio_alunos())
    print('\nRelatório professores:')
    print(relatorio_professores())
    print('\nRelatório cursos:')
    print(relatorio_cursos())
    print('\nRelatório disciplinas:')
    print(relatorio_disciplinas())
    print('\nRelatório alunos por disciplina (D01):')
    print(relatorio_alunos_por_disciplina('D01'))
    ok, texto = emitir_certificado('A100')
    print('\nEmitir certificado A100:')
    print(ok, texto)


def ler_input(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print('\nEntrada interrompida pelo usuário.')
        return ''


def menu():
    while True:
        print('\n--- Sistema Acadêmico (menu) ---')
        print('1. Cadastrar curso')
        print('2. Cadastrar disciplina')
        print('3. Cadastrar professor')
        print('4. Cadastrar aluno')
        print('5. Lançar nota')
        print('6. Relatórios')
        print('7. Emitir certificado')
        print('8. Sair')
        escolha = ler_input('Escolha uma opção (1-8): ')
        if escolha == '1':
            codigo = ler_input('Código do curso: ')
            nome = ler_input('Nome do curso: ')
            ok, msg = cadastrar_curso(codigo, nome)
            print(msg)
        elif escolha == '2':
            codigo = ler_input('Código da disciplina: ')
            nome = ler_input('Nome da disciplina: ')
            ok, msg = cadastrar_disciplina(codigo, nome)
            print(msg)
        elif escolha == '3':
            matricula = ler_input('Matrícula do professor: ')
            nome = ler_input('Nome do professor: ')
            disciplina = ler_input('Código da disciplina: ')
            curso = ler_input('Código do curso: ')
            ok, msg = cadastrar_professor(matricula, nome, disciplina, curso)
            print(msg)
        elif escolha == '4':
            matricula = ler_input('Matrícula do aluno: ')
            nome = ler_input('Nome do aluno: ')
            curso = ler_input('Código do curso: ')
            ok, msg = cadastrar_aluno(matricula, nome, curso)
            print(msg)
        elif escolha == '5':
            aluno = ler_input('Matrícula do aluno: ')
            disciplina = ler_input('Código da disciplina: ')
            nota = ler_input('Nota (0-10): ')
            ok, msg = lancar_nota(aluno, disciplina, nota)
            print(msg)
        elif escolha == '6':
            print('\n--- Relatórios ---')
            print('a. Todos os alunos')
            print('b. Todos os professores')
            print('c. Cursos')
            print('d. Disciplinas')
            print('e. Alunos por curso')
            print('f. Alunos por disciplina')
            print('g. Relatório aluno completo')
            sub = ler_input('Escolha (a-g): ')
            if sub == 'a':
                print(relatorio_alunos())
            elif sub == 'b':
                print(relatorio_professores())
            elif sub == 'c':
                print(relatorio_cursos())
            elif sub == 'd':
                print(relatorio_disciplinas())
            elif sub == 'e':
                curso = ler_input('Código do curso: ')
                print(relatorio_alunos_por_curso(curso))
            elif sub == 'f':
                disc = ler_input('Código da disciplina: ')
                print(relatorio_alunos_por_disciplina(disc))
            elif sub == 'g':
                mat = ler_input('Matrícula do aluno: ')
                print(relatorio_aluno_completo(mat))
            else:
                print('Opção inválida.')
        elif escolha == '7':
            mat = ler_input('Matrícula do aluno: ')
            ok, texto = emitir_certificado(mat)
            print(texto)
        elif escolha == '8':
            print('Saindo. Até logo!')
            break
        else:
            print('Opção inválida, tente novamente.')


if __name__ == '__main__':
    if '--demo' in sys.argv:
        demo()
        sys.exit(0)
    try:
        menu()
    except KeyboardInterrupt:
        print('\nPrograma interrompido pelo usuário.')
