"""Sistema acadêmico simples (versão didática)

Este arquivo implementa um conjunto mínimo de funções para gerenciar:
- cursos (código, nome)
- disciplinas (código, nome)
- professores (matrícula, nome, disciplina, curso)
- alunos (matrícula, nome, curso)
- notas (aluno, disciplina, nota)

As estruturas são em memória (dicionários) e o programa é intencionalmente
simples para facilitar o entendimento e uso com conceitos básicos de Python.

Regras principais implementadas:
- A média para aprovação é >= 7.0
- Se média < 7 e >= 4, o sistema mostra as disciplinas abaixo do esperado e
  permite alterar notas.
- Se média < 4, o aluno é reprovado no curso.
- Para concluir o curso um aluno deve ter ao menos 10 disciplinas aprovadas.
"""

from datetime import date

# Estruturas de dados principais: dicionários simples
# - cursos: {codigo: nome}
# - disciplinas: {codigo: nome}
# - professores: {matricula: {"nome": ..., "disciplina": codigo, "curso": codigo}}
# - alunos: {matricula: {"nome": ..., "curso": codigo}}
# - notas: {(aluno_matricula, disciplina_codigo): nota_float}

cursos = {}
disciplinas = {}
professores = {}
alunos = {}
notas = {}


def cadastrar_curso(codigo, nome):
    """Cadastra um curso se o código não existir."""
    if codigo in cursos:
        return False, "Código de curso já existe."
    cursos[codigo] = nome
    return True, "Curso cadastrado."


def cadastrar_disciplina(codigo, nome):
    """Cadastra uma disciplina se o código não existir."""
    if codigo in disciplinas:
        return False, "Código de disciplina já existe."
    disciplinas[codigo] = nome
    return True, "Disciplina cadastrada."


def cadastrar_professor(matricula, nome, disciplina_codigo, curso_codigo):
    """Cadastra professor com referências para disciplina e curso."""
    if matricula in professores:
        return False, "Matrícula de professor já existe."
    if disciplina_codigo not in disciplinas:
        return False, "Disciplina não encontrada. Cadastre a disciplina primeiro."
    if curso_codigo not in cursos:
        return False, "Curso não encontrado. Cadastre o curso primeiro."
    professores[matricula] = {
        "nome": nome,
        "disciplina": disciplina_codigo,
        "curso": curso_codigo,
    }
    return True, "Professor cadastrado."


def cadastrar_aluno(matricula, nome, curso_codigo):
    """Cadastra aluno vinculado a um curso."""
    if matricula in alunos:
        return False, "Matrícula de aluno já existe."
    if curso_codigo not in cursos:
        return False, "Curso não encontrado."
    alunos[matricula] = {"nome": nome, "curso": curso_codigo}
    return True, "Aluno cadastrado."


def lancar_nota(aluno_matricula, disciplina_codigo, nota):
    """Registra ou atualiza uma nota para aluno e disciplina.

    Nota deve estar entre 0 e 10.
    """
    if aluno_matricula not in alunos:
        return False, "Aluno não cadastrado."
    if disciplina_codigo not in disciplinas:
        return False, "Disciplina não cadastrada."
    try:
        nota_float = float(nota)
    except (TypeError, ValueError):
        return False, "Nota inválida. Use um número entre 0 e 10."
    if not (0 <= nota_float <= 10):
        return False, "Nota fora do intervalo 0-10."
    notas[(aluno_matricula, disciplina_codigo)] = nota_float
    return True, "Nota registrada/atualizada."


def calcular_media(aluno_matricula):
    """Calcula a média simples das notas de um aluno.

    Retorna (media, lista_de_notas) onde lista_de_notas é lista de tuples
    (disciplina_codigo, nota).
    """
    itens = [((a, d), n) for (a, d), n in notas.items() if a == aluno_matricula]
    if not itens:
        return None, []
    notas_list = [(d, n) for ((a, d), n) in itens]
    soma = sum(n for d, n in notas_list)
    media = soma / len(notas_list)
    return media, notas_list


def disciplinas_baixas(aluno_matricula, limite=7.0):
    """Retorna disciplinas em que o aluno obteve nota menor que 'limite'."""
    _, notas_list = calcular_media(aluno_matricula)
    return [(d, n) for (d, n) in notas_list if n < limite]


def relatorio_alunos():
    """Retorna uma lista de todos os alunos cadastrados."""
    return [(m, info["nome"], info["curso"]) for m, info in alunos.items()]


def relatorio_professores():
    return [(m, info["nome"], info["disciplina"], info["curso"]) for m, info in professores.items()]


def relatorio_cursos():
    return list(cursos.items())


def relatorio_disciplinas():
    return list(disciplinas.items())


def relatorio_alunos_por_curso(curso_codigo):
    return [(m, info["nome"]) for m, info in alunos.items() if info["curso"] == curso_codigo]


def relatorio_alunos_por_disciplina(disciplina_codigo):
    # alunos que têm nota lançada naquela disciplina
    r = []
    for (a, d), n in notas.items():
        if d == disciplina_codigo:
            r.append((a, alunos.get(a, {}).get("nome", "(nome desconhecido)"), n))
    return r


def relatorio_aluno_completo(aluno_matricula):
    """Relatório com nome do aluno, curso e todas as notas por disciplina."""
    aluno = alunos.get(aluno_matricula)
    if not aluno:
        return None
    media, notas_list = calcular_media(aluno_matricula)
    detalhes = [(disciplinas.get(d, "(disciplina desconhecida)"), n) for d, n in notas_list]
    return {"matricula": aluno_matricula, "nome": aluno["nome"], "curso": cursos.get(aluno["curso"], "(curso desconhecido)"), "media": media, "notas": detalhes}


def aprovado_em_disciplina(nota, limite=7.0):
    return nota >= limite


def contar_aprovadas(aluno_matricula, limite=7.0):
    _, notas_list = calcular_media(aluno_matricula)
    return sum(1 for d, n in notas_list if aprovado_em_disciplina(n, limite))


def emitir_certificado(aluno_matricula):
    """Emite um certificado simples se o aluno tiver >= 10 disciplinas aprovadas."""
    aluno = alunos.get(aluno_matricula)
    if not aluno:
        return False, "Aluno não encontrado."
    aprovadas = contar_aprovadas(aluno_matricula)
    if aprovadas < 10:
        return False, f"Aluno tem {aprovadas} disciplinas aprovadas; precisa de 10 para concluir."
    texto = f"Certificamos que {aluno['nome']} concluiu o curso {cursos.get(aluno['curso'],'(curso desconhecido)')} em {date.today().isoformat()}."
    return True, texto