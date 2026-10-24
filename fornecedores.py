import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuração de estilo visual com base na skill 'chart-image'
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# 1. Leitura dos dados originais
caminho_csv = os.path.join("dados", "fornecedores.csv")
df = pd.read_csv(caminho_csv)

# 2. Critérios e pesos da Matriz de Decisão
pesos = {
    "preco_unitario": 0.30,
    "defeitos_pct": 0.30,
    "prazo_dias": 0.20,
    "suporte_nota": 0.20,
}

# 3. Normalização das notas em escala de 1 a 10 (Skill decision-matrix)
min_preco = df["preco_unitario"].min()
min_prazo = df["prazo_dias"].min()
min_defeitos = df["defeitos_pct"].min()
max_suporte = df["suporte_nota"].max()

df_scores = pd.DataFrame()
df_scores["fornecedor"] = df["fornecedor"]
df_scores["score_preco"] = 10 * (min_preco / df["preco_unitario"])
df_scores["score_prazo"] = 10 * (min_prazo / df["prazo_dias"])
df_scores["score_defeitos"] = 10 * (min_defeitos / df["defeitos_pct"])
df_scores["score_suporte"] = 10 * (df["suporte_nota"] / max_suporte)

# 4. Nota final ponderada
df_scores["nota_final"] = (
    df_scores["score_preco"] * pesos["preco_unitario"]
    + df_scores["score_prazo"] * pesos["prazo_dias"]
    + df_scores["score_defeitos"] * pesos["defeitos_pct"]
    + df_scores["score_suporte"] * pesos["suporte_nota"]
)

# Merge com os dados brutos para os novos gráficos
df_completo = pd.merge(df, df_scores, on="fornecedor")
df_ranking = df_completo.sort_values(by="nota_final", ascending=False).reset_index(drop=True)
df_ranking["ranking"] = df_ranking.index + 1
melhor = df_ranking.iloc[0]

print("============================================================")
print("MATRIZ DE DECISAO - RESULTADOS")
print("============================================================")
for _, row in df_ranking.iterrows():
    print(f" {int(row['ranking'])}º Lugar: {row['fornecedor']} - Nota Final: {row['nota_final']:.2f}")
print(f"\nMELHOR FORNECEDOR: {melhor['fornecedor']} (Nota: {melhor['nota_final']:.2f})")
print("============================================================")

os.makedirs("resultados", exist_ok=True)

# -------------------------------------------------------------
# GRÁFICO 1 (MELHORADO): analise_fornecedores.png
# Painel duplo com design refinado, contraste aprimorado e rótulos claros
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.patch.set_facecolor("#fafafa")

# Cores com destaque no vencedor
cores_ranking = ["#27ae60" if f == melhor["fornecedor"] else "#7f8c8d" for f in df_ranking["fornecedor"]]

# Subplot 1: Ranking em barras horizontais (ordem do 1º ao último)
df_invertido = df_ranking.sort_values(by="nota_final", ascending=True)
barras = ax1.barh(df_invertido["fornecedor"], df_invertido["nota_final"],
                  color=["#27ae60" if f == melhor["fornecedor"] else "#95a5a6" for f in df_invertido["fornecedor"]],
                  height=0.55, edgecolor="#2c3e50", linewidth=1)
ax1.set_facecolor("#ffffff")
ax1.set_title("Ranking Geral Ponderado (Decision Matrix)", fontsize=13, fontweight="bold", pad=12, color="#2c3e50")
ax1.set_xlabel("Nota Final (Escala 0 a 10)", fontsize=11, labelpad=8)
ax1.set_xlim(0, 11)
ax1.grid(axis="x", linestyle="--", alpha=0.5)

# Rótulos nas barras
for barra in barras:
    largura = barra.get_width()
    ax1.annotate(f" {largura:.2f} pts",
                 xy=(largura, barra.get_y() + barra.get_height() / 2),
                 xytext=(4, 0), textcoords="offset points",
                 ha="left", va="center", fontsize=11, fontweight="bold",
                 color="#27ae60" if largura == melhor["nota_final"] else "#2c3e50")

# Subplot 2: Desempenho comparativo detalhado por critério
df_plot = df_ranking.set_index("fornecedor")[["score_preco", "score_prazo", "score_defeitos", "score_suporte"]]
df_plot.columns = ["Preço (30%)", "Prazo (20%)", "Qualidade (30%)", "Suporte (20%)"]

paleta_criterios = ["#34495e", "#2980b9", "#e67e22", "#16a085"]
df_plot.plot(kind="bar", ax=ax2, color=paleta_criterios, width=0.75, edgecolor="#2c3e50", linewidth=0.8)
ax2.set_facecolor("#ffffff")
ax2.set_title("Desempenho por Critério Avaliado", fontsize=13, fontweight="bold", pad=12, color="#2c3e50")
ax2.set_xlabel("Fornecedor", fontsize=11, labelpad=8)
ax2.set_ylabel("Nota do Critério (1 a 10)", fontsize=11)
ax2.set_ylim(0, 11.5)
ax2.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
ax2.grid(axis="y", linestyle="--", alpha=0.5)
ax2.tick_params(axis="x", rotation=0)

