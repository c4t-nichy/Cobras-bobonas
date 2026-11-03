# Cobras-bobonas

## Criptografar textos

Aplicativo gráfico em Python para criptografar e descriptografar textos com senha. A criptografia usa Fernet com uma chave derivada por PBKDF2-HMAC-SHA256 e salt aleatório. O resultado pode ser copiado para a área de transferência.

### Como executar

```bash
python3 -m pip install -r requirements.txt
python3 text_cipher.py
```

Digite ou cole o texto, informe uma senha e escolha **Criptografar** ou **Descriptografar**. Use **Copiar resultado** para copiar a saída.

Guarde a senha: não é possível recuperar o texto sem ela. O resultado criptografado inclui o salt necessário para derivar a chave, mas não inclui a senha.

### Versão no navegador

Para iniciar a interface web local:

```bash
python3 web_app.py
```

Abra `http://localhost:8000`. O servidor é destinado a uso local e não deve ser exposto publicamente.