import click


@click.group()
def cli():
    pass

@cli.command()
def quote():
    pass

@cli.command()
def portfolio():
    pass

@cli.command()
def order():
    pass

@cli.command()
def buy():
    pass

@cli.command()
def sell():
    pass


