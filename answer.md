# Resolução – Questão 3

---

## 3.1 Conjuntos que compõem o grafo

### Definições

**Conjuntos de Vértices**

- **V<sub>carros</sub>**: 24 veículos (um vértice por modelo).  
- **V<sub>peças</sub>**: 22 peças (ordem fixa; define a posição do bit no *label*).

**Arestas do Bipartido**  
- E ⊂ V<sub>carros</sub> × V<sub>peças</sub>  
  - Há uma aresta (c, p) se o carro **c** utiliza a peça **p** (total de 94 relações).

---

### Construção do Grafo

1. Criamos a **matriz de incidência** carro × peça (0/1), respeitando a ordem de `V_peças`.
2. Projetamos para o grafo veículo–veículo G' = (V<sub>carros</sub>, E'):
   - Para cada par (u, v), fazemos o **AND** entre as linhas (vetores 0/1) de *u* e *v*.
   - Se existe ao menos uma peça comum ⇒ adicionamos (u, v) ∈ E'.

   **Atributos da aresta:**
   - `weight`: número de peças em comum (soma do AND).
   - `label`: string binária de **22 bits** indicando quais peças são compartilhadas.
   - `pecas_compartilhadas`: lista nominal das peças comuns.

---

### Resultado Estrutural

- |V| = 24 (veículos)  
- |E'| = 276 conexões ⇒ C(24, 2) → grafo projetado **completo**.

> **Observação:** todos os veículos possuem **Sistema ABS Bosch**, garantindo ao menos uma peça em comum para qualquer par. Enquanto que, a peça “**Chassi Monobloco**” está presente em `V_peças`, mas **não é usada** por nenhum carro (coluna de zeros).

---

## 3.2 Vértices de Maior e Menor Grau

Como G' é **completo**, o **grau não ponderado** de todos os vértices é **23**.  
Para avaliar relevância, analisamos o **grau ponderado** (soma dos `weight` das arestas incidentes).

### Top 5 – Maior grau ponderado (mais peças compartilhadas)

| Posição | Veículo               | Grau ponderado |
|----------|----------------------|----------------|
| 1        | Audi Q7 4L           | 42             |
| 2        | Porsche Cayenne      | 42             |
| 3        | VW Touareg 7L        | 42             |
| 4        | Audi TT Mk2          | 40             |
| 5        | BMW 3 Series (F30)   | 39             |

### Bottom 5 – Menor grau ponderado

| Posição | Veículo             | Grau ponderado |
|----------|--------------------|----------------|
| 1        | Renault Clio V     | 24             |
| 2        | Nissan Micra K14   | 24             |
| 3        | VW Polo Mk5        | 26             |
| 4        | Renault Clio IV    | 27             |
| 5        | Renault Captur     | 27             |

> **Análise:** veículos com maior grau ponderado pertencem a plataformas amplamente compartilhadas, como PL71 (Q7/Touareg/Cayenne), MQB (Golf/A3) e Small Wide 4×4 (Renegade/Compass/Toro), indicando **maior risco de efeito dominó** em eventuais falhas de abastecimento.

---

## 3.3 Subconjuntos e subgrafos

Um subconjunto S ⊆ V é subgrafo induzido de G' se todas as arestas entre pares de S presentes em G' também estão no subgrafo.

### **Subgrafo 1 — VW–Audi (Plataforma PQ35)**

**Vértices:** {VW Golf Mk6, Audi A3 8P, VW Polo Mk5, Audi TT Mk2}  
**|V| = 4**, **|E| = 6**

**Arestas (peso e peças compartilhadas):**

| Conexão | Peso (w) | Peças compartilhadas |
|----------|-----------|----------------------|
| Golf Mk6 ↔ A3 8P | 4 | DSG DQ250, PQ35, ABS Bosch, MIB |
| Golf Mk6 ↔ Polo Mk5 | 1 | ABS Bosch |
| Golf Mk6 ↔ TT Mk2 | 4 | EA888 2.0T, DSG DQ250, PQ35, ABS Bosch |
| A3 8P ↔ Polo Mk5 | 2 | EA111 1.6, ABS Bosch |
| A3 8P ↔ TT Mk2 | 3 | DSG DQ250, PQ35, ABS Bosch |
| TT Mk2 ↔ Polo Mk5 | 1 | ABS Bosch |

> **Análise:** este subgrafo representa o núcleo histórico da **plataforma PQ35** do Grupo VW.  
> A presença consistente de **ABS**, **transmissão DSG** e **arquitetura PQ35** evidencia alto grau de padronização entre hatchbacks e esportivos compactos da marca.

---

### Subconjuntos adicionais

| Grupo | Veículos | Peso (w) | Peças compartilhadas |
|--------|-----------|-----------|-----------------------|
| **PL71 (SUVs VW Group Premium)** | Audi Q7 4L, VW Touareg 7L, Porsche Cayenne | 5 | PL71, Suspensão Multilink, ABS, Turbocompressor KKK, Motor VR6 3.6 |
| **MQB (VAG Compactos)** | VW Golf Mk7, Audi A3 8V | 5 | MQB, EA888, DSG DQ250, ABS, MIB |
| **B-Platform (Renault–Nissan)** | Renault Clio IV, Nissan Micra K13, Renault Captur | 3 | Plataforma B, HR16DE, ABS |
| **CMF (Common Module Family)** | Clio V–Micra K14 (w=2), Qashqai J11–Kadjar (w=3) | 2–3 | CMF-B/CD, Multilink, ABS |
| **Small Wide 4×4 (Stellantis)** | Jeep Renegade, Compass, Fiat Toro | 4 | Small Wide 4×4, Tigershark 2.4, Aisin 6F24, ABS |
| **Premium DE (BMW/Mercedes)** | BMW X3, Mercedes C-Class | ≥3 | Multilink, ABS, KKK, (BMW: N20 2.0T) |

> Todos os subconjuntos acima **formam subgrafos induzidos** de G'.
