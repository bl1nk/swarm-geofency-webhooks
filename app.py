from flask import Flask, request
import json
import foursquare
import ConfigParser

app = Flask(__name__)

config = ConfigParser.SafeConfigParser()
config.read('config.ini')


@app.route('/', methods=['POST', 'GET'])
def hi():
    client_id = config.get('foursquare', 'client_id')
    client_secret = config.get('foursquare', 'client_secret')
    redirect_uri = config.get('foursquare', 'redirect_uri')
    client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    if request.method == 'POST':
        data = json.loads(request.data)
        if data.get(u'device') == config.get('geofency', 'device_name'):
            access_code = config.get('foursquare', 'access_code')
            client.set_access_token(client.oauth.get_token(access_code))

            location = data.get(u'name')
            if config.get('venues', location):
                client.checkins.add(params={'venueId': config.get('venues', location)})
                return "OK"
    else:
        return "<a href=\"%s\"><h1>DO THE OAUTH</h1></a>" % client.oauth.auth_url()


@app.route('/oauth2/authorize', methods=['GET'])
def oauth_authorize():
    code = request.args.get('code')
    config.set('foursquare', 'access_code', code)
    with open('config.ini', 'wb') as cfg:
        config.write(cfg)
    return "done, set up your webhook now"


@app.route("/debug", methods=['POST'])
def test():
    data = json.loads(request.data)
    print data
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
