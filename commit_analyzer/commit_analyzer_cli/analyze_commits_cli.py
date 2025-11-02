import requests
import typer
from typing_extensions import Annotated
from datetime import datetime
from rich import print as rprint
import pprint

app = typer.Typer()
pp = pprint.PrettyPrinter(indent=4)


@app.command()
def summarize_commits(
    ctx: typer.Context,
    url: Annotated[str, typer.Argument()],
    repo_name: Annotated[str, typer.Option("--repo-name", "-rn")],
    repo_owner: Annotated[str, typer.Option("--repo-owner", "-ro")],
):

    repo_url = f"{url}{repo_owner}/{repo_name}/commits?per_page=100"

    response = requests.get(repo_url)
    response_json = response.json()
    # pp.pprint(response_json[0])
    commits = []
    for obj in response_json:
        commit = {
            "date": datetime.strptime(
                obj["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
            ),
            "message": obj["commit"]["message"],
            "author": obj["commit"]["author"]["name"],
            "month_year": datetime.strptime(
                obj["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%m-%Y"),
        }
        commits.append(commit)

    pp.pprint(len(commits))


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    message = f"""
    [bold]-------------------------------------------[/bold]
    application message
    [bold]-------------------------------------------[/bold]
    """

    if ctx.invoked_subcommand is None:
        rprint(message)
        raise typer.Exit()


if __name__ == "__main__":
    app()
