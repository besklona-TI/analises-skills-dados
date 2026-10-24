# Relatório de Qualidade de Dados (conferir-csv)

- **Arquivo verificado:** `dados\fornecedores_erro.csv`
- **Finalidade:** Seleção e avaliação de fornecedores (Decision Matrix)
- **Total de registros (linhas):** 4
- **Total de atributos (colunas):** 5
- **Linhas duplicadas:** 0

## 1. Estrutura das Colunas e Valores Ausentes

| Coluna | Tipo Detectado | Valores Ausentes | % Ausente |
|---|---|---|---|
| `fornecedor` | str | 0 | 0.0% |
| `preco_unitario` | float64 | 1 | 25.0% |
| `prazo_dias` | int64 | 0 | 0.0% |
| `defeitos_pct` | float64 | 0 | 0.0% |
| `suporte_nota` | float64 | 1 | 25.0% |

## 2. Problemas Encontrados e Evidências

- **Inconsistência:** Preço unitário ausente para o(s) fornecedor(es): Delta
- **Inconsistência:** Nota de suporte ausente para o(s) fornecedor(es): Beta

## 3. Tratamentos Propostos

1. **Preservar o arquivo original:** Nunca modificar diretamente `dados/fornecedores_erro.csv`.
2. **Regras para dados ausentes:**
   - Para o fornecedor **Delta**: Obter a cotação oficial do `preco_unitario` antes de rodar a matriz de decisão.
   - Para o fornecedor **Beta**: Confirmar a `suporte_nota` com a equipe de compras/suporte.
3. **Impacto:** A falta dessas informações impede o cálculo comparativo justo, pois deixaria o Delta sem nota de custo e o Beta sem nota de suporte.
