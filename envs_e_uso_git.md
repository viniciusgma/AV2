# Environment

Pode ser útil criar um novo ambiente antes de clonar o projeto.

Assim, depois de criar e acessar a pasta em que deseja clonar o projeto:

`python -m venv nome_ambiente`

No Windows, para ativar o ambiente:

`nome_ambiente\Scripts\Activate.sp1`

Você pode testar se ativou o ambiente.

No Powershell: Get_Command python

Em outro OS: which python (se não funcionar, tente perguntar ao chat GTP)

Então:

`pip install -r requirements.txt`

# AV2
Repositório para realização do projeto avaliativo de programação 2.

Qualquer dúvida, podem me entrar em contato comigo.

## Instruções e Informações Iniciais
links:

[gh quickstart](https://docs.github.com/en/github-cli/github-cli/quickstart)

[Apostila ufmg git](http://www.cpdee.ufmg.br/~petee/ref/doc/minicursos_oficinas/git/Apostila_git.pdf)

[cheat sheet git e github](https://training.github.com/downloads/pt_BR/github-git-cheat-sheet.pdf)


**Verifique se o Git está instalado:**
   ```bash
   git --version
   ```
Se ainda não possui o Git instalado, você pode fazer isso através do link:
[Instalação do Git]( https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Para facilitar o uso do GitHub, instale o GitHub CLI:
[GitHub CLI](https://github.com/cli/cli#installation)

Windows:
```bash
choco install gh
```
Para sistemas operacionais em geral:
```bash
conda install gh --channel conda-forge
```
[Faça login](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git) na sua conta do GitHub:

```bash
gh auth login [flags]
```
> In the command line, enter gh auth login, then follow the prompts.
    When prompted for your preferred protocol for Git operations, select HTTPS.
     When asked if you would like to authenticate to Git with your GitHub credentials, enter Y.

Configure o Git para usar o GitHub CLI como o helper de credenciais:

```bash
gh auth setup-git
```
## Sobre o Git e o GitHub
Controle de versões de arquivos: permite salvar versões e acompanhar mudanças.

Git: software para controle de versões.
GitHub: hospedagem de repositórios na web.

Comandos básicos do Git:
`git help [command]`  ou `git [command] --help` 

#### Principais Conceitos
**Branch:** Linha de desenvolvimento independente que permite modificar o código sem afetar a versão principal (main). Cria uma cópia da versão atual do repositório.

**Commit:** Envia alterações para o repositório. Use -m para adicionar uma mensagem descritiva sobre as mudanças.

**Pull Request:** Solicitação para que outra pessoa revise e mescle suas contribuições ao projeto.

**.gitignore:** Arquivo que especifica quais arquivos ou pastas devem ser ignorados pelo Git durante um commit (ex.: senhas.txt ou teste/).

**Stash:** Armazena temporariamente alterações não comitadas, permitindo que você limpe seu diretório de trabalho sem perder mudanças.


#### Criar
##### criar repositório e começar a rastrear alterações de arquivos.
  * git init

##### Faz o download de um repositório a partir da URL especificada.
* git clone [url]

##### Cria uma nova branch com o nome especificado.
* git branch <nome_da_branch>

#### Alterações 

##### Exibir o status dos arquivos no diretório de trabalho e na área de staging.
* git status

##### Mostrar as diferenças entre as alterações não comitadas e o último commit.
* git diff

##### Adicionar o arquivo especificado à área de staging para o próximo commit.
* git add [arquivo]

##### Remover o arquivo da área de staging, retornando-o ao estado não rastreado.
git reset [arquivo]

##### Salvar temporariamente as alterações não comitadas, permitindo reverter a um diretório de trabalho limpo.
* git stash


##### Registrar as alterações na área de staging no repositório com uma mensagem associada.
git commit -m "mensagem"

##### Reverter para um commit anterior, desfazendo todos os commits após o hash especificado.
* git reset <hash_do_commit>

##### Criar um novo commit que desfaz as alterações feitas pelo commit especificado.
* git revert <hash_do_commit>

##### Exibe o histórico de commits do repositório.
* git log

#### Sincronização
##### Faz o download das alterações do repositório remoto sem mesclá-las.
* git fetch <nome_remoto>

##### Baixa as alterações do repositório remoto e as mescla na branch atual.
* git pull
 
##### Envia as alterações comitadas para o repositório remoto especificado.
* git push <nome_remoto>


#### Branches
##### Cria uma nova branch com o nome especificado.
* git branch <nome_da_branch>

##### Lista todas as branches no repositório atual.
* git branch

##### Remove a branch especificada.
* git branch -d <nome>

##### Cria e muda para a branch especificada.
* git switch -c <nome_da_branch>

##### Muda para a branch especificada.
* git checkout <nome_da_branch>

##### Mescla a branch especificada na branch atual.
* git merge <nome_da_branch>

##### Reaplica os commits da branch atual em cima da branch base especificada, permitindo um histórico linear do projeto.
* git rebase <branch_base>

### Workflow

Clonar o repositório remoto:
```bash
git clone <url> <path>
```

Ou ver status e puxar do remoto pull para garantir estar atualizado:
```bash
git status
git pull
```

Listar todas as branches (locais e remotas):
```bash
git branch -a
```

Criar branch:
```bash
git branch name_brach
```
Acessar branch:
```bash
git checkout name_branch
```

**Modificar os arquivos.**

Adicionar todas as mudanças ao staging:
```bash
git add -A
```

Realizar um commit:
```bash
git commit -m "Mensagem descritiva do commit"
```

Acessar main:
```bash
git checkout main
```

Baixar e mesclar mudanças do repositório remoto:
```bash
git pull
```

Mesclar branches:
```bash
git merge branch_name
```

Listar branches mergidos:
```bash
git branch --merged
```

Enviar as mudanças para o repositório remoto:
```bash
git push
```

Deletar a branch usada para as modificações:
```bash
git branch -d branch_name
```

Listar todas as branches novamente:
```bash
git branch -a
```

Deletar a branch do repositório remoto:
```bash
git push origin --delete branch_name
```
