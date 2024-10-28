# AV2
Repositório para realização do projeto avaliativo de programação 2.

Qualquer dúvida, podem me entrar em contato comigo.

whatsapp: 55 55 984020506.

## Instruções e informaições iniciais

abra o terminal:
  `git --version`
  
Se ainda não possui git instalado:
  https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Para faacilitar o uso do GitHub:
  Instale GitHub CLI
  https://github.com/cli/cli#installation

  Windows: choco install gh
  OS em geral: conda install gh --channel conda-forge

Use https://cli.github.com/manual/gh_auth_login para fazer login com sua conta do GitHub
  gh auth login [flags]

  E

  # Configure git to use GitHub CLI as the credential helper for all authenticated hosts
  # https://cli.github.com/manual/gh_auth_setup-git
$ gh auth setup-git

## Sobre o git e o GitHub
Controle de versões de arquivos: salvar versões e acompanhar mudanças.

Git → software for version control

Github → web hosting repositories

### Git
## Git

`git help [command]`  or `git command --help` 

To stop tracking just remove the .git file created in the repo after init. 

Branch = copy of the repo current version;

Commit = submits changes to the repo; [-m associated message]

pull request = (opens) solicitation for someone to analyze and merge your contribution;

.gitignore = Tells git what file it can ignore when doing a commit; ex: senhas.txt \n teste/

Stash

Workplace 

Index

Local Repo

Remote Repo

Stash saves temporarily;  Workplace (pc); Index = Commit queue; Local .git folder; cloud;
![image-1707095063510.jpg7243234375879575060.jpg](https://prod-files-secure.s3.us-west-2.amazonaws.com/9c8e2005-d1cf-4c11-bc7f-7b18b3bf3e77/5cef32f7-e55f-44e1-9745-22ee6e3919d9/image-1707095063510.jpg7243234375879575060.jpg)

### Create

- git init [nome do projeto]
    - create a new repository
- git clone [url]
    - download a repository
- git branch <name>

### Changes

- git status
    - list pendent files
- git diff
    - shows differences in non-commited files
- git add [file]
    - add changes to staging area
- git reset [file]
    - remove file from staging area; they return to be untracked
- git stash
    - archive changes not commited to the branch;
- git commit -m “message”
    - Commit all file changes since last commit
- git reset <commit hash value>
    - Undo all commits after
- git revert <commit hash value (git log)>

### Synchronization

- git add <name> <url>
    - adds remote repo
- git fetch <remote repo [name] [url]>
    - download ramification without trying to integrate it (to analyze changes).
- git pull
    - download and merge ramification.
- git  push <name>
    - Sends changes to remote repo.

### Tag

- git tag -a name -m ‘message’
- git tag name
- git show tag_name
    - info
- git push origin tag_name
    - sends tag to remote repo
- git push origin  - -delete tag_name
- git tag -d tag_name | deletes locally

### Verify info

- git log

### Branches

- git branch <banch_name>
    - creates branch
- git branch
    - shows current repo’s branches
- git branch -d <name>
- git switch -c [branch_name]
    - switches to specified branch
- git checkout <name>
    - goes to branch  <name>
- git merge <branch_name>
    - merges branch_name with the current branch.
- git rebase master
    - `git checkout <branch4>`  `git rebase <branch3>` it’ll find the common ancestor, obtain the diff and aplly the changes in branch4 to branch3.

### Workflow comum
git clone url path

git remote -v (info about cloned repo)

git branch -a (ls local and remote branches)

% Change file %

git diff (show changes)

git status (shows 1 modified file - changes not staged for commit)

git add -A (adds all files to stage area)

git commit -m “message” (files committed locally) 

git pull origin master (to download any changes made since you downloaded)

git push origin master (origin=name remote repo; master=branch we want to push to)

 

Common Workflow

git branch name1

git branch (ls local branches)

git checkout name1

% Open file and make changes %

git add -A

git commit -m “@” (the commit has no effect on local and remote master branch

git push -u name_remote_repo name1

git branch -a (to see remote and local branches)

(Company runs tests)

They went well:

git checkout master (checkout on local master branch)

git pull name_remote_repo master (to check if changes were made)

git branch - -merged (to check wich branches have been merged)

git merge name1 (merge changes in master branch)

git push name_remote_repo master (push changes to remote repo)

(We can delete the branch used to modify to remote repo)

git branch - -merged

git branch -d name1

git branch -a

git push name_remote_repo- -delete name1

## Clonar

Abra o terminal e entre na pasta que deseje clonar o repositório.
`cd path_para_pasta`
git clone https://github.com/usuario/nome-do-repositorio.git

