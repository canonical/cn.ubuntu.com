import re
from pathlib import Path
from unittest import TestCase

from webapp.app import app
from webapp.api import get_releases


class TestReleasesYamlReferences(TestCase):
    """
    Validates that all `releases.X` references in templates
    correspond to actual fields in releases.yaml
    """

    @classmethod
    def setUpClass(cls):

        with app.app_context():
            releases_url = app.config["UBUNTU_COM_RELEASES"]
            cls.releases_data = get_releases(releases_url)

        cls.valid_paths = set()
        cls._build_paths(cls.releases_data, "releases", cls.valid_paths)

        cls.project_root = Path(__file__).parent.parent

    @classmethod
    def _build_paths(cls, data, prefix, paths):
        """Builds a list of valid paths from the releases.yaml"""
        paths.add(prefix)
        if isinstance(data, dict):
            for key, value in data.items():
                cls._build_paths(value, f"{prefix}.{key}", paths)

    def _find_template_files(self):
        templates_dir = self.project_root / "templates"
        return list(templates_dir.rglob("*.html"))

    def _extract_releases_references(self, content, pattern):
        """Extract all releases.X.Y.Z references from within Jinja tags."""
        jinja_blocks = re.findall(
            r"\{[\{\%](.*?)[\}\%]\}", content, flags=re.DOTALL
        )

        references = []
        for block in jinja_blocks:
            matches = pattern.findall(block)
            for match in matches:
                path = re.sub(r"[\s\|\}\)\]\,\:\;]+$", "", match)
                path = re.sub(r"\[.*$", "", path)
                if path:
                    references.append(f"releases.{path}")
        return references

    def test_template_references_exist(self):
        """
        Test that all releases references in html exist in releases.yaml
        """
        pattern = re.compile(r"releases\.([a-zA-Z0-9_\.]+)")

        # Add any false positives you want to ignore here
        ignored_refs = {"releases.ubuntu.com"}

        template_files = self._find_template_files()

        for filepath in template_files:
            try:
                with open(
                    filepath, "r", encoding="utf-8", errors="ignore"
                ) as f:
                    content = f.read()
            except Exception:
                continue

            refs = self._extract_releases_references(content, pattern)
            relative_path = filepath.relative_to(self.project_root)

            for ref in refs:
                # Skip the reference if it's in our ignore list
                if ref in ignored_refs:
                    continue

                with self.subTest(file=str(relative_path), reference=ref):
                    self.assertTrue(
                        ref in self.valid_paths,
                        f"'{ref}' not found in releases.yaml "
                        f"(file: {relative_path})",
                    )
