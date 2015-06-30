from flask import Flask, request
import foursquare
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')


@app.route('/', methods=['POST', 'GET'])
def hi():
    client_id = config.get('foursquare', 'client_id')
    client_secret = config.get('foursquare', 'client_secret')
    redirect_uri = config.get('foursquare', 'redirect_uri')
    client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    if request.method == 'POST':
        device = request.form.get('device')
        location = request.form.get('name')

        if config.has_section(device):
            client.set_access_token(client.oauth.get_token(config.get('foursquare', 'access_code')))
            if config.has_option(device, location):
                client.checkins.add(params={'venueId': config.get(device, location)})
                return "OK"

    else:
        if config.has_option('foursquare', 'access_code'):
            return "nope"
        return "<a href=\"%s\"><h1>DO THE OAUTH</h1></a>" % client.oauth.auth_url()


@app.route('/oauth2/authorize', methods=['GET'])
def oauth_authorize():
    code = request.args.get('code')
    config.set('foursquare', 'access_code', code)
    with open('config.ini', 'w') as cfg:
        config.write(cfg)
    return "done, set up your webhook now"


@app.route("/debug", methods=['POST'])
def debug():
    print(request.form)
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
