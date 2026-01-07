import click
from click_shell import shell

message = """
Welcome to LLMs World, watch how society of llms evolve over time!
"""


@shell(prompt="lmsociety/> ", intro=message)
def lmsociety():
    """Main entry point for lms."""
    pass


@lmsociety.command()
@click.option("--name", prompt="Enter your name ", help="Name of person", required=True)
def say_hello(name: str):
    click.echo(f"Hello {name}!")


@lmsociety.command()
def say_wlcm():
    click.echo("Welcome to the society!")


if __name__ == "__main__":
    lmsociety()
