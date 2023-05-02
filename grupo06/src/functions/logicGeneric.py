import os
import csv
from config import *;

def importador_csv(dataset_name):
    """procedimiento que abre el archivo csv pedido y devuelve una el encabezado y una lista con su contenido"""
    
    dataset_csv = open(os.path.join(PROCESSED_PATH, dataset_name), encoding = 'utf8')
    reader_dataset = csv.reader(dataset_csv, delimiter = ',')
    header, reader = list(next(reader_dataset)), list(reader_dataset)
    dataset_csv.close()
    return header, reader