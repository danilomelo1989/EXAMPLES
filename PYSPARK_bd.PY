import os
import urllib.request
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, sum, desc, round

def processar_dados_spark():
    # 1. Inicializa a SparkSession
    spark = SparkSession.builder \
        .appName("DataSusPysparkNativo") \
        .config("spark.sql.shuffle.partitions", "5") \
        .getOrCreate()
    
    print("⚡ SparkSession inicializada !")

    # 2. Baixa o arquivo CSV público usando a biblioteca nativa do Python
    url_dados = "https://githubusercontent.com"
    arquivo_local = "gastos_sus.csv"
    
    if not os.path.exists(arquivo_local):
        print(f"📥 Baixando dados públicos diretamente da URL...")
        urllib.request.urlretrieve(url_dados, arquivo_local)
        print("✅ Download concluído!")
    else:
        print("🔄 Arquivo local já existente, pulando download.")

    # 3. Define o Schema explicitamente (Prática ALTAMENTE valorizada por recrutadores Sênior)
    # Isso evita que o Spark precise ler o arquivo duas vezes para inferir o schema (inferSchema=True)
    schema_gastos = StructType([
        StructField("uf", StringType(), True),
        StructField("codigo_municipio", StringType(), True),
        StructField("municipio", StringType(), True),
        StructField("ano", StringType(), True),
        StructField("gasto_total", DoubleType(), True)
    ])

    # 4. Leitura do arquivo usando apenas recursos nativos do PySpark
    print("📖 Carregando o arquivo diretamente no PySpark DataFrame...")
    df_spark = spark.read \
        .format("csv") \
        .option("header", "true") \
        .option("sep", ",") \
        .schema(schema_gastos) \
        .load(arquivo_local)

    # 5. Transformação e Agregação de Dados
    # Vamos agrupar os gastos totais em saúde por Estado (UF)
    print("📊 Agrupando gastos por Unidade da Federação...")
    df_resultado = df_spark \
        .groupBy("uf") \
        .agg(round(sum("gasto_total"), 2).alias("Total_Investido_R$")) \
        .filter(col("uf").isNotNull()) \
        .orderBy(desc("Total_Investido_R$"))

    # 6. Exibe o resultado na tela (Ação do Spark)
    df_resultado.show(15, truncate=False)

    # Opcional: Remove o arquivo temporário do disco após a execução
    if os.path.exists(arquivo_local):
        os.remove(arquivo_local)
        
    return df_resultado

if __name__ == "__main__":
    processar_dados_spark()







