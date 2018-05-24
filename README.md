# assistants-backend
Flask backend supporting Alexa and Google Assistant from VUI presentations

## Setup

```bash
pip install -r requirements.txt
```

You'll also need a valid Meetup API key in `meetup_utils.md` to run. You can grab one from the Meetup developer portal.

## Running

```bash
python app.py
```

You'll need to use a service like `ngrok` to make the API visible to the voice assistants.