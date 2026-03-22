# Script de Automação para Commit e Push no GitHub
# Para usar: .\commit.ps1 -Mensagem "Sua mensagem" -Branch "main"

param(
    [string]$Mensagem = "Atualização de receitas",
    [string]$Branch = "main",
    [string]$CaminhoRepo = "."
)

function Executar-Comando {
    param(
        [string]$Comando,
        [bool]$MostrarErro = $true
    )
    
    try {
        $output = & cmd /c "$Comando 2>&1"
        $sucesso = $LASTEXITCODE -eq 0
        return @{ Sucesso = $sucesso; Output = $output }
    }
    catch {
        if ($MostrarErro) {
            Write-Host "❌ Erro ao executar: $Comando" -ForegroundColor Red
        }
        return @{ Sucesso = $false; Output = $_.Exception.Message }
    }
}

function Verificar-GitInicializado {
    $resultado = Executar-Comando "git -C $CaminhoRepo status" $false
    return $resultado.Sucesso
}

function Inicializar-Git {
    if (-not (Verificar-GitInicializado)) {
        Write-Host "📁 Inicializando repositório Git..." -ForegroundColor Cyan
        $resultado = Executar-Comando "git -C $CaminhoRepo init"
        if ($resultado.Sucesso) {
            Write-Host "✅ Repositório inicializado" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Falha ao inicializar repositório" -ForegroundColor Red
            return $false
        }
    }
    else {
        Write-Host "✅ Repositório Git já inicializado" -ForegroundColor Green
        return $true
    }
}

function Verificar-ArquivosPendentes {
    $resultado = Executar-Comando "git -C $CaminhoRepo status --porcelain" $false
    
    if ($resultado.Output) {
        Write-Host "`n📝 Arquivos pendentes:" -ForegroundColor Cyan
        $resultado.Output | ForEach-Object {
            if ($_) {
                Write-Host "   $_" -ForegroundColor Yellow
            }
        }
        return $true
    }
    return $false
}

function Adicionar-Arquivos {
    Write-Host "`n📦 Adicionando arquivos ao Git..." -ForegroundColor Cyan
    $resultado = Executar-Comando "git -C $CaminhoRepo add -A"
    
    if ($resultado.Sucesso) {
        Write-Host "✅ Arquivos adicionados com sucesso" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "❌ Falha ao adicionar arquivos" -ForegroundColor Red
        return $false
    }
}

function Fazer-Commit {
    param([string]$MsgCommit)
    
    Write-Host "`n💾 Fazendo commit com mensagem: '$MsgCommit'" -ForegroundColor Cyan
    $resultado = Executar-Comando "git -C $CaminhoRepo commit -m `"$MsgCommit`""
    
    if ($resultado.Sucesso) {
        Write-Host "✅ Commit realizado com sucesso" -ForegroundColor Green
        return $true
    }
    else {
        if ($resultado.Output -match "nothing to commit|nothing added to commit") {
            Write-Host "ℹ️  Nenhuma mudança para fazer commit" -ForegroundColor Yellow
            return $true
        }
        Write-Host "❌ Falha ao fazer commit" -ForegroundColor Red
        return $false
    }
}

function Fazer-Push {
    Write-Host "`n🚀 Fazendo push para o branch '$Branch'..." -ForegroundColor Cyan
    $resultado = Executar-Comando "git -C $CaminhoRepo push origin $Branch"
    
    if ($resultado.Sucesso) {
        Write-Host "✅ Push realizado com sucesso" -ForegroundColor Green
        return $true
    }
    else {
        if ($resultado.Output -match "no changes added to commit") {
            Write-Host "ℹ️  Nenhuma mudança para fazer push" -ForegroundColor Yellow
            return $true
        }
        Write-Host "⚠️  Não foi possível fazer push" -ForegroundColor Yellow
        Write-Host "   Verifique a conexão ou configuração do Git" -ForegroundColor Yellow
        return $false
    }
}

function Exibir-StatusFinal {
    Write-Host "`n" + ("="*60) -ForegroundColor Cyan
    Write-Host "📊 STATUS FINAL DO REPOSITÓRIO" -ForegroundColor Cyan
    Write-Host ("="*60) -ForegroundColor Cyan
    
    $resultado = Executar-Comando "git -C $CaminhoRepo status" $false
    if ($resultado.Sucesso) {
        Write-Host $resultado.Output -ForegroundColor White
    }
    
    Write-Host "`n📜 ÚLTIMOS COMMITS:" -ForegroundColor Cyan
    $resultado = Executar-Comando "git -C $CaminhoRepo log --oneline -5" $false
    if ($resultado.Sucesso) {
        Write-Host $resultado.Output -ForegroundColor White
    }
}

# === EXECUÇÃO PRINCIPAL ===
Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "🔄 AUTOMATIZAÇÃO DE COMMIT E PUSH" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan
Write-Host "⏰ $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')`n" -ForegroundColor White

# Etapa 1: Inicializar Git
if (-not (Inicializar-Git)) {
    Write-Host "❌ Não foi possível inicializar o repositório" -ForegroundColor Red
    exit 1
}

# Etapa 2: Verificar arquivos pendentes
if (-not (Verificar-ArquivosPendentes)) {
    Write-Host "ℹ️  Nenhum arquivo pendente para commit" -ForegroundColor Yellow
    Exibir-StatusFinal
    exit 0
}

# Etapa 3: Adicionar arquivos
if (-not (Adicionar-Arquivos)) {
    Write-Host "❌ Não foi possível adicionar arquivos" -ForegroundColor Red
    exit 1
}

# Etapa 4: Fazer commit
if (-not (Fazer-Commit -MsgCommit $Mensagem)) {
    Write-Host "❌ Não foi possível fazer commit" -ForegroundColor Red
    exit 1
}

# Etapa 5: Fazer push
if (-not (Fazer-Push)) {
    Write-Host "⚠️  Commit realizado, mas push falhou" -ForegroundColor Yellow
}

# Exibir status final
Exibir-StatusFinal

Write-Host "`n" + ("="*60) -ForegroundColor Green
Write-Host "✅ PROCESSO CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host ("="*60) + "`n" -ForegroundColor Green