fig.suptitle("Avaliação e Seleção de Fornecedores - Skill chart-image", fontsize=15, fontweight="bold", y=0.98, color="#1a252f")
fig.text(0.99, 0.01, "Fonte: dados/fornecedores.csv | Metodologia: Decision Matrix", ha="right", fontsize=9, color="#7f8c8d")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

caminho_grafico1 = os.path.join("resultados", "analise_fornecedores.png")
plt.savefig(caminho_grafico1, dpi=300)
plt.close()
print(f"Gráfico 1 (Melhorado) salvo em: {caminho_grafico1}")

# -------------------------------------------------------------
# GRÁFICO 2 (NOVO): grafico_radar_fornecedores.png
# Gráfico de Radar (Spider Chart) para comparação de perfil
# -------------------------------------------------------------
categorias = ["Preço (Custo)", "Prazo (Rapidez)", "Qualidade (Defeitos)", "Suporte Técnico"]
N = len(categorias)
angulos = [n / float(N) * 2 * np.pi for n in range(N)]
angulos += angulos[:1]

fig_radar = plt.figure(figsize=(8, 8))
fig_radar.patch.set_facecolor("#fafafa")
ax_radar = plt.subplot(111, polar=True)
ax_radar.set_facecolor("#ffffff")

# Ajuste dos eixos
plt.xticks(angulos[:-1], categorias, color="#2c3e50", size=11, fontweight="bold")
ax_radar.set_rlabel_position(30)
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#7f8c8d", size=9)
plt.ylim(0, 10.5)

cores_fornecedores = {
    "Delta": ("#27ae60", 2.5, 0.25),
    "Beta": ("#2980b9", 1.8, 0.15),
    "Alfa": ("#f39c12", 1.5, 0.10),
    "Gama": ("#e74c3c", 1.5, 0.10),
}

for _, r in df_ranking.iterrows():
    f_nome = r["fornecedor"]
    valores = [r["score_preco"], r["score_prazo"], r["score_defeitos"], r["score_suporte"]]
    valores += valores[:1]
    cor, lw, alpha = cores_fornecedores[f_nome]
    
    label_text = f"{f_nome} (Vencedor: {r['nota_final']:.2f})" if f_nome == melhor["fornecedor"] else f"{f_nome} ({r['nota_final']:.2f})"
    ax_radar.plot(angulos, valores, linewidth=lw, linestyle="solid", label=label_text, color=cor)
    ax_radar.fill(angulos, valores, color=cor, alpha=alpha)

plt.title("Perfil Multidimensional dos Fornecedores (Radar)\n(Escala 1 a 10, onde 10 é excelente)",
          size=13, fontweight="bold", y=1.08, color="#2c3e50")
plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=10, framealpha=0.9)
fig_radar.text(0.99, 0.02, "Fonte: dados/fornecedores.csv", ha="right", fontsize=9, color="#7f8c8d")

caminho_grafico2 = os.path.join("resultados", "grafico_radar_fornecedores.png")
plt.savefig(caminho_grafico2, dpi=300, bbox_inches="tight")
plt.close()
print(f"Gráfico 2 (Radar) salvo em: {caminho_grafico2}")

# -------------------------------------------------------------
# GRÁFICO 3 (NOVO): grafico_tradeoff_custo_qualidade.png
# Dispersão Custo vs. Qualidade com indicação de Prazo e Suporte
# -------------------------------------------------------------
fig_tradeoff, ax_t = plt.subplots(figsize=(9, 6))
fig_tradeoff.patch.set_facecolor("#fafafa")
ax_t.set_facecolor("#ffffff")

# Scatter com tamanho baseado na nota de suporte e cor indicando vencedor
for _, r in df_ranking.iterrows():
    is_melhor = r["fornecedor"] == melhor["fornecedor"]
    cor = "#27ae60" if is_melhor else "#3498db"
    tamanho = (r["suporte_nota"] ** 2.2) * 3
    
    ax_t.scatter(r["preco_unitario"], r["defeitos_pct"], s=tamanho, color=cor,
                 alpha=0.85, edgecolors="#2c3e50", linewidth=1.5, zorder=5)
    
    # Rótulo de cada ponto
    offset_y = 0.2 if r["fornecedor"] != "Delta" else -0.3
    ax_t.annotate(
        f"{r['fornecedor']}\nPreço: R${r['preco_unitario']:.0f} | Defeitos: {r['defeitos_pct']}%\nPrazo: {r['prazo_dias']}d | Suporte: {r['suporte_nota']}",
        xy=(r["preco_unitario"], r["defeitos_pct"]),
        xytext=(0, 20 if offset_y > 0 else -35),
        textcoords="offset points",
        ha="center", fontsize=9.5, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor=cor, alpha=0.9),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color=cor, lw=1.2),
        zorder=6
    )

