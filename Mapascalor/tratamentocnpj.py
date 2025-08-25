import pandas as pd

# Configurações
caminho_entrada = r"C:\Users\USER\Downloads\chato.txt"
caminho_saida = r"C:\Users\USER\Downloads\sp_todos.xlsx"

try:
    # Ler o arquivo em chunks para economizar memória
    chunks = pd.read_csv(
        caminho_entrada,
        sep=";",
        encoding="latin1",
        header=None,
        dtype={11: str},  # Especificar que a coluna UF é string
        chunksize=100000
    )
    
    lista_sp = []
    
    for i, chunk in enumerate(chunks):
        # Verificar se a coluna 9 (UF) existe
        if len(chunk.columns) > 9:
            # Filtrar apenas registros de SP (coluna 9)
            chunk['UF'] = chunk[11].astype(str).str.strip().str.upper()
            chunk_sp = chunk[chunk['UF'] == 'SP']
            lista_sp.append(chunk_sp)
            print(f"Processado chunk {i+1}: {len(chunk_sp)} registros de SP")
        else:
            print(f"Chunk {i+1} não contém coluna UF (posição 9)")
    
    # Consolidar todos os registros de SP
    if lista_sp:
        df_sp = pd.concat(lista_sp)
        
        # Salvar em Excel
        df_sp.to_csv(caminho_saida, index=False)
        print(f"\nArquivo salvo com {len(df_sp)} registros de SP em {caminho_saida}")
        
        # Mostrar resumo
        print("\nResumo:")
        print(f"Total de registros: {len(df_sp)}")
        if len(df_sp.columns) > 20:  # Se tiver coluna de município
            print("\nTop 10 municípios:")
            print(df_sp[20].value_counts().head(10))
    else:
        print("Nenhum registro de SP encontrado.")

except Exception as e:
    print(f"Erro: {str(e)}")