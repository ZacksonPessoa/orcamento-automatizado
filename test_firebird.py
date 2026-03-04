from worker.firebird_db import query_fc03000, query_fc03000_por_descricao

print(query_fc03000(3))  # deve imprimir 3 registros
print(query_fc03000_por_descricao("DIPIRONA", 5))  # exemplo