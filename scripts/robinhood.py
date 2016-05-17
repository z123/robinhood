import click
import os
import pickle
import requests

class Robinhood:

    api_base = 'https://api.robinhood.com'
    token = None
    account = None
    authenticated = False

    def __init__(self, config_file):
            self.session = requests.Session()
            self.config_file = config_file

    def login(self, username, password):
        url = '%s/api-token-auth/' % (self.api_base)
        data = {
            'username': username,
            'password': password
        }
        r = self.session.post(url, data=data)
        r = r.json()
        if 'token' in r:
            self.token = r['token']
            self.session.headers['Authorization'] = 'Token %s' % (self.token)
            self.account = self.get_account()
            self.authenticated = True
            self.save()
            return True
        else:
            return False

    @property
    def is_authenticated(self):
        return self.authenticated

    def get_account(self):
        url = '%s/accounts/' % (self.api_base)
        r = self.session.get(url)
        return r.json()['results'][0]['account_number']

    def get_portfolio(self):
        url = '%s/portfolios/%s/' % (self.api_base, self.account)
        r = self.session.get(url)
        return r.json()

    def get_quote(self, symbol):
        url = '%s/quotes/%s/' % (self.api_base, symbol.strip().upper())
        r = self.session.get(url)
        return r.json()

    def save(self):
        pickle.dump(self, open(config_file, 'wb'))


def login(robinhood):
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    if not robinhood.login(username, password):
        click.echo('Bad credentials, please try again.')
        return False
    return True

@click.group()
@click.pass_context
def cli(ctx):
    config_file = os.path.join(os.path.dirname(__file__),
                               'robinhood.pkl')
    if os.path.isfile(config_file):
        ctx.obj = pickle.load(open(config_file, 'rb'))
    else:
        ctx.obj = Robinhood(config_file)

@cli.command()
@click.argument('symbol')
@click.pass_obj
def quote(robinhood, symbol):
    r = robinhood.get_quote(symbol)
    price = float(r['last_trade_price'])
    previous_close = float(r['previous_close'])
    change = price - previous_close
    pct_change = change / previous_close * 100
    sign = '+' if pct_change > 0 else ''
    click.echo('Symbol: %s' % r['symbol'])
    click.echo('Price: ${:,.2f}'.format(price))
    click.echo('Change: {}${:,.2f} ({}{:,.2f}%)'.format(sign, change,
                                                        sign, pct_change))
@cli.command()
@click.pass_obj
def portfolio(robinhood):
    if robinhood.is_authenticated or login(robinhood):
        r = robinhood.get_portfolio()
        equity = float(r['equity'])
        previous_equity = float(r['equity_previous_close'])
        change = equity - previous_equity
        pct_change = change / previous_equity * 100
        sign = '+' if pct_change > 0 else ''
        click.echo('Portfolio Value: ${:,.2f}'.format(equity))
        click.echo('Change: {}${:,.2f} ({}{:,.2f}%)'.format(sign, change,
                                                            sign, pct_change))

@cli.command()
def order():
    pass

@cli.command()
def buy():
    pass

@cli.command()
def sell():
    pass
