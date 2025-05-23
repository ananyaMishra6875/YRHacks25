from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

# temporarily store journal entries in memory --> add sql?
entries = []

@app.route('/')
def home():
    # home page to submit journal entry
    return render_template('home.html')

@app.route('/data')
def get_data():
    mood_data = []
    for i in range(0, len(entries)):
        mood_data.append(int(entries[i]['mood']))
    # when users submits the form, this route will handle the data
    # mood = request.form['mood']  # get the selected mood
    # if(mood == 'ecstatic'):
    # mood_data.append(12)
    # # elif(mood == 'happy'):
    # mood_data.append(9)
    # # elif(mood == 'neutral'):
    # mood_data.append(6)
    # # elif(mood == 'sad'):
    # mood_data.append(3)
    # # elif(mood == 'depressed'):
    # mood_data.append(0)
    # # print(mood_data)

    depressedCount = 0
    for mood in mood_data:
        if (mood <= 5):
            depressedCount+=1
    notDepressedCount = len(mood_data) - depressedCount
    doughnut_data = [notDepressedCount, depressedCount]
    doughnut_labels = ["Not Depressed", "Depressed"]
    return jsonify({
        "mood_data": mood_data,
        "doughnut_data": doughnut_data,
        "doughnut_labels": doughnut_labels,
    })

@app.route('/submit', methods=['POST'])
def submit_entry():
    # when users submits the form, this route will handle the data
    mood = request.form['mood']  # get the selected mood
    tags = request.form['tags']  # get optional tags
    journal = request.form['journal']  # get the journal entry text

    # Store the entry (for now, we're just appending to an in-memory list)
    entries.append({
        'mood': mood,
        'tags': tags,
        'journal': journal
    })

    color_map = {
        'ecstatic': 'mood-ecstatic',
        'happy': 'mood-happy',
        'neutral': 'mood-neutral',
        'sad': 'mood-sad',
        'depressed': 'mood-depressed'
    }

    mood_class = color_map.get(mood, '')

    # redirect to journal page after saving entry
    return render_template('journal.html', entries=entries, mood_class=mood_class)

@app.route('/journal')
def journal():
    # The journal page will display all the saved entries
    return render_template('journal.html', entries=entries, mood_class=None)

@app.route('/entry')
def entry():
    # The entry page will allow users to write an entry
    return render_template('entry.html')

@app.route('/graph')
def graph():
    # The graph page will allow users to view a progress graph analysis of their entries
    return render_template('graph.html')

@app.route('/settings')
def settings():
    # The settings page will display the settings for the app
    return render_template('settings.html')

    name = request.form['name']
    email = request.form['email'] 
    comment = request.form['comment'] 

    entries.append({
        'name': name,
        'email': email,
        'comment': comment
    })

@app.route('/submit', methods=['POST'])
def submit_entry2():
    audio_file = request.files.get('audio')
    video_file = request.files.get('video')

    if audio_file:
        audio_path = os.path.join('static/uploads', audio_file.filename)
        audio_file.save(audio_path)

    if video_file:
        video_path = os.path.join('static/uploads', video_file.filename)
        video_file.save(video_path)

    # process/save form data too
    return "Entry submitted."

if __name__ == '__main__':
    app.run(debug=True)