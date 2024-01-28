from flask import Blueprint, current_app, redirect, render_template, request, flash, jsonify, send_file, url_for
from flask_login import login_required, current_user
from .models import Note, Recording, User
from sqlalchemy.sql import func
from . import db
import json
import pyaudio
import wave
import os


views = Blueprint('views', __name__)

# ------------Profile--------------#

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

from werkzeug.security import generate_password_hash, check_password_hash

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Check if a new password is provided
        new_password = request.form.get('password')
        if new_password:
            # Check if the provided current password matches the stored hash
            current_password = request.form['current_password']
            if check_password_hash(current_user.password, current_password):

                current_user.email = request.form['email']
                current_user.user_name = request.form['username']

                # If the current password is correct, proceed with changing the password
                hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                # Update the user's password in the database
                current_user.password = hashed_new_password
                # flash('Updated successfully!', 'success')
            else:
                # If the current password is incorrect, show an error message
                flash('Incorrect current password. Update failed!.', 'error')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.profile'))

    return render_template('edit_profile.html', user=current_user)



# ------------Pages--------------#

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note_text = request.form.get("note")
        if len(note_text) > 0:
            new_note = Note(data=note_text, user=current_user)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user)


# ------------Note--------------#

from datetime import datetime

@views.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    if request.method == 'POST':
        note_text = request.form.get('note')
        if len(note_text) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note_text, user_id=current_user.id, date=datetime.now())
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('Notes.html', user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

@views.route('/delete-notes', methods=['POST'])
def delete_notes():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})


#---updating note from the Note page  -----


@views.route('/update-note/<int:note_id>', methods=['POST'])
@login_required
def update_note(note_id):
    if request.method == 'POST':
        note_text = request.form.get('update-note')

        existing_note = Note.query.get(note_id)

        if existing_note and existing_note.user_id == current_user.id:
            existing_note.data = note_text
            existing_note.date = func.now()

            db.session.commit()
            flash('Note updated!', category='success')
        else:
            flash('Note not found or you do not have permission!', category='error')

    return redirect(url_for('views.note'))



#--- updating from the home page -----


@views.route('/update-notes/<int:note_id>', methods=['POST'])
@login_required
def update_notes(note_id):
    if request.method == 'POST':
        note_text = request.form.get('update-notes')

        existing_note = Note.query.get(note_id)

        if existing_note and existing_note.user_id == current_user.id:
            existing_note.data = note_text
            existing_note.date = func.now()

            db.session.commit()
            flash('Note updated!', category='success')
        else:
            flash('Note not found or you do not have permission!', category='error')

    return redirect(url_for('views.home'))




#---------Voice-----------#

@views.route('/voice', methods=['POST', 'GET'])
@login_required
def voice():
    user_recordings = Recording.query.filter_by(user_id=current_user.id).all()
    return render_template('Voice.html', user=current_user, recordings=user_recordings)
    

UPLOAD_FOLDER = 'uploads'

def get_next_filename(user_id):
    i = 1
    while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], f'user_{user_id}_Note_{i}.wav')):
        i += 1
    return f'user_{user_id}_Note_{i}.wav'

@views.route('/record', methods=['POST'])
def record():
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
        frames = []

        for i in range(0, int(44100 / 1024 * 5)):
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        user_id = current_user.id if current_user.is_authenticated else None
        filename = get_next_filename(user_id)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        wf = wave.open(filepath, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

  #      Save the recording information to the database
        recording = Recording(user_id=user_id, filename=filename)
        db.session.add(recording)
        db.session.commit()

        return jsonify({'message': 'Recording complete', 'filename': filename},render_template(url_for('views.voice')))
    except Exception as e:
        print(f"Error recording: {e}")
        return jsonify({'error': 'Error recording'}), 500

from datetime import datetime
import pytz

@views.route('/play/<filename>')
@login_required
def play():
    try:
        user_id = current_user.id
        # path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'user_{user_id}_{filename}')
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], get_next_filename(user_id))

        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500


# @views.route('/play/<filename>')
# @login_required
# def play():
#     data = json.loads(request.data)
#     recording_id= data['recordingId']
#     recording = Recording.query.get(recording_id)
#     if recording and recording.user_id == current_user.id:
#         file_path = os.path.join(current_app.config['UPLOAD_FORDER'], recording.filename)
#         return (file_path)

# --- deleting Voice Note------
    
@views.route('/delete-voice', methods=['POST'])
def delete_voice():
    data = json.loads(request.data)
    recording_id = data['recordingId']
    recording = Recording.query.get(recording_id)
    
    if recording and recording.user_id == current_user.id:
        # Delete the associated audio file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], recording.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        # Delete the database entry
        db.session.delete(recording)
        db.session.commit()

        return jsonify({'message': 'Recording deleted successfully'})
    else:
        return jsonify({'error': 'Unable to delete recording'}), 400

