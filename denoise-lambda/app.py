import boto3
from chalice import Chalice


app = Chalice(app_name='denoise-lambda')
s3 = boto3.client('s3')

_SUPPORTED_IMAGE_EXTENSIONS = (
    '.jpg',
    '.png',
)

@app.route('/')
def index():
    return {'status_code': 200,
            'message': 'welcome to test API'}

@app.route('/upload/{file_name}', methods=['POST'], content_types=['image/png'], cors=True)
def upload_to_s3(file_name):
    try:
        body = app.current_request.raw_body
        temp_file = '/tmp/' + file_name
        with open(temp_file, 'wb') as f:
            f.write(body)
        s3.upload_file(temp_file, 'imagebucket940127', file_name)

        return { 'file_name': 'https://imagebucket940127.s3.ca-central-1.amazonaws.com/' + file_name }
    except Exception:
        raise ChaliceViewError('something went wrong')

@app.on_s3_event(bucket='imagebucket940127',
events=['s3:ObjectCreated:*'])
def react_to_s3_upload(event):
    if _is_image(event.key):
        _handle_created_image(bucket=event.bucket, key=event.key)

def _is_image(key):
    return key.endswith(_SUPPORTED_IMAGE_EXTENSIONS)

def _handle_created_image(bucket, key):
    obj = s3.download_file(bucket, key, "/tmp/temp.png")










# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
