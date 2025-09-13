from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws, monotonically_increasing_id, col, lit

# Initialisation Spark
spark = SparkSession.builder \
    .appName("Graph Fraud Preprocessing") \
    .getOrCreate()

# Chargement des fichiers CSV
transaction_df = spark.read.csv("train_transaction.csv", header=True, inferSchema=True)
identity_df = spark.read.csv("train_identity.csv", header=True, inferSchema=True)

# Join sur TransactionID
df = transaction_df.join(identity_df, on="TransactionID", how="left")

# Colonnes simples à traiter
relations = {
    "card1": "relation_card1_edgelist",
    "card2": "relation_card2_edgelist",
    "card3": "relation_card3_edgelist",
    "card4": "relation_card4_edgelist",
    "card5": "relation_card5_edgelist",
    "card6": "relation_card6_edgelist",
    "addr1": "relation_addr1_edgelist",
    "addr2": "relation_addr2_edgelist",
    "DeviceInfo": "relation_DeviceInfo_edgelist",
    "DeviceType": "relation_DeviceType_edgelist",
    "P_emaildomain": "relation_P_emaildomain_edgelist",
    "R_emaildomain": "relation_R_emaildomain_edgelist"
}

# Fonction pour créer les edge lists
def generate_edgelist(df, col_name, folder):
    edges = df.select("TransactionID", col_name) \
              .dropna() \
              .withColumn(":from", concat_ws("-", lit("t"), col("TransactionID"))) \
              .withColumn(":to", concat_ws("-", lit(col_name), col(col_name).cast("string"))) \
              .withColumn(":id", concat_ws("-", lit("t"), col("TransactionID"), lit(col_name), col(col_name).cast("string"))) \
              .select(":id", ":from", ":to") \
              .dropDuplicates()
    
    edges.write.csv(f"graph/{folder}", header=True, mode="overwrite")

# Génération des relations simples
for col_name, folder in relations.items():
    generate_edgelist(df, col_name, folder)

# Relations dynamiques pour les id_XX
id_columns = [col for col in df.columns if col.startswith("id_")]

for col_name in id_columns:
    folder = f"relation_{col_name}_edgelist"
    generate_edgelist(df, col_name, folder)

spark.stop()
