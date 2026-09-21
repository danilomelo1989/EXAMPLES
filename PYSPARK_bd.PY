import os
import sys
import urllib.request
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import col, sum, desc, round, concat, lit


def processar_dados_spark():

    python_exe = sys.executable 
    os.environ["PYSPARK_PYTHON"] = python_exe
    os.environ["PYSPARK_DRIVER_PYTHON"] = python_exe

    # Inicializa a SparkSession
    spark = SparkSession.builder \
        .appName("DataSusPysparkNativo") \
        .config("spark.sql.shuffle.partitions", "5") \
        .config("spark.pyspark.python", python_exe) \
        .config("spark.pyspark.driver.python", python_exe) \
        .getOrCreate()
    
    print("SparkSession inicializada !")

    # Tenta baixar o arquivo CSV público; se falhar, gera um CSV local estável
    url_dados = "https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv"
    arquivo_local = os.path.join(os.getcwd(), "2014_usa_states.csv")
    
    if not os.path.exists(arquivo_local):
        print("Tentando baixar dados públicos diretamente da URL...")
        try:
            urllib.request.urlretrieve(url_dados, arquivo_local)
            print("Download concluído!")
        except Exception as exc:
            print(f"Não foi possível baixar a URL pública ({exc}).")
    else:
        print("Arquivo local já existente, pulando download.")

    # Define o Schema explicitamente conforme o cabeçalho do CSV
    schema_gastos = StructType([
        StructField("Rank", IntegerType(), True),
        StructField("State", StringType(), True),
        StructField("Postal", StringType(), True),
        StructField("Population", DoubleType(), True)
    ])

    # Leitura do arquivo usando apenas recursos nativos do PySpark
    print("Carregando o arquivo diretamente no PySpark DataFrame...")
    df_spark = spark.read \
        .format("csv") \
        .option("header", "true") \
        .option("sep", ",") \
        .schema(schema_gastos) \
        .load(arquivo_local)

    # Transformação e Agregação de Dados
    print("Agrupando população pela primeira letra do Estado...")

    letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    df_letras = spark.createDataFrame([(letra,) for letra in letras], ["Primeira_Letra"])

    df_agrupado = df_spark \
        .withColumn("Primeira_Letra", col("State").substr(1, 1)) \
        .groupBy("Primeira_Letra") \
        .agg(sum("Population").alias("Total_Populacao_Por_Letra"))

    total_us = df_spark.agg(sum("Population").alias("Total_Populacao_US")).collect()[0]["Total_Populacao_US"]

    df_resultado = df_letras \
        .join(df_agrupado, on="Primeira_Letra", how="left") \
        .na.fill({"Total_Populacao_Por_Letra": 0}) \
        .withColumn("Total_Populacao_Por_Letra", col("Total_Populacao_Por_Letra").cast("decimal(18,2)")) \
        .withColumn(
            "Percentual_Populacao",
            (col("Total_Populacao_Por_Letra") / total_us * 100).cast("decimal(10,2)")
        ) \
        .withColumn(
            "Percentual_Populacao",
            concat(col("Percentual_Populacao").cast("string"), lit("%"))
        ) \
        .orderBy("Primeira_Letra")

    # Exibe o resultado na tela (Ação do Spark)
    df_resultado.show(26, truncate=False)

    print(f"\nPopulação total dos EUA: {total_us:,.2f}")

    # Opcional: Remove o arquivo temporário do disco após a execução
    if os.path.exists(arquivo_local):
        os.remove(arquivo_local)
        
    return df_resultado

if __name__ == "__main__":
    processar_dados_spark()







