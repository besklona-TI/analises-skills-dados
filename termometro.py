import os
import matplotlib.pyplot as plt

# 1. Pontos conhecidos (calibração do sensor)
# Ponto 1: 0 °C -> 4 mA
# Ponto 2: 100 °C -> 20 mA
x1, y1 = 0, 4
x2, y2 = 100, 20

# 2. Equação da reta: y = a * x + b
# Coeficiente angular (a): variação de corrente dividida pela variação de temperatura
a = (y2 - y1) / (x2 - x1)

# Coeficiente linear (b): valor da corrente quando a temperatura é 0 °C
b = y1 - a * x1

# 3. Cálculo para x = 50 graus
x_alvo = 50
y_alvo = a * x_alvo + b

# Exibição dos resultados do cálculo
print(f"Coeficiente a: {a}")
print(f"Coeficiente b: {b}")
print(f"Equação da reta: Corrente = {a} * Temperatura + {b}")
print(f"Para Temperatura = {x_alvo} °C, a Corrente é: {y_alvo:.2f} mA")

# 4. Classificação da temperatura
# - Baixa: até 30 graus
# - Média: até 60 graus
# - Alta: acima de 60 graus
if x_alvo <= 30:
    classificacao = "Baixa"
elif x_alvo <= 60:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura ({x_alvo} °C): {classificacao}")

# 5. Avisos caso os valores estejam fora dos limites operacionais
if x_alvo < 0 or x_alvo > 100:
    print(f"⚠️ AVISO: A temperatura ({x_alvo} °C) está fora da faixa permitida (0 a 100 °C)!")

if y_alvo < 4 or y_alvo > 20:
    print(f"⚠️ AVISO: A corrente ({y_alvo:.2f} mA) está fora da faixa permitida (4 a 20 mA)!")

# 6. Geração do gráfico com Matplotlib
temperaturas = [0, 25, 50, 75, 100]
correntes = [a * t + b for t in temperaturas]

plt.figure(figsize=(8, 5))
plt.plot(temperaturas, correntes, label="Curva de Resposta (4 a 20 mA)", color="blue", linewidth=2)
# Destaque do ponto medido em x = 50 °C
plt.plot(x_alvo, y_alvo, marker="o", markersize=8, color="red", label=f"Ponto Medido ({x_alvo} °C, {y_alvo:.1f} mA)")

# Configuração dos eixos e legendas
plt.title("Transmissor de Temperatura: Temperatura vs Corrente Elétrica")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()

# Garantir que a pasta resultados/ existe e salvar o gráfico
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico, dpi=300, bbox_inches="tight")
print(f"Gráfico salvo com sucesso em: {caminho_grafico}")

# Exibe o gráfico sem travar a execução
plt.show(block=False)
