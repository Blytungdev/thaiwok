# & Thai Wok
Semi-automatic python script for uploading measurement data to google sheets

## Requirements:
- `config.json`, configuration JSON, with the following format:

```
{
    "ssh_user": "pi",
    "ssh_host": "teletornet.amcoff.net",
    "ssh_keypath": "/home/melvinj/.ssh/id_rsa",
    "ssh_port": "2200",

    "remote_script": "measurement.py",

    "credentials": "credentials.json",
    "sheet_id": "17cL8tHRxyToATZ-PO8TtvV3WyDqKIIdBx74Vo3DPxpw",
    "worksheet_name": "Blad1"
}
```

- `credentials.json`, or similar. Google Credentials for the service account inputing into the google sheet
