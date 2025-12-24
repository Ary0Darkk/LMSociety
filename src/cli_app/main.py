import click

@click.group()
def lms():
    pass

@click.command(name="say_hello")
@click.option('--name',prompt="Enter your name",help="Name of person",required=True)
def say_hello(name:str):
    click.echo(f'Hello {name}!')


@click.command(name="say_welcome")
@click.option('--name',prompt="Enter your name",help="Name of person",required=True)
def say_wlcm(name:str):
    click.echo(f'Welcome, {name}!')


# group cmds
lms.add_command(say_hello)
lms.add_command(say_wlcm)

if __name__ == "__main__":
    lms()