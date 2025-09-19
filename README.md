# Sprint 3 — IoT: Reconhecimento Facial com dlib/OpenCV

> Repositório analisado: `Lucas-Umada/Sprint3_IoT` (contém `teste.py` e três modelos `.dat` do dlib).

## 📌 Visão geral

Este projeto demonstra um pipeline básico de **detecção, alinhamento e reconhecimento facial** em Python usando **dlib** e **OpenCV**. O repositório inclui os pesos pré‑treinados do dlib (shape predictors e modelo de embeddings) e um script principal (`teste.py`) para rodar o sistema localmente.

### O que este projeto faz

- Detecta rostos em tempo real (webcam) ou imagens/vídeos.
- Alinha o rosto usando landmarks (5 ou 68 pontos).
- Extrai **vetores 128D** (embeddings) com o modelo ResNet do dlib.
- (Opcional) Compara embeddings com um banco local para **identificação**.

> Observação: como apenas o arquivo `teste.py` está disponível no repositório público e seu conteúdo pode evoluir, este README descreve a arquitetura e o uso **baseados na estrutura atual do repo** e nos modelos inclusos. Ajuste os comandos conforme sua versão do script.

## 🗂️ Estrutura do projeto

```
Sprint3_IoT/
├─ .gitignore
├─ teste.py
├─ dlib_face_recognition_resnet_model_v1.dat
├─ shape_predictor_5_face_landmarks.dat
└─ shape_predictor_68_face_landmarks.dat
```

- **`teste.py`** — script principal do reconhecimento facial.
- **`shape_predictor_5_face_landmarks.dat`** — landmarks (olhos e nariz), ideal para **alinhamento rápido**.
- **`shape_predictor_68_face_landmarks.dat`** — landmarks completos, útil para **análise facial detalhada**.
- **`dlib_face_recognition_resnet_model_v1.dat`** — **modelo ResNet** que gera vetores 128D para reconhecimento.

## ⚙️ Requisitos

- **Python 3.8+**
- Sistema com toolchain C/C++ instalado (necessário para dlib em muitas plataformas).
- Webcam (para modo em tempo real).

### Dependências Python

