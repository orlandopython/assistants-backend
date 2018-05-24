from flask import Flask, Response, jsonify
from flask_ask import Ask, statement
from flask_assistant import Assistant, tell
from flask_cors import CORS
import meetup_utils

app = Flask(__name__)

app.config['ASSIST_ACTIONS_ON_GOOGLE'] = True

cors = CORS(app)
assist = Assistant(app, route='/google')
ask = Ask(app, route='/alexa')

@app.route('/<group_name>')
def group_details(group_name: str) -> Response:
    """
    Returns general meetup group details
    """
    group = meetup_utils.get_group(group_name)
    return jsonify(meetup_utils.extract_details(group))


@app.route('/<group_name>/next')
def next_meetup_endpoint(group_name: str) -> Response:
    """
    Returns details on the next meetup for a group
    """
    group = meetup_utils.get_group(group_name)
    title, time, count = meetup_utils.next_meetup(group)
    return jsonify({'title': title, 'time': time, 'count': count})

@assist.action('member-count')
def google_member_count(meetup: str) -> tell:
    group = meetup_utils.get_group(meetup)
    details = meetup_utils.extract_details(group)
    speech_text = f"{details['name']} has {details['members']} {details['member_title']}"
    return tell(speech_text).card(
        title=details['name'],
        text=f"{details['members']} {details['member_title']}"
    )

@ask.intent('MemberCount', convert={'meetup': str})
def alexa_member_count(meetup: str) -> statement:
    group = meetup_utils.get_group(meetup)
    details = meetup_utils.extract_details(group)
    speech_text = f"{details['name']} has {details['members']} {details['member_title']}"
    return statement(speech_text).simple_card(
        title=details['name'],
        content=f"{details['members']} {details['member_title']}"
    )

if __name__ == '__main__':
    app.run('localhost', 8000)