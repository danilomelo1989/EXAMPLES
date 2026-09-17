def calcular_digitos_cpf(cpf_nove_digitos: str) -> str:
    """
    Calcula os dois dígitos verificadores de um CPF a partir dos 9 primeiros dígitos.
    Recebe uma string com 9 números e retorna uma string com os 2 dígitos calculados.
    """
    # Remove qualquer caractere que não seja número por segurança
    cpf = [int(digito) for digito in cpf_nove_digitos if digito.isdigit()]
    
    if len(cpf) != 9:
        raise ValueError("O CPF de entrada deve conter exatamente 9 dígitos numéricos.")

    # 1º Dígito: Multiplica-se os 9 dígitos por pesos de 10 a 2
    soma_1 = sum(cpf[i] * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1
    cpf.append(digito_1)

    # 2º Dígito: Multiplica-se os 10 dígitos (incluindo o 1º achado) por pesos de 11 a 2
    soma_2 = sum(cpf[i] * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2

    return f"{digito_1}{digito_2}"


# --- Exemplo de Uso Prático ---
if __name__ == "__main__":
    # Exemplo com os 9 primeiros dígitos do CPF do gerador padrão (comum em testes)
    nove_digitos = "277455488"
    digitos_verificadores = calcular_digitos_cpf(nove_digitos)
    
    print(f"9 Dígitos iniciais: {nove_digitos}")
    print(f"Dígitos calculados: {digitos_verificadores}")
    print(f"CPF Completo: {nove_digitos}-{digitos_verificadores}")
