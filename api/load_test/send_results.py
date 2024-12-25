#!/tools/python/3.12.0/bin/python

from datetime import datetime
import requests
import sys, json, os

send_to = 'dano@xsightlabs.com'
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

log_fn = 'locust.log'
report_fn = 'locust_report.html'
config_fn = 'locust.conf'

save_to = '/projects/common/home/dano/locust_reports'

# files_src  = [ os.path.join(os.getcwd(), file) for file in [report_fn, config_fn] ]
# files_dest = [ os.path.join(save_to, file) for file in [report_fn, config_fn] ]


files = [ os.path.join(os.getcwd(), file) for file in [report_fn, config_fn]]

with open(log_fn, 'r') as f:
    log = f.read()
    f.close()
with open(config_fn, 'r') as f:
    config = f.read()
    f.close()

host = 'http://x-flask:2222'
route = 'send_mail'
url = f'{host}/{route}'

data = {
    'to': [send_to],
    'subject': f'Locust report for {date}',
    'body': f'Locust config:\n\n{config}\n\nLocust logs:\n\n{log}', 
    'sender': 'simba',
    'files': files
}

response = requests.post(url, json=json.dumps(data)).json()

success = response.get('mail_sent', False)

print(f"Mail sent to {send_to}: {success}")

if success:
    with open(log_fn, 'w') as f:
        f.write('')
        f.close()

sys.exit(0)