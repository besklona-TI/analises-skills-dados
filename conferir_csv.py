import os
import pandas as pd

# Caminho do arquivo a ser auditado
caminho_csv = os.path.join("dados", "fornecedores_erro.csv")

# Leitura considerando células em branco/espaços como nulas (conforme a skill conferir-csv)
df = pd.read_csv(caminho_csv, na_values=["", " ", "NA", "null", "NaN"])

# 1. Métricas gerais calculadas com código
linhas, colunas = df.shape
duplicadas = int(df.duplicated().sum())

# 2. Auditoria por coluna
info_colunas = []
for col in df.columns:
    tipo = str(df[col].dtype)
    ausentes = int(df[col].isna().sum())
    pct_ausente = (ausentes / linhas) * 100
    info_colunas.append({
        "coluna": col,
        "tipo": tipo,
        "ausentes": ausentes,
        "pct_ausente": pct_ausente,
    })

# 3. Detalhamento de problemas específicos
problemas = []
if df["preco_unitario"].isna().any():
    forn_sem_preco = df[df["preco_unitario"].isna()]["fornecedor"].tolist()
    problemas.append(f"Preço unitário ausente para o(s) fornecedor(es): {', '.join(forn_sem_preco)}")

if df["suporte_nota"].isna().any():
    forn_sem_suporte = df[df["suporte_nota"].isna()]["fornecedor"].tolist()
    problemas.append(f"Nota de suporte ausente para o(s) fornecedor(es): {', '.join(forn_sem_suporte)}")

# 4. Exibição no console
print("=" * 60)
print("AUDITORIA DE QUALIDADE DE DADOS (conferir-csv)")
print("=" * 60)
print(f"Arquivo analisado: {caminho_csv}")
print(f"Total de linhas: {linhas} | Total de colunas: {colunas}")
print(f"Linhas duplicadas: {duplicadas}\n")

print("Resumo por coluna:")
for item in info_colunas:
    print(f" - {item['coluna']}: tipo {item['tipo']} | Ausentes: {item['ausentes']} ({item['pct_ausente']:.1f}%)")

print("\nProblemas identificados:")
if problemas:
    for prob in problemas:
        print(f" [!] {prob}")
else:
    print(" Nenhum problema encontrado.")
print("=" * 60)

# 5. Salvar resumo em resultados/qualidade.md (Regra 8 da skill)
os.makedirs("resultados", exist_ok=True)
caminho_relatorio = os.path.join("resultados", "qualidade.md")
with open(caminho_relatorio, "w", encoding="utf-8") as f:
    f.write("# Relatório de Qualidade de Dados (conferir-csv)\n\n")
    f.write(f"- **Arquivo verificado:** `{caminho_csv}`\n")
    f.write(f"- **Finalidade:** Seleção e avaliação de fornecedores (Decision Matrix)\n")
    f.write(f"- **Total de registros (linhas):** {linhas}\n")
    f.write(f"- **Total de atributos (colunas):** {colunas}\n")
    f.write(f"- **Linhas duplicadas:** {duplicadas}\n\n")
    
    f.write("## 1. Estrutura das Colunas e Valores Ausentes\n\n")
    f.write("| Coluna | Tipo Detectado | Valores Ausentes | % Ausente |\n")
    f.write("|---|---|---|---|\n")
    for item in info_colunas:
        f.write(f"| `{item['coluna']}` | {item['tipo']} | {item['ausentes']} | {item['pct_ausente']:.1f}% |\n")
        
    f.write("\n## 2. Problemas Encontrados e Evidências\n\n")
    for prob in problemas:
        f.write(f"- **Inconsistência:** {prob}\n")
        
    f.write("\n## 3. Tratamentos Propostos\n\n")
    f.write("1. **Preservar o arquivo original:** Nunca modificar diretamente `dados/fornecedores_erro.csv`.\n")
    f.write("2. **Regras para dados ausentes:**\n")
    f.write("   - Para o fornecedor **Delta**: Obter a cotação oficial do `preco_unitario` antes de rodar a matriz de decisão.\n")
    f.write("   - Para o fornecedor **Beta**: Confirmar a `suporte_nota` com a equipe de compras/suporte.\n")
    f.write("3. **Impacto:** A falta dessas informações impede o cálculo comparativo justo, pois deixaria o Delta sem nota de custo e o Beta sem nota de suporte.\n")

print(f"\nResumo de qualidade salvo em: {caminho_relatorio}")

