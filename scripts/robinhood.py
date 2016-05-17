import click
import requests

class Robinhood:

    api_base = 'https://api.robinhood.com'

    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        pass

    def get_quote(self, symbol):
        url = '%s/quotes/%s/' % (self.api_base, symbol.strip().upper())
        r = self.session.get(url)
        return r.json()

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Robinhood()

@cli.command()
@click.argument('symbol')
@click.pass_obj
def quote(robinhood, symbol):
    r = robinhood.get_quote(symbol)
    price = float(r['last_trade_price'])
    previous_close = float(r['previous_close'])
    pct_change = (price - previous_close) / previous_close * 100
    sign = '+' if pct_change > 0 else '-'
    click.echo('Symbol: %s' % r['symbol'])
    click.echo('Price: %.2f' % price)
    click.echo('Percent Change: %s%.2f%%' % (sign, pct_change))

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
