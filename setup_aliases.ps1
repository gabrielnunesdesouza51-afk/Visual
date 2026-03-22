# Aliases para facilitar a automação de commit e push
# Adicione este arquivo ao seu PowerShell profile
# Uso: echo ". $HOME\Documents\PowerShell\profile.ps1" >> $PROFILE

# Alias para executar o script de commit automaticamente
Set-Alias -Name commit -Value {
    & "$PSScriptRoot\commit.ps1" @args
} -Option AllScope -Force

# Alias curto para commit automático com mensagem padrão
function c {
    param(
        [string]$Mensagem = "Atualização de receitas",
        [string]$Branch = "main"
    )
    & "$PSScriptRoot\commit.ps1" -Mensagem $Mensagem -Branch $Branch
}

# Alias para commit + push rápido com mensagem
function cpush {
    param(
        [string]$Mensagem = "Atualização de receitas"
    )
    & "$PSScriptRoot\commit.ps1" -Mensagem $Mensagem -Branch "main"
}

# Alias para status do git
function gs {
    git status
}

# Alias para log do git
function gl {
    param([int]$Linhas = 10)
    git log --oneline -$Linhas
}
