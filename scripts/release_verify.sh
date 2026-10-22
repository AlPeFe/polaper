#!/bin/bash
# Verifica que el APK que se va a publicar es REALMENTE el build de la version declarada.
# Nace del fallo de la v0.2.0: se publico el APK de la v0.1.9 (build de 3 semanas antes)
# porque el assemble nunca se ejecuto y el glob recogio los APKs viejos de app/build/outputs.
#
# Uso: bash scripts/release_verify.sh
# Sale con codigo != 0 y explica el motivo si algo no cuadra.

set -u
cd "$(dirname "$0")/.." || exit 1

fail=0
note() { printf '  %-6s %s\n' "$1" "$2"; }
ok()   { note "OK" "$1"; }
bad()  { note "FALLO" "$1"; fail=$((fail + 1)); }

echo "== Version declarada en app/build.gradle.kts =="
decl_code=$(grep -m1 -E '^[[:space:]]*versionCode[[:space:]]*=' app/build.gradle.kts | tr -dc '0-9')
decl_name=$(grep -m1 -E '^[[:space:]]*versionName[[:space:]]*=' app/build.gradle.kts | sed -E 's/.*"(.*)".*/\1/')
if [ -z "$decl_code" ] || [ -z "$decl_name" ]; then
    bad "no se pudo leer versionCode/versionName de app/build.gradle.kts"
    echo "RESULTADO: FALLO ($fail)"; exit 1
fi
note "info" "versionCode=$decl_code versionName=$decl_name"

bc=app/build/generated/source/buildConfig/debug/eu/kanade/tachiyomi/BuildConfig.java
apk=app/build/outputs/apk/debug/app-universal-debug.apk

echo "== BuildConfig generado =="
if [ ! -f "$bc" ]; then
    bad "no existe $bc (no se ha compilado)"
else
    bc_code=$(grep -m1 'VERSION_CODE' "$bc" | tr -dc '0-9')
    bc_name=$(grep -m1 'VERSION_NAME' "$bc" | sed -E 's/.*"(.*)".*/\1/')
    bc_upd=$(grep -m1 'UPDATER_ENABLED' "$bc" | grep -o 'true')
    [ "$bc_code" = "$decl_code" ] || bad "BuildConfig VERSION_CODE=$bc_code != declarado $decl_code (build viejo)"
    case "$bc_name" in
        "$decl_name"*) ok "VERSION_NAME=$bc_name coincide con $decl_name" ;;
        *) bad "BuildConfig VERSION_NAME=$bc_name no empieza por $decl_name (build viejo)" ;;
    esac
    [ "$bc_upd" = "true" ] && ok "UPDATER_ENABLED=true" || bad "UPDATER_ENABLED=false (compilado sin -Penable-updater)"
fi

echo "== APK universal =="
if [ ! -f "$apk" ]; then
    bad "no existe $apk (no se ha compilado)"
else
    apk_time=$(date -r "$apk" +%s)
    apk_human=$(date -r "$apk" '+%Y-%m-%d %H:%M')
    note "info" "APK: $apk_human ($(du -h "$apk" | cut -f1))"
    # Un APK no puede ser anterior al ultimo commit: si lo es, es de un build viejo.
    last_commit=$(git log -1 --format=%ct)
    if [ "$apk_time" -lt "$last_commit" ]; then
        bad "APK anterior al ultimo commit ($(git log -1 --format='%h %ad' --date=format:'%Y-%m-%d %H:%M')): es un build viejo, vuelve a compilar"
    else
        ok "APK posterior al ultimo commit"
    fi
    if [ -f "$bc" ] && [ "$apk_time" -lt "$(date -r "$bc" +%s)" ]; then
        bad "APK anterior a BuildConfig.java: assemble no se ejecuto tras el ultimo cambio"
    else
        ok "APK generado despues de BuildConfig.java"
    fi
    # Un debug APK de Polaper debe llevar el applicationId con sufijo .dev
    if command -v aapt >/dev/null 2>&1; then
        pkg=$(aapt dump badging "$apk" 2>/dev/null | grep -m1 package | sed -E "s/.*name='([^']+)'.*/\1/")
        [ "$pkg" = "app.polaper.dev" ] && ok "package=$pkg" || bad "package inesperado: '$pkg'"
    fi
fi

echo "== Etiqueta libre =="
tag="v${decl_name}-polaper"
if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    bad "el tag $tag ya existe localmente"
else
    ok "tag $tag disponible"
fi
if git ls-remote --tags --exit-code origin "$tag" >/dev/null 2>&1; then
    bad "el tag $tag ya existe en origin"
else
    ok "tag $tag libre en origin"
fi

echo
if [ "$fail" -eq 0 ]; then
    echo "RESULTADO: OK - APK listo para publicar como $tag (versionCode $decl_code)"
    exit 0
else
    echo "RESULTADO: FALLO ($fail) - NO publicar"
    exit 1
fi
