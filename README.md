# IR - Gerador de relatório para declaração do imposto de renda

Este projeto tem como objetivo simplificar o processo de declaração de investimentos no imposto de renda, gerando relatórios detalhados e organizados que incluem ações, fundos imobiliários e BDR's.

## Pré-requisitos

- **Python** - [Python Download](https://www.python.org/downloads/release/python-3123/)

## Instalação

Clone esse projeto em seu computador com o comando:

```
git clone https://github.com/Nilsantos/ir.git
```

Na pasta do projeto, digite o seguinte comando de acordo com seu sistema operacional:

Windows

```
venv/Scripts/activate
```

Linux

```
source venv/bin/activate
```

Digite o seguinte comando para instalar as dependências do projeto:

```
pip install -r ./requirements.txt
```

## Arquivos necessários

1. Acesse a Área do investidor no site da B3 e realize o login; [Site B3](https://www.investidor.b3.com.br/login)

2. Baixe todos os relátorios de movimentações [Movimentações B3](https://www.investidor.b3.com.br/extrato/movimentacao)

3. Baixe o relatório consolidado do ano atual [Consolidado B3](https://www.investidor.b3.com.br/relatorios/mensal-consolidado)

4. Insira os relatórios de movimentações na pasta input > movimentações

5. Insira o relatório consolidado na pasta input > consolidado

## Execução

Após ter configurado o projeto e adicionado os arquivos necessário execute o comando para gerar o relatório do IR:

```
python main.py generate-ir-report
```

O arquivo será gerado na pasta output > "Relátorio IR.pdf"

## Funcionalidades

- Consolidar a posição de Ações, Fundos imobiliários e BDR's;
- Consolidar os dividendos e juros sobre capital próprio recebidos;
- Fornecer um relátorio passo a passo dos itens necessários para declarar Ações, Fundos imobiliários e BDR's no imposto de renda.

## Próximos passos

- Obter o valor pago nas subscrições para calcular o preço médio corretamente;
- Obter o preço médio em ações que mudaram o código de negociação;
- Tabela mensal de lucro e prejuizo;
- Calculo de lucro com vendas abaixo de 20k no mês;
- Criação de testes unitários;

## Exemplo do relatório gerado

## Links

- [Como declarar ações no Imposto de Renda 2024](https://www.infomoney.com.br/guias/declarar-acoes-imposto-de-renda-ir/)
- [Como declarar fundos imobiliários no Imposto de Renda](https://www.infomoney.com.br/guias/fundos-imobiliarios-fiis-imposto-de-renda-ir/)
- [Como declarar BDRs no Imposto de Renda 2024](https://www.infomoney.com.br/guias/bdr-imposto-de-renda-ir/)

## Autores

<table>
  <tr>
    <td align="center"><a href="https://github.com/Nilsantos"><img src="https://avatars.githubusercontent.com/u/44170812?v=4" width="100px;" alt="Nilsantos"/><br><sub><b>Nilsantos</b></sub></a></td>
  </tr>
</table>

## Licença

The MIT License (MIT)

Copyright (c) [2024] [IR]

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
