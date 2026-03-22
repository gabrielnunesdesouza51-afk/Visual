@echo off
REM Script de Automação para Commit e Push no GitHub
REM Uso: commit.bat "Mensagem do commit" main

::=================================================
:: CONFIGURAÇÕES
::=================================================
setlocal enabledelayedexpansion

set "MENSAGEM=%~1"
set "BRANCH=%~2"

if "%MENSAGEM%"=="" (
    set "MENSAGEM=Atualização de receitas"
)

if "%BRANCH%"=="" (
    set "BRANCH=main"
)

::=================================================
:: CABEÇALHO
::=================================================
cls
echo.
echo ============================================================
echo.  AUTOMATIZAÇÃO DE COMMIT E PUSH
echo ============================================================
echo.
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c/%%a/%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)
echo.  Data/Hora: %mydate% %mytime%
echo.
echo.  Mensagem: "%MENSAGEM%"
echo.  Branch:   %BRANCH%
echo.
echo ============================================================
echo.

::=================================================
:: VERIFICAR SE GIT ESTÁ INSTALADO
::=================================================
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo ERRO: Git não está instalado ou não está no PATH
    echo.
    echo Faça download em: https://git-scm.com/download/win
    pause
    exit /b 1
)

::=================================================
:: VERIFICAR SE REPOSITÓRIO GIT FOI INICIALIZADO
::=================================================
if not exist ".git" (
    echo.
    echo Inicializando repositório Git...
    git init >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        color 0A
        echo OK - Repositório inicializado
        color 0F
    ) else (
        color 0C
        echo ERRO - Falha ao inicializar repositório
        pause
        exit /b 1
    )
)

::=================================================
:: VERIFICAR ARQUIVOS PENDENTES
::=================================================
echo.
echo Verificando arquivos pendentes...
git status --porcelain >temp_status.txt 2>&1

for /f "tokens=*" %%A in (temp_status.txt) do (
    set "STATUS_LINE=%%A"
)

if defined STATUS_LINE (
    color 0E
    echo Arquivos pendentes:
    echo.
    type temp_status.txt
    echo.
    color 0F
) else (
    echo Nenhum arquivo pendente
    del temp_status.txt
    goto :EOF
)

del temp_status.txt

::=================================================
:: ADICIONAR ARQUIVOS
::=================================================
echo.
echo Adicionando arquivos ao Git...
git add -A >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    color 0A
    echo OK - Arquivos adicionados
    color 0F
) else (
    color 0C
    echo ERRO - Falha ao adicionar arquivos
    color 0F
    pause
    exit /b 1
)

::=================================================
:: FAZER COMMIT
::=================================================
echo.
echo Fazendo commit: "%MENSAGEM%"
git commit -m "%MENSAGEM%" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    color 0A
    echo OK - Commit realizado
    color 0F
) else (
    color 0E
    echo AVISO - Falha ao fazer commit ou nada para commitar
    color 0F
)

::=================================================
:: FAZER PUSH
::=================================================
echo.
echo Fazendo push para branch '%BRANCH%'...
git push origin %BRANCH% >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    color 0A
    echo OK - Push realizado
    color 0F
) else (
    color 0E
    echo AVISO - Falha ao fazer push
    echo Verifique a conexão ou configuração do Git
    color 0F
)

::=================================================
:: EXIBIR STATUS FINAL
::=================================================
echo.
echo ============================================================
echo Status do repositório:
echo ============================================================
echo.
git status
echo.

echo ============================================================
echo Últimos commits:
echo ============================================================
echo.
git log --oneline -5

echo.
echo ============================================================
color 0A
echo OK - Processo concluído com sucesso!
echo ============================================================
color 0F
echo.

pause
