from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# temporarily store journal entries in memory --> add sql?
entries = []
dynamic_array = [10,2,8,0,4] #for graph testing

@app.route('/')
def home():
    # home page to submit journal entry
    return render_template('home.html')

@app.route('/data')
def get_data():
    return jsonify(dynamic_array)

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

if __name__ == '__main__':
    app.run(debug=True)