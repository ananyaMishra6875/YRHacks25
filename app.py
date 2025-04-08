from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# temporarily store journal entries in memory --> add sql?
entries = []

@app.route('/')
def home():
    # home page to submit journal entry
    return render_template('home.html')

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

    # redirect to journal page after saving entry
    return redirect(url_for('journal'))

@app.route('/journal')
def journal():
    # The journal page will display all the saved entries
    return render_template('journal.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)