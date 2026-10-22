package tachiyomi.domain.release.interactor

import io.kotest.matchers.shouldBe
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import tachiyomi.domain.release.model.Release
import tachiyomi.domain.release.service.ReleaseService

class GetApplicationReleaseTest {

    private lateinit var getApplicationRelease: GetApplicationRelease
    private lateinit var releaseService: ReleaseService

    @BeforeEach
    fun beforeEach() {
        releaseService = mockk()

        getApplicationRelease = GetApplicationRelease(releaseService)
    }

    @Test
    fun `When has update but is nightly expect new update`() = runTest {
        val release = Release(
            "r2000",
            "info",
            "http://example.com/release_link",
            "http://example.com/release_link.apk",
        )

        coEvery { releaseService.latest(any()) } returns release

        val result = getApplicationRelease.await(
            GetApplicationRelease.Arguments(
                isFoss = false,
                isNightly = true,
                commitCount = 1000,
                versionName = "",
                repository = "test",
            ),
        )

        (result as GetApplicationRelease.Result.NewUpdate).release shouldBe GetApplicationRelease.Result.NewUpdate(
            release,
        ).release
    }

    @Test
    fun `When has update expect new update`() = runTest {
        val release = Release(
            "v2.0.0",
            "info",
            "http://example.com/release_link",
            "http://example.com/release_link.apk",
        )

        coEvery { releaseService.latest(any()) } returns release

        val result = getApplicationRelease.await(
            GetApplicationRelease.Arguments(
                isFoss = false,
                isNightly = false,
                commitCount = 0,
                versionName = "v1.0.0",
                repository = "test",
            ),
        )

        (result as GetApplicationRelease.Result.NewUpdate).release shouldBe GetApplicationRelease.Result.NewUpdate(
            release,
        ).release
    }

    @Test
    fun `When has no update expect no new update`() = runTest {
        val release = Release(
            "v1.0.0",
            "info",
            "http://example.com/release_link",
            "http://example.com/release_link.apk",
        )

        coEvery { releaseService.latest(any()) } returns release

        val result = getApplicationRelease.await(
            GetApplicationRelease.Arguments(
                isFoss = false,
                isNightly = false,
                commitCount = 0,
                versionName = "v2.0.0",
                repository = "test",
            ),
        )

        result shouldBe GetApplicationRelease.Result.NoNewUpdate
    }

    // Polaper: los builds publicados son debug y llevan "-<commitCount>" pegado al versionName
    // (0.2.1-8218). Antes el saneado numerico lo convertia en 0.2.8218 y un salto de parche
    // no se detectaba nunca, ademas de que el indexado podia petar si cambiaba el nº de partes.

    private fun polaperRelease(tag: String) = Release(
        tag,
        "info",
        "https://github.com/AlPeFe/polaper/releases/tag/$tag",
        "https://github.com/AlPeFe/polaper/releases/download/$tag/app-universal-debug.apk",
    )

    private suspend fun check(installed: String, tag: String): GetApplicationRelease.Result {
        coEvery { releaseService.latest(any()) } returns polaperRelease(tag)
        return getApplicationRelease.await(
            GetApplicationRelease.Arguments(
                isFoss = false,
                isNightly = false,
                commitCount = installed.substringAfter("-", "0").toIntOrNull() ?: 0,
                versionName = installed,
                repository = "AlPeFe/polaper",
            ),
        )
    }

    @Test
    fun `When installed debug build matches latest tag expect no new update`() = runTest {
        // El bucle de la v0.2.0: la app ya tiene la version publicada y seguia pidiendo actualizar.
        check("0.2.1-8218", "v0.2.1-polaper") shouldBe GetApplicationRelease.Result.NoNewUpdate
    }

    @Test
    fun `When latest is a patch above installed debug build expect new update`() = runTest {
        // Antes del arreglo: 0.2.1 > 0.2.8218 era false y el update nunca aparecia.
        (check("0.2.1-8218", "v0.2.2-polaper") is GetApplicationRelease.Result.NewUpdate) shouldBe true
    }

    @Test
    fun `When installed is older release expect new update`() = runTest {
        (check("0.1.9-7979", "v0.2.1-polaper") is GetApplicationRelease.Result.NewUpdate) shouldBe true
    }

    @Test
    fun `When installed is newer than latest expect no new update`() = runTest {
        check("0.3.0-9000", "v0.2.9-polaper") shouldBe GetApplicationRelease.Result.NoNewUpdate
    }
}