ax_t.set_title("Análise de Trade-off: Preço Unitário vs. Taxa de Defeitos", fontsize=13, fontweight="bold", pad=12, color="#2c3e50")
ax_t.set_xlabel("Preço Unitário (R$) — (Menor é melhor)", fontsize=11, labelpad=8)
ax_t.set_ylabel("Taxa de Defeitos (%) — (Menor é melhor)", fontsize=11, labelpad=8)
ax_t.set_xlim(80, 120)
ax_t.set_ylim(-0.5, 5.0)
ax_t.grid(True, linestyle="--", alpha=0.5)

# Destaque de quadrante favorável
ax_t.axvline(x=100, color="#bdc3c7", linestyle=":", linewidth=1)
ax_t.axhline(y=2.0, color="#bdc3c7", linestyle=":", linewidth=1)

fig_tradeoff.text(0.99, 0.01, "Tamanho dos círculos proporcional à Nota de Suporte | Fonte: dados/fornecedores.csv", ha="right", fontsize=9, color="#7f8c8d")
plt.tight_layout(rect=[0, 0.03, 1, 0.96])

caminho_grafico3 = os.path.join("resultados", "grafico_tradeoff_custo_qualidade.png")
plt.savefig(caminho_grafico3, dpi=300)
plt.close()
print(f"Gráfico 3 (Trade-off) salvo em: {caminho_grafico3}")

# -------------------------------------------------------------
# Atualização do Relatório Markdown incluindo todos os gráficos
# -------------------------------------------------------------
caminho_relatorio = os.path.join("resultados", "relatorio_fornecedores.md")
with open(caminho_relatorio, "w", encoding="utf-8") as f:
    f.write("# Relatório de Avaliação de Fornecedores (Decision Matrix & Chart Image)\n\n")
    f.write("Este relatório foi gerado seguindo as diretrizes das skills **decision-matrix** e **chart-image**.\n\n")
    
    f.write("## 1. Dados Originais dos Fornecedores\n\n")
    f.write("| Fornecedor | Preço Unitário (R$) | Prazo (Dias) | Defeitos (%) | Nota de Suporte |\n")
    f.write("|---|---|---|---|---|\n")
    for _, r in df.iterrows():
        f.write(f"| {r['fornecedor']} | {r['preco_unitario']} | {r['prazo_dias']} | {r['defeitos_pct']}% | {r['suporte_nota']} |\n")
    
    f.write("\n## 2. Critérios e Pesos Utilizados\n\n")
    f.write("- **Preço Unitário (30%):** Menor valor é melhor.\n")
    f.write("- **Qualidade / Defeitos (30%):** Menor taxa de defeitos é melhor.\n")
    f.write("- **Prazo de Entrega (20%):** Menor tempo é melhor.\n")
    f.write("- **Suporte Técnico (20%):** Maior nota é melhor.\n\n")
    
    f.write("## 3. Notas Normalizadas (Escala de 1 a 10)\n\n")
    f.write("| Fornecedor | Score Preço | Score Prazo | Score Defeitos | Score Suporte | **Nota Final Ponderada** | **Posição** |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for _, r in df_ranking.iterrows():
        f.write(f"| **{r['fornecedor']}** | {r['score_preco']:.2f} | {r['score_prazo']:.2f} | {r['score_defeitos']:.2f} | {r['score_suporte']:.2f} | **{r['nota_final']:.2f}** | {int(r['ranking'])}º |\n")
    
    f.write(f"\n## 4. Conclusão e Recomendação\n\n")
    f.write(f"**Fornecedor Recomendado:** **{melhor['fornecedor']}** com nota ponderada de **{melhor['nota_final']:.2f}**.\n\n")
    f.write(f"- **Pontos Fortes:** Nota 10 em agilidade (4 dias), qualidade (0.5% defeitos) e suporte técnico (9.5).\n")
    f.write(f"- **Trade-off:** Preço ligeiramente superior (R$ 110), amplamente compensado pela confiabilidade operacional.\n\n")
    
    f.write("## 5. Análises Visuais de Apoio à Decisão\n\n")
    f.write("### Gráfico 1: Ranking e Comparativo por Critério\n")
    f.write("![Ranking e Critérios](analise_fornecedores.png)\n\n")
    f.write("### Gráfico 2: Perfil Multidimensional (Radar)\n")
    f.write("![Gráfico Radar](grafico_radar_fornecedores.png)\n\n")
    f.write("### Gráfico 3: Trade-off Custo vs. Qualidade\n")
    f.write("![Trade-off Custo x Qualidade](grafico_tradeoff_custo_qualidade.png)\n")

print(f"Relatório atualizado em: {caminho_relatorio}")
