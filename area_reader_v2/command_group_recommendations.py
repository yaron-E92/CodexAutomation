from __future__ import annotations

from collections.abc import Iterable

DEFAULT_RECOMMENDED_COMMAND_GROUPS = [
    "env",
    "dotnet-solution",
    "node-root",
    "markdown-smoke",
]

CONDITIONAL_COMMAND_GROUPS = {
    "api-client-generate": "Run if API/OpenAPI/client generation is touched.",
    "web-app": "Run for web-specific issues or if root scripts are insufficient.",
    "maui-android-doctor": "Run for MAUI/mobile issues or explicit mobile verification.",
    "maui-android-build": "Run for MAUI/mobile issues when Android SDK is available.",
    "ci-manual-reference": "Reference only; do not run by default.",
}

ALL_COMMAND_GROUPS = [
    *DEFAULT_RECOMMENDED_COMMAND_GROUPS,
    *CONDITIONAL_COMMAND_GROUPS.keys(),
]

API_CLIENT_TERMS = (
    "api client generation",
    "openapi",
    "swagger",
    "generated client",
    "api contract",
    "api contracts",
    "typescript client",
)

WEB_TERMS = (
    "react",
    "vite",
    "ui",
    "frontend",
    "browser",
    "component",
    "web shell",
)

MAUI_TERMS = (
    "maui",
    "android",
    "mobile",
    "emulator",
    "device",
    "xaml",
    "mobile build",
)

API_CONTRACT_PATH_MARKERS = (
    "openapi",
    "swagger",
    "api-contract",
    "api_contract",
    "contracts",
    "generated",
)


def recommend_command_groups(
    *,
    issue_text: str,
    changed_paths: Iterable[str],
    web_build_errors: str = "",
    root_node_scripts_sufficient: bool = True,
    android_sdk_available: bool = False,
    user_requested_mobile_verification: bool = False,
) -> dict[str, object]:
    """Return JSON-ready command-group metadata for area-reader v2 output."""

    normalized_issue = issue_text.casefold()
    normalized_web_errors = web_build_errors.casefold()
    normalized_paths = tuple(path.replace("\\", "/").casefold() for path in changed_paths)

    recommended = list(DEFAULT_RECOMMENDED_COMMAND_GROUPS)

    if _api_client_relevant(normalized_issue, normalized_web_errors, normalized_paths):
        recommended.append("api-client-generate")

    if _web_relevant(normalized_issue, normalized_paths, root_node_scripts_sufficient):
        recommended.append("web-app")

    maui_relevant = _maui_relevant(
        normalized_issue,
        normalized_paths,
        user_requested_mobile_verification,
    )
    if maui_relevant:
        recommended.append("maui-android-doctor")

    if maui_relevant and android_sdk_available:
        recommended.append("maui-android-build")

    return {
        "available_command_groups": list(ALL_COMMAND_GROUPS),
        "recommended_command_groups": recommended,
        "conditional_command_groups": dict(CONDITIONAL_COMMAND_GROUPS),
    }


def _api_client_relevant(
    issue_text: str,
    web_build_errors: str,
    changed_paths: Iterable[str],
) -> bool:
    if _contains_any(issue_text, API_CLIENT_TERMS):
        return True

    if _contains_any(web_build_errors, ("generated api client", "stale generated", "missing generated")):
        return True

    return any(_is_api_contract_path(path) for path in changed_paths)


def _web_relevant(
    issue_text: str,
    changed_paths: Iterable[str],
    root_node_scripts_sufficient: bool,
) -> bool:
    if any(path.startswith("phoodab/apps/web/") for path in changed_paths):
        return True

    if _contains_any(issue_text, WEB_TERMS):
        return True

    return not root_node_scripts_sufficient


def _maui_relevant(
    issue_text: str,
    changed_paths: Iterable[str],
    user_requested_mobile_verification: bool,
) -> bool:
    if user_requested_mobile_verification:
        return True

    if any(
        path.startswith("phoodab/apps/mobile/")
        or path.startswith("phoodab/apps/mobile-shared/")
        for path in changed_paths
    ):
        return True

    return _contains_any(issue_text, MAUI_TERMS)


def _is_api_contract_path(path: str) -> bool:
    if not (
        path.startswith("phoodab/apps/api/")
        or path.startswith("phoodab/packages/api-client/")
        or "/api/" in path
    ):
        return False

    return _contains_any(path, API_CONTRACT_PATH_MARKERS)


def _contains_any(value: str, terms: Iterable[str]) -> bool:
    return any(term in value for term in terms)
