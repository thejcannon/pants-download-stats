import subprocess
import github
import json
import pathlib
from datetime import datetime

def _github():
    token = subprocess.run(
        ["gh", "auth", "token"], check=True, text=True, capture_output=True
    ).stdout.strip()
    return github.Github(auth=github.Auth.Token(token))


def main():
    gh = _github()
    repo = gh.get_repo("pantsbuild/pants")
    stats = {}
    for release in repo.get_releases():
        if not release.tag_name.startswith("release_2"):
            continue
        stats[release.tag_name] = {}
        for asset in release.get_assets():
            download_count = asset.download_count
            stats[release.tag_name][asset.name] = download_count

    datadir = pathlib.Path("data")
    datadir.mkdir(exist_ok=True)
    (datadir / f"{datetime.now().strftime('%Y-%m-%d')}.json").write_text(json.dumps(stats))


if __name__ == "__main__":
    main()
