import unittest

from area_reader_v2.command_group_recommendations import (
    ALL_COMMAND_GROUPS,
    recommend_command_groups,
)


class CommandGroupRecommendationTests(unittest.TestCase):
    def test_generic_issue_uses_conservative_default_recommendations(self):
        result = recommend_command_groups(
            issue_text="Run local verification before issue-to-PR readiness.",
            changed_paths=[],
        )

        self.assertEqual(result["available_command_groups"], ALL_COMMAND_GROUPS)
        self.assertEqual(
            result["recommended_command_groups"],
            [
                "env",
                "dotnet-solution",
                "node-root",
                "markdown-smoke",
            ],
        )
        self.assertNotIn("maui-android-doctor", result["recommended_command_groups"])
        self.assertNotIn("maui-android-build", result["recommended_command_groups"])
        self.assertNotIn("ci-manual-reference", result["recommended_command_groups"])
        self.assertIn("conditional_command_groups", result)

    def test_api_client_group_is_recommended_for_openapi_issue_text(self):
        result = recommend_command_groups(
            issue_text="Regenerate the TypeScript client from the OpenAPI contract.",
            changed_paths=[],
        )

        self.assertIn("api-client-generate", result["recommended_command_groups"])

    def test_api_client_group_is_recommended_for_backend_contract_paths(self):
        result = recommend_command_groups(
            issue_text="Update backend behavior.",
            changed_paths=["phoodab/apps/api/openapi.json"],
        )

        self.assertIn("api-client-generate", result["recommended_command_groups"])

    def test_web_group_is_recommended_for_web_scope(self):
        result = recommend_command_groups(
            issue_text="Fix React component rendering.",
            changed_paths=["phoodab/apps/web/src/App.tsx"],
        )

        self.assertIn("web-app", result["recommended_command_groups"])

    def test_maui_doctor_is_recommended_only_for_mobile_scope(self):
        generic = recommend_command_groups(
            issue_text="Fix backend validation.",
            changed_paths=["phoodab/apps/api/Program.cs"],
        )
        mobile = recommend_command_groups(
            issue_text="Fix Android emulator startup for the MAUI mobile app.",
            changed_paths=["phoodab/apps/mobile/MainPage.xaml"],
        )

        self.assertNotIn("maui-android-doctor", generic["recommended_command_groups"])
        self.assertIn("maui-android-doctor", mobile["recommended_command_groups"])

    def test_maui_build_requires_mobile_scope_and_android_availability(self):
        missing_android = recommend_command_groups(
            issue_text="Fix MAUI mobile build.",
            changed_paths=["phoodab/apps/mobile/PHOODAB.Mobile.csproj"],
            android_sdk_available=False,
        )
        with_android = recommend_command_groups(
            issue_text="Fix MAUI mobile build.",
            changed_paths=["phoodab/apps/mobile/PHOODAB.Mobile.csproj"],
            android_sdk_available=True,
        )

        self.assertNotIn("maui-android-build", missing_android["recommended_command_groups"])
        self.assertIn("maui-android-build", with_android["recommended_command_groups"])

    def test_ci_manual_reference_remains_conditional_reference_only(self):
        result = recommend_command_groups(
            issue_text="Inspect remote CI state for this PR.",
            changed_paths=[],
        )

        self.assertIn("ci-manual-reference", result["available_command_groups"])
        self.assertIn("ci-manual-reference", result["conditional_command_groups"])
        self.assertNotIn("ci-manual-reference", result["recommended_command_groups"])


if __name__ == "__main__":
    unittest.main()
