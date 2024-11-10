#!/bin/bash

# Caminho para o diretório de hooks personalizados
CUSTOM_HOOKS_DIR="hooks"
GIT_HOOKS_DIR=".git/hooks"

# Verifica se o diretório .git/hooks existe
if [ ! -d "$GIT_HOOKS_DIR" ]; then
  echo "Diretório .git/hooks não encontrado. Certifique-se de que está executando o script na raiz do repositório."
  exit 1
fi

# Copia todos os hooks personalizados para .git/hooks
echo "Copiando hooks personalizados para $GIT_HOOKS_DIR..."

for hook in "$CUSTOM_HOOKS_DIR"/*; do
  hook_name=$(basename "$hook")
  cp "$hook" "$GIT_HOOKS_DIR/$hook_name"
  chmod +x "$GIT_HOOKS_DIR/$hook_name" # Torna o hook executável
  echo "Hook '$hook_name' copiado com sucesso."
done

echo "Todos os hooks foram configurados com sucesso!"
