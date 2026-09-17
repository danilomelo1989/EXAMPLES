# 1. O método __init__ e o conceito de POO básico
class Desenvolvedor:
    def __init__(self, nome, stack):
        self.nome = nome          # Atributo de instância
        self.stack = stack

    # Método mágico para representação em string legível
    def __str__(self):
        return f"Dev: {self.nome} | Stack: {self.stack}"

dev = Desenvolvedor("Ana", "Python/Django")
print(dev)  # Saída: Dev: Ana | Stack: Python/Django


# 2. Geradores (Uso eficiente de memória com 'yield')
# O RECRUTADOR PERGUNTA: Como ler um arquivo gigante ou sequência sem estourar a memória?
def gerador_numeros(maximo):
    n = 1
    while n <= maximo:
        yield n  # Retorna o valor atual e pausa a execução, sem salvar tudo na memória
        n += 1

g = gerador_numeros(1000000)
print(next(g))  # Saída: 1
print(next(g))  # Saída: 2
print(next(g))  # Saída: 3
print(next(g))  # Saída: 4