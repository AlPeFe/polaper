package eu.kanade.presentation.browse.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import mihon.icons.materialsymbols.MaterialSymbols
import mihon.icons.materialsymbols.rounded.CollectionsBookmark
import tachiyomi.presentation.core.components.Badge

@Composable
internal fun InLibraryBadge(enabled: Boolean) {
    if (enabled) {
        Badge(
            imageVector = MaterialSymbols.Rounded.CollectionsBookmark,
        )
    }
}

/**
 * Tiny red dot shown on manga covers in browse search when the manga is known to
 * have zero chapters (already fetched once, nothing stored locally).
 */
@Composable
internal fun RowScope.NoChaptersBadge(enabled: Boolean) {
    if (enabled) {
        Box(
            modifier = Modifier
                .align(Alignment.CenterVertically)
                .size(NoChaptersDotSize)
                .background(MaterialTheme.colorScheme.error, CircleShape),
        )
    }
}

internal val NoChaptersDotSize = 8.dp