from flask import Flask, request
import json
import foursquare
import ConfigParser

app = Flask(__name__)

config = ConfigParser.SafeConfigParser()
config.read('config.ini')


@app.route('/', methods=['POST', 'GET'])
def hi():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data.get(u'device') == config.get('geofency', 'device_name'):
            checkin(data.get(u'name'))
            return "OK"

    else:
        client_id = config.get('foursquare', 'client_id')
        client_secret = config.get('foursquare', 'client_secret')
        redirect_uri = config.get('foursquare', 'redirect_uri')

        client = foursquare.Foursquare(client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)

        auth_uri = client.oauth.auth_url()
        print "Open: %s" % auth_uri


@app.route('/oauth2/authorize', methods=['GET'])
def oauth_authorize():
    code = request.args.get('code')
    config.set('foursquare', 'access_code', code)
    with open('config.ini', 'wb') as cfg:
        config.write(cfg)
    return code


def checkin(loc):
    client_id = config.get('foursquare', 'client_id')
    client_secret = config.get('foursquare', 'client_secret')
    redirect_uri = config.get('foursquare', 'redirect_uri')
    access_code = config.get('foursquare', 'access_code')

    client = foursquare.Foursquare(client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
    access_token = client.oauth.get_token(access_code)
    client.set_access_token(access_token)

    # if loc == "test":
    #     client.checkins.add(params={'venueId': '5556ff71498ede07439e5d24'})

    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
