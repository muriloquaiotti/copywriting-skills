# Copywriting Skills

Uma skill em português para agentes de IA criarem e analisarem **anúncios, VSLs, landing pages, páginas de site, e-mails e outras peças de copy**.

A entrada única é **`copywriting`**. Ela inclui referências sintetizadas de cinco livros, com 59 arquivos de capítulos ou seções, e carrega somente o material pertinente ao pedido. Funciona sem os PDFs e sem instalar cinco outras skills.

## Instalação

Requer Git e Python 3.9 ou superior para usar o instalador. A skill em si contém Markdown e não exige Python, API paga ou ferramenta específica de navegação.

```bash
git clone https://github.com/muriloquaiotti/copywriting-skills.git
cd copywriting-skills
python3 scripts/install.py --scope user
```

Isso instala `copywriting` em `~/.agents/skills/`, disponível para o usuário em diferentes projetos. Para instalar apenas em um projeto:

```bash
python3 scripts/install.py --scope project --project "/caminho/do/projeto"
```

A instalação por projeto usa `.agents/skills/copywriting/`. Esses locais seguem a [documentação oficial de skills](https://learn.chatgpt.com/docs/build-skills). Abra uma nova sessão se a instalação não aparecer na sessão atual.

Também é possível copiar manualmente a pasta `skills/copywriting` inteira para o diretório de skills aceito pelo seu agente. Outros agentes podem exigir um local ou uma referência explícita próprios; a leitura automática de `AGENTS.md` e a sintaxe `$copywriting` dependem do agente.

### Atualização

```bash
git pull --ff-only
python3 scripts/install.py --scope user --replace
```

O instalador não sobrescreve versões diferentes por padrão. Com `--replace`, preserva a versão anterior em `.agents/skill-backups/`, fora do diretório de descoberta. Uma instalação idêntica não é alterada. Para atualização por projeto, use novamente `--scope project --project "/caminho/do/projeto" --replace`.

## Uso

```text
Use $copywriting para analisar a copy desta landing page: [URL].
Priorize os problemas e reescreva a primeira dobra e o CTA.
```

```text
Use $copywriting para criar três roteiros de anúncios de 30 segundos
para [produto], com fala, cenas, texto na tela e ângulos diferentes.
```

```text
Use $copywriting para escrever uma VSL de [duração] usando o briefing,
as provas e as condições da oferta disponíveis neste projeto.
```

Há mais [exemplos de pedidos](examples/pedidos.md). A skill permite seleção automática por descrição; a invocação explícita ajuda a escolhê-la quando há outras skills de copywriting instaladas.

### Orientar os agentes de um projeto

Após instalar por projeto, acrescente ao `AGENTS.md` existente, preservando as outras instruções:

```markdown
Para criação, revisão ou análise de copy de marketing, leia
`.agents/skills/copywriting/SKILL.md` e aplique o fluxo pertinente.
Use o briefing, a voz da marca, as provas e os termos reais deste projeto.
Entregue o texto solicitado e identifique informações ainda pendentes.
```

Se preferir instalação global, aponte para `~/.agents/skills/copywriting/SKILL.md`. Essa orientação se destina a agentes que leem `AGENTS.md`; veja a [documentação de personalização](https://learn.chatgpt.com/docs/customization/overview).

## Como trabalha

- **Anúncios:** ângulo, lead, fala, apoio visual, CTA e duração estimada.
- **VSLs:** progressão do argumento, provas, objeções, oferta e narração completa.
- **Páginas:** mensagem principal, seções, benefícios, diferenciação, provas e próximo passo.
- **Auditoria:** achados vinculados a trechos observados, prioridades, reescritas e hipóteses de teste.
- **Revisão:** CUB — confuso, inverossímil, tedioso — e verificação de ideia, promessa, prova e credibilidade.

Para analisar uma URL, o agente precisa de acesso à página por alguma ferramenta disponível. Texto colado ou arquivos locais também funcionam. Uma extração textual não equivale a uma inspeção visual, e a skill distingue essas limitações. Ela não inventa provas nem apresenta hipóteses editoriais como resultados medidos de conversão.

## Referências

| Livro | Uso |
|---|---|
| Breakthrough Advertising — Eugene Schwartz | Desejo, consciência, sofisticação e argumento |
| Great Leads — Michael Masterson e John Forde | Ideia única e escolha da abertura |
| Copy Logic — Michael Masterson e Mike Palmer | Diagnóstico e revisão |
| Quick Start Copywriting — Clayton Makepeace | Ritmo, bullets, fechamento e peças auxiliares |
| $100M Offers — Alex Hormozi | Estrutura da oferta e equação de valor |

Consulte [fontes e limites das edições](skills/copywriting/references/fontes.md). Breakthrough usa uma edição resumida; Quick Start cobre apenas o volume 2; dois livros passaram por OCR e 100M Offers usa uma tradução automática. As referências são sínteses operacionais, não os textos integrais dos livros.

A conversão inicial utilizou [book-to-skill](https://github.com/virgiliojr94/book-to-skill). O pacote não distribui esse conversor, os PDFs nem bibliotecas particulares do projeto de origem.

## Estrutura

```text
skills/copywriting/
  SKILL.md
  agents/openai.yaml
  references/
    roteiros.md
    paginas.md
    fontes.md
    books/                 # cinco referências e seus capítulos
scripts/
  install.py               # instalação com proteção contra sobrescrita
  validate.py              # links, cobertura e portabilidade
examples/pedidos.md
```

Para verificar o pacote:

```bash
python3 scripts/validate.py
python3 scripts/test_install.py
```

A validação estrutural não mede desempenho comercial. Os cenários de revisão de comportamento estão em [examples/avaliacao.md](examples/avaliacao.md).

## Licença

[MIT](LICENSE) para o código e a redação original deste pacote. As obras e marcas citadas permanecem pertencentes aos respectivos titulares; a licença não concede direitos sobre os livros originais nem implica endosso dos autores.
