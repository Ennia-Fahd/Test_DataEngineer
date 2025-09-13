# Challenge 1: Fraud Detection Graph 

This project transforms transaction and identity data into a **property graph** structure using PySpark, aimed at supporting fraud detection tasks.

---

## 📁 Structure

- `graph_preprocessing.py`: Main PySpark script to convert raw tabular data into edge list format suitable for graph processing.
- `graph/`: Output folder containing all generated edge list files, one folder per relationship.

---

## ⚙️ Requirements

You need the following installed:

- Python 3.x
- Java 8 or 11 (required by Spark)
- Apache Spark (standalone or in your environment)
- PySpark

### Install PySpark and Java (if using pip):
```bash
pip install pyspark
```

Make sure Java is installed:
```bash
java -version
```

If Java is not installed, you can install it on Ubuntu/Debian with:
```bash
sudo apt update
sudo apt install openjdk-11-jdk
```

### Download and configure Apache Spark:
Go to https://spark.apache.org/downloads.html and download Spark (version 3.0 or higher, pre-built for Hadoop). Then:

```bash
tar -xzf spark-3.5.0-bin-hadoop3.tgz
export SPARK_HOME=~/spark-3.5.0-bin-hadoop3
export PATH=$SPARK_HOME/bin:$PATH
```

---

## 🚀 Run the project

### 1. Place input files
Download and place the following files in the root directory of the project:
- `train_transaction.csv`
- `train_identity.csv`

### 2. Run preprocessing
Use the following command to run the transformation and generate graph edge lists:

```bash
spark-submit graph_preprocessing.py
```

This will:
- Join the two datasets on `TransactionID`
- Create one folder per relationship with edge list CSVs inside

---


## 👨‍💻 Author

Developed for the **Helkinz Data Engineering Take-Home Challenge**.

---
