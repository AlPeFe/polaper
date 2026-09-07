<div align="center">

<img src="./.github/assets/logo.png" alt="Polaper logo" title="Polaper logo" width="140"/>

# Polaper

### Lector de manga para Android — fork personal de [Mihon](https://github.com/mihonapp/mihon)

Lector de manga, webtoons y cómics, libre y open source (Apache-2.0), con branding y funciones propias. Uso personal.

[![License: Apache-2.0](https://img.shields.io/github/license/AlPeFe/polaper?labelColor=27303D&color=0877d2)](/LICENSE)

</div>

## ✨ Funciones propias de este fork

- **Indicador de mangas sin capítulos**: un punto rojo en la portada (esquina inferior derecha) marca los mangos que ya conoces y tienen 0 capítulos, en los 3 modos de vista de Explorar.
- **Filtro y aviso "Missing source"**: en la biblioteca, un badge circular junto al título muestra cuántos mangos han perdido su extensión/fuente; púlsalo (o usa el filtro en Ajustes) para verlos.
- **Búsqueda sin anclados**: la búsqueda global usa siempre todas las fuentes activas (eliminado el selector "Anclados" por defecto).
- **Auto-actualización contra este repo**: la app comprueba las releases de `AlPeFe/polaper` (Ajustes → Acerca de → Buscar actualizaciones).
- **Branding propio**: nombre, icono y splash sin marca de Mihon.

## 📥 Descargar / actualizar

Las releases están en la página de [Releases](https://github.com/AlPeFe/polaper/releases) (APK firmados de debug, para uso personal).

La app (v0.1.3+) se auto-actualiza desde este mismo repositorio.

## 🚀 Compilar

Requiere JDK 21+ y Android SDK.

```bash
./gradlew :app:assembleDebug -Penable-updater
```

El APK queda en `app/build/outputs/apk/debug/`.

## 🔌 Extensiones

Las extensiones se cargan desde un repositorio de extensiones dentro de la app (Ajustes → Examinar → Repositorios de extensiones), p. ej. [keiyoushi/extensions](https://github.com/keiyoushi/extensions). Se actualizan de forma independiente a la app.

## 🛠️ Características (heredadas de Mihon)

- Lector configurable: múltiples visores, direcciones de lectura y más ajustes.
- Seguimiento (tracking) con MangaBaka, MyAnimeList, AniList, Kitsu, MangaUpdates, Shikimori, Bangumi y Hikka.
- Categorías para organizar tu biblioteca.
- Temas claro y oscuro.
- Actualización programada de la biblioteca.
- Copias de seguridad locales o a la nube.
- Y mucho más.

## 📚 Créditos y licencia

Este proyecto es un **fork de [Mihon](https://github.com/mihonapp/mihon)** (heredero de Tachiyomi). Todo el mérito del lector original es de sus autores y colaboradores.

<pre>
Copyright © 2015 Javier Tomás
Copyright © 2024 Mihon Open Source Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
</pre>

### Disclaimer

Esta aplicación no tiene ninguna afiliación con los proveedores de contenido disponibles y no aloja contenido propio.
