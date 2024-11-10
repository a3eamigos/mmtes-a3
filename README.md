# MMTeS-A3
Este repositório é dedicado ao trabalho da disciplina **Modelos, Métodos e Técnicas de Engenharia de Software**.

---

## Configuração Importante no Git

Antes de começar a modificar o projeto, siga os passos abaixo para garantir que seu ambiente esteja corretamente configurado:

1. **Copie o arquivo `commit-msg`**: 
   - Localize o arquivo `commit-msg` dentro da pasta `hooks`.

2. **Navegue até a pasta `.git/hooks`**:
   - Encontre o diretório `.git` no repositório e acesse a subpasta `hooks`.

3. **Cole o arquivo `commit-msg`**:
   - Transfira o arquivo `commit-msg` copiado para dentro da pasta `.git/hooks`.

4. **Abra o terminal na pasta `.git/hooks`**:
   - Navegue até o diretório `.git/hooks` no terminal.

5. **Teste o funcionamento**:
   - Tente realizar um commit com uma mensagem incorreta para garantir que o hook está funcionando. Exemplo:
     ```bash
     git commit -m "mensagem inválida"
     ```
   
Se tudo estiver correto, o hook `commit-msg` impedirá que commits com mensagens fora do padrão sejam realizados.

---

Com essas etapas concluídas, você estará pronto para contribuir com o projeto de maneira estruturada e conforme as boas práticas de versionamento.
