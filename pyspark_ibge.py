import json
import os
import sys
import urllib.request

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
from pyspark.sql.types import DoubleType, StringType, StructField, StructType


URL_IBGE = (
    "https://apisidra.ibge.gov.br/values/t/6579/n3/all/"
    "v/9324/p/2024"
)


def buscar_dados_ibge():
    python_exe = sys.executable
    os.environ["PYSPARK_PYTHON"] = python_exe
    os.environ["PYSPARK_DRIVER_PYTHON"] = python_exe

    spark = (
        SparkSession.builder
        .appName("PopulacaoIbgePySpark")
        .config("spark.sql.shuffle.partitions", "5")
        .config("spark.pyspark.python", python_exe)
        .config("spark.pyspark.driver.python", python_exe)
        .getOrCreate()
    )

    try:
        print("SparkSession inicializada!")
        print("Consultando dados de população na API do IBGE...")

        requisicao = urllib.request.Request(
            URL_IBGE,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            dados_api = json.load(resposta)

        registros = [
            {
                "codigo_uf": registro["D1C"],
                "nome_uf": registro["D1N"],
                "populacao": registro["V"],
            }
            for registro in dados_api[1:]
        ]

        if not registros:
            raise RuntimeError("A API do IBGE não retornou registros.")

        schema_ibge = StructType([
            StructField("codigo_uf", StringType(), False),
            StructField("nome_uf", StringType(), False),
            StructField("populacao", StringType(), False),
        ])

        df_ibge = (
            spark.createDataFrame(registros, schema=schema_ibge)
            .withColumn("populacao", col("populacao").cast(DoubleType()))
        )

        print(f"Registros carregados: {df_ibge.count()}")
        print("População por unidade federativa:")

        df_por_uf = (
            df_ibge
            .groupBy("codigo_uf", "nome_uf")
            .agg(spark_sum("populacao").alias("populacao_total"))
            .orderBy("nome_uf")
        )

        df_por_uf.show(30, truncate=False)
        return df_por_uf
    finally:
        spark.stop()
        print("SparkSession encerrada.")


if __name__ == "__main__":
    buscar_dados_ibge()