Instale num ambiente virtual:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install --upgrade pip wheel setuptools
pip install opencv-python dlib numpy imutils
# Se seu teste.py utilizar:
pip install face-recognition
```

> **Dicas de instalação do dlib**
>
> - **Windows**: instale o [CMake](https://cmake.org/download/), **Visual Studio Build Tools** (C++ build tools) e tente `pip install dlib`.
> - **macOS**: `xcode-select --install` e (opcional) `brew install cmake`. Em Apple Silicon, pode ser necessário `arch -arm64 pip install dlib`.
> - **Linux**: garanta `build-essential`, `cmake`, `libopenblas-dev`, `liblapack-dev`, `libx11-dev` instalados via seu gerenciador de pacotes.

## 🚀 Como executar

1. **Clone** o repositório e entre na pasta:
   ```bash
   git clone https://github.com/Lucas-Umada/Sprint3_IoT.git
   cd Sprint3_IoT
   ```
2. **Ative** seu ambiente virtual e instale as dependências (ver seção anterior).
3. **Execute o script**:
   ```bash
   python teste.py
   ```
   - Se o script aceitar parâmetros (por ex.: `--camera 0`, `--image path.jpg`, `--db faces/`), ajuste aqui:
   ```bash
   # Exemplos (adapte ao seu teste.py)
   python teste.py --camera 0
   python teste.py --image ./amostras/foto1.jpg
   python teste.py --video ./amostras/video.mp4
   python teste.py --db ./faces_cadastradas
   ```

## 🧠 Como funciona (visão técnica resumida)

1. **Detecção**: identifica a face em uma imagem/quadro de vídeo (HOG/CNN do dlib ou `cv2.CascadeClassifier`, conforme implementado).
2. **Landmarks**: aplica `shape_predictor_5_face_landmarks` (mais rápido) ou `shape_predictor_68_face_landmarks` (mais denso) para **alinhamento** do rosto.
3. **Embeddings (128D)**: usa `dlib_face_recognition_resnet_model_v1` para converter o rosto alinhado em um vetor 128‑dimensional.
4. **Comparação** (opcional): calcula a distância (ex.: Euclidiana) entre o embedding de entrada e embeddings cadastrados. Se a distância < **threshold** (ex.: 0.6), considera **match**.

> **Threshold sugerido**: 0.6–0.62 para o modelo do dlib. Ajuste conforme seu cenário e condições de luz/câmera.

## 🧪 Cadastro e base de rostos (opcional)

Uma prática comum é manter uma pasta com subpastas por pessoa, por exemplo:

```
faces_cadastradas/
├─ Enzo/
│  ├─ img1.jpg
│  └─ img2.jpg
├─ Gustavo/
│  ├─ img1.jpg
│  └─ img2.jpg
...
```

Seu script pode:

- Gerar embeddings para cada imagem da base.
- Salvar em `embeddings.npy` + `labels.json`.
- No runtime, comparar o embedding capturado com o banco salvo.

> Se `teste.py` ainda não fizer isso, há espaço para evolução (ver **Roadmap**).

## 🖼️ Espaços para imagens no README

Adicione prints do seu sistema aqui (arraste e solte no GitHub após o commit):

- **Figura 1 — Pipeline geral:** _[insira imagem do fluxo]_
- **Figura 2 — Detecção + landmarks:** _[insira print do rosto com landmarks]_
- **Figura 3 — Reconhecimento em tempo real:** _[insira print da webcam com nome/confiança]_

## 🔧 Solução de problemas

- **Erro ao instalar dlib**: confira toolchain (CMake + compilador). Em ambientes restritos, considere `pip install face-recognition` (que empacota chamadas comuns, mas ainda depende do dlib).
- **Câmera não abre**: verifique permissões do SO; no macOS, conceda acesso a Terminal/IDE.
- **Baixa acurácia**: melhore a **iluminação**, use 5–10 imagens variadas por pessoa, ajuste o **threshold**.
- **Modelos `.dat` não encontrados**: confirme caminhos relativos no código; os três `.dat` estão no diretório raiz do repo.

## 🛡️ Nota ética e de privacidade — uso de dados faciais

Este projeto envolve **dados biométricos** (faces). Siga estes princípios:

1. **Base legal e consentimento**: colete e use imagens **apenas** com consentimento explícito e informado das pessoas identificadas, descrevendo finalidade, retenção e compartilhamento.
2. **Minimização de dados**: capture **apenas** o necessário; evite armazenar imagens cruas quando embeddings forem suficientes para a finalidade.
3. **Segurança**: proteja imagens e embeddings com **criptografia em repouso** e **em trânsito**; restrinja acesso por função.
4. **Retenção e descarte**: defina prazos claros de retenção e procedimentos de **eliminação segura** quando os dados não forem mais necessários.
5. **Transparência**: informe os usuários sobre como o sistema funciona (incluindo riscos de **falsos positivos/negativos**) e disponibilize um canal para dúvidas/remoção de dados.
6. **Avaliação de viés**: teste o sistema com **conjuntos diversos** para reduzir viés demográfico; monitore métricas de erro por grupo.
7. **Uso responsável**: **não** utilize para vigilância invasiva, scoring social ou decisões automatizadas sensíveis sem revisão humana.
8. **Conformidade**: verifique leis locais (ex.: LGPD no Brasil, GDPR na UE). Alguns datasets/modelos possuem **licenças** que **restringem uso comercial** — revise antes de distribuir.

> **Importante**: os arquivos `shape_predictor_68_face_landmarks.dat` e `shape_predictor_5_face_landmarks.dat` são derivados de datasets (ex.: iBUG 300-W) com **restrições de uso**. O modelo `dlib_face_recognition_resnet_model_v1.dat` é distribuído por seus autores para uso gratuito, mas é sua responsabilidade verificar e cumprir as licenças.

## 🗺️ Roadmap sugerido

- [ ] Script de **cadastro** de rostos com salvamento de embeddings/labels.
- [ ] CLI com argumentos (`--camera/--image/--video/--db/--threshold`).
- [ ] Modo **headless** para processar pastas de imagens.
- [ ] Métricas de qualidade (confiança, distância média, FPR/FNR).
- [ ] Dockerfile para ambiente reprodutível (compilação do dlib inclusa).
- [ ] Guia de implantação (Raspberry Pi/Jetson, se aplicável).

## 📚 Referências

- Modelos oficiais dlib (downloads e descrição).
  - shape_predictor_5_face_landmarks: <http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2>
  - shape_predictor_68_face_landmarks: <http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2>
  - dlib_face_recognition_resnet_model_v1: <https://github.com/davisking/dlib-models>
- Exemplo dlib — **face_recognition.py** (uso de 5-point + ResNet 128D).
  - <http://dlib.net/face_recognition.py.html>
- Biblioteca **face_recognition** (empacota dlib): <https://github.com/ageitgey/face_recognition>

## 📝 Licença

Se sua disciplina não especificou, sugiro adicionar uma licença (ex.: MIT/Apache-2.0). **Atenção**: os **pesos `.dat`** podem ter **licenças próprias** distintas da licença do seu código — documente isso neste README.

---

> ## 👨‍💻 Integrantes
>
> Enzo Luiz Goulart - RM99666
> Gustavo Henrique Santos Bonfim - RM98864
> Kayky Paschoal Ribeiro - RM99929
> Lucas Yuji Farias Umada - RM99757
> Natan Eguchi dos Santos - RM98720
> **Sugestões/PRs** são bem-vindos!
