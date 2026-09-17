# 1. List Comprehensions (Muito cobrado para avaliar legibilidade e performance)
# Filtrar números pares elevados ao quadrado
numeros = [1, 2, 3, 4, 5, 6]
quadrados_pares = [x**2 for x in numeros if x % 2 == 0]
print(f"Pares ao quadrado: {quadrados_pares}")  # Saída: [4, 16]


# 2. A pegadinha dos argumentos mutáveis padrão em funções
# O RECRUTADOR PERGUNTA: O que acontece se chamarmos a função abaixo três vezes?
def adiciona_item(item, lista=[]):
    lista.append(item)
    return lista

print(adiciona_item(1))  # Saída: [1]
print(adiciona_item(2))  # Saída: [1, 2] -> A lista persiste entre as chamadas!
# EXPLICAÇÃO: Em Python, os argumentos padrão são avaliados apenas uma vez quando a função é definida.
# CORREÇÃO: Usar `lista=None` e inicializar dentro da função se for None.


# 3. Diferença entre Listas (Mutáveis) e Tuplas (Imutáveis)
minha_lista = [1, 2, 3]
minha_lista[0] = 99  # Funciona perfeitamente

minha_tupla = (1, 2, 3)
# minha_tupla[0] = 99  # Erro! TypeError (Ótimo para chaves de dicionários ou dados protegidos)
