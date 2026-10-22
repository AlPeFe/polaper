package tachiyomi.domain.release.interactor

import dev.zacsweers.metro.Inject
import tachiyomi.domain.release.model.Release
import tachiyomi.domain.release.service.ReleaseService

@Inject
class GetApplicationRelease(
    private val service: ReleaseService,
) {
    suspend fun await(arguments: Arguments): Result {
        val release = service.latest(arguments) ?: return Result.NoNewUpdate

        // Check if latest version is different from current version
        val isNewVersion = isNewVersion(
            arguments.isNightly,
            arguments.commitCount,
            arguments.versionName,
            release.version,
        )
        return when {
            isNewVersion -> Result.NewUpdate(release)
            else -> Result.NoNewUpdate
        }
    }

    private fun isNewVersion(
        isNightly: Boolean,
        commitCount: Int,
        versionName: String,
        versionTag: String,
    ): Boolean {
        return if (isNightly) {
            // Nightly builds: based on releases in "mihonapp/mihon-preview" repo
            // tagged as something like "r1234"
            // Polaper: los builds debug añaden "-<commitCount>" al versionName; sin quitarlo
            // el sufijo numerico se colaba en la comparacion y ocultaba updates.
            val newVersion = versionTag.substringBefore("-").replace("[^\\d.]".toRegex(), "")
            (newVersion.toIntOrNull() ?: 0) > commitCount
        } else {
            // Release builds: based on releases in "AlPeFe/polaper" repo
            // tagged as something like "v0.1.2-polaper"
            // Polaper: quitamos el sufijo "-<commitCount>" de los builds debug antes de
            // comparar; si no, "0.2.0-7979" se leia como 0.2.7979 y un 0.2.1 nunca se veia.
            val newVersion = versionTag.substringBefore("-").replace("[^\\d.]".toRegex(), "")
            val oldVersion = versionName.substringBefore("-").replace("[^\\d.]".toRegex(), "")

            val newSemVer = newVersion.split(".").mapNotNull { it.toIntOrNull() }
            val oldSemVer = oldVersion.split(".").mapNotNull { it.toIntOrNull() }

            // Comparacion componente a componente (la de upstream solo miraba si el nuevo
            // era mayor en algun indice y fallaba al comparar distinto numero de partes).
            for (index in 0 until maxOf(newSemVer.size, oldSemVer.size)) {
                val newPart = newSemVer.getOrElse(index) { 0 }
                val oldPart = oldSemVer.getOrElse(index) { 0 }
                if (newPart != oldPart) {
                    return newPart > oldPart
                }
            }

            false
        }
    }

    data class Arguments(
        val isFoss: Boolean,
        val isNightly: Boolean,
        val commitCount: Int,
        val versionName: String,
        val repository: String,
        val forceCheck: Boolean = false,
    )

    sealed interface Result {
        data class NewUpdate(val release: Release) : Result
        data object NoNewUpdate : Result
        data object OsTooOld : Result
    }
}
