# 1. Inverter uma string ou lista (O jeito Pythonico vs O jeito clássico)
texto = "DaniloMelo"
# Jeito Pythonico (Slicing) - Rápido e performático
invertido_pythonico = texto[::-1] 
print(f"Invertido (Pythonico): {invertido_pythonico}")

# 2. Resolução do clássico "Two Sum" (Encontrar dois números que somam um alvo)
# Abordagem eficiente usando Dicionário (Complexidade de Tempo: O(n))
def dois_soma(nums, alvo):
    valores_vistos = {}  # valor : indice
    for indice, num in enumerate(nums):
        complemento = alvo - num
        if complemento in valores_vistos:
            return [valores_vistos[complemento], indice]
        valores_vistos[num] = indice
    return []

print(dois_soma([2, 7, 11, 15], 9))  # Saída: [0, 1] (porque 2 + 7 = 9)


# 3. Remover duplicatas mantendo a ordem original
lista_com_duplicatas = [1, 2, 2, 3, 4, 4, 1]
# Usar dict.fromkeys() é o jeito mais rápido mantendo a ordem
lista_limpa = list(dict.fromkeys(lista_com_duplicatas))
print(lista_limpa)  # Saída: [1, 2, 3, 4]
