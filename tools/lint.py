import subprocess


def lint() -> None:
    subprocess.run(["black", "./src", "tests/unit"])
    subprocess.run(["isort", "./src", "./tests/unit"])
    subprocess.run([
        "flake8", "--config", "./flake8.cfg", "./src", "./tests/unit"
    ])
    subprocess.run(["mypy", "./src", "tests/unit"])
