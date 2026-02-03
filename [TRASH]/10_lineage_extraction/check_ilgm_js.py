import boto3

s3 = boto3.client('s3')
key = 'html/0017fbd840f2539f.html'
js_key = key.replace('html/', 'html_js/').replace('.html', '_js.html')

try:
    s3.head_object(Bucket='ci-strains-html-archive', Key=js_key)
    print(f'JS version exists: {js_key}')
except:
    print(f'No JS version, using: {key}')
