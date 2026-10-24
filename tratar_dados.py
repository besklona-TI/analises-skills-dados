import os
import pandas as pd

# 1. Leitura da base original (respeitando a regra de nunca alterar dados/)
caminho_entrada = os.path.join("dados", "fornecedores_erro.csv")
df_original = pd.read_csv(caminho_entrada, na_values=["", " ", "NA", "null", "NaN"])

# Cópia para aplicar o preenchimento
df_tratado = df_original.copy()

print("=" * 60)
print("TRATAMENTO DE DADOS - PREENCHIMENTO PELA MEDIA DOS ANTERIORES")
print("=" * 60)

# 2. Preenchimento pela média dos valores anteriores (linhas acima)
valores_preenchidos = {}
for col in ["preco_unitario", "suporte_nota"]:
    for i in range(len(df_tratado)):
        if pd.isna(df_tratado.loc[i, col]):
            # Pega os valores válidos das linhas anteriores na mesma coluna
            anteriores = df_original.loc[:i-1, col].dropna()
            media_anteriores = anteriores.mean()
            df_tratado.loc[i, col] = round(media_anteriores, 2)
            fornecedor = df_tratado.loc[i, "fornecedor"]
            valores_preenchidos[f"{fornecedor} ({col})"] = {
                "valores_anteriores": anteriores.tolist(),
                "media_calculada": round(media_anteriores, 2)
            }

# 3. Exibição dos cálculos no terminal
for item, info in valores_preenchidos.items():
    print(f"Campo: {item}")
    print(f" -> Valores anteriores considerados: {info['valores_anteriores']}")
    print(f" -> Media aplicada: {info['media_calculada']}\n")

print("Tabela Final Tratada:")
print(df_tratado.to_string(index=False))
print("=" * 60)

# 4. Gravação da nova base tratada em resultados/ (preservando dados/)
os.makedirs("resultados", exist_ok=True)
caminho_saida = os.path.join("resultados", "fornecedores_tratado.csv")
df_tratado.to_csv(caminho_saida, index=False)
print(f"Base tratada salva com sucesso em: {caminho_saida}")

# 5. Atualização do relatório de qualidade com o histórico do tratamento
caminho_relatorio = os.path.join("resultados", "qualidade.md")
with open(caminho_relatorio, "a", encoding="utf-8") as f:
    f.write("\n## 4. Tratamento Aplicado (Média dos Anteriores)\n\n")
    f.write(f"Arquivo gerado: `resultados/fornecedores_tratado.csv`\n\n")
    f.write("| Fornecedor | Campo Tratado | Valores Anteriores Considerados | Média Inserida |\n")
    f.write("|---|---|---|---|\n")
    for item, info in valores_preenchidos.items():
        forn = item.split()[0]
        campo = item.split("(")[1].replace(")", "")
        f.write(f"| **{forn}** | `{campo}` | {info['valores_anteriores']} | **{info['media_calculada']}** |\n")
    f.write("\n> [!NOTE]\n")
    f.write("> O arquivo original `dados/fornecedores_erro.csv` foi mantido intacto conforme as regras do projeto.\n")

print(f"Relatório atualizado em: {caminho_relatorio}")
