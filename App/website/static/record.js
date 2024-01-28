// --- Delete Note ----

function DeleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/note";
  });
}
function DeleteNotes(noteId) {
  fetch("/delete-notes", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


  // update note from Note page

function UpdateNote(noteId) {
  const updateNoteForm = document.getElementById(`updateNoteForm-${noteId}`);
  updateNoteForm.action = `/update-note/${noteId}`;
  updateNoteForm.submit();
}

// update note from home page


function UpdateNotes(noteId) {
  const updateNoteForm = document.getElementById(`updateNoteForm-${noteId}`);
  updateNoteForm.action = `/update-notes/${noteId}`;
  updateNoteForm.submit();
}



document.addEventListener("DOMContentLoaded", function () {
  const noteForm = document.getElementById("noteForm");
  const noteTextarea = document.getElementById("note");

  noteTextarea.addEventListener("keyup", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault(); // Prevent the default newline insertion
      noteForm.submit();
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Your JavaScript code here
  const startRecordingButton = document.getElementById("start-recording");
  const stopRecordingButton = document.getElementById("stop-recording");
  // const recordingStatus = document.getElementById("recording-status");
  // const audioPlayer = document.getElementById("audio-player");
  let isRecording = false;
  let mediaRecorder;
  let chunks = [];
  let timerInterval;

  startRecordingButton.addEventListener("click", startRecording);
  stopRecordingButton.addEventListener("click", stopRecording);
  let recordingTimeInSeconds = 0;

  function updateTimer() {
    const minutes = Math.floor(recordingTimeInSeconds / 60);
    const seconds = recordingTimeInSeconds % 60;
    const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById("recording-time").innerText = formattedTime;
    recordingTimeInSeconds++;
  }

  function startRecording() {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        const options = { mimeType: "audio/webm" };
        mediaRecorder = new MediaRecorder(stream, options);
        chunks = [];

        mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            chunks.push(e.data);
          }
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(chunks, { type: "audio/webm" });

          // Send the recorded audio to the server
          uploadAudio(audioBlob);
          clearInterval(timerInterval);
        };

        mediaRecorder.start();
        isRecording = true;
        startRecordingButton.disabled = true;
        stopRecordingButton.disabled = false;
        // recordingStatus.innerText = "Recording...";

        // Update the timer every second
        updateTimer();
        timerInterval = setInterval(updateTimer, 1000);
      })
      .catch((error) => console.error("Error accessing microphone:", error));
  }

  function uploadAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob);

    fetch("/record", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        // Reload the page after added in uploads folders
        setTimeout(() => {
            location.reload();
          }, Math.floor(Math.random() * (400 - 0 + 0)) + 0);
        // Optionally, you can handle the response from the server
      })
      .catch((error) => console.error("Error uploading audio:", error));
  }

  function stopRecording() {
    if (isRecording) {
      mediaRecorder.stop();
      isRecording = false;
      startRecordingButton.disabled = false;
      stopRecordingButton.disabled = true;
      recordingStatus.innerText = "Recording stopped";
    }
  }
});

  // function updateTimer() {
  //   // Implement timer logic if needed
  // }

function deleteRecording(recordingId) {
  fetch("/delete-voice", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ recordingId: recordingId }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.message) {
        // Reload the page after a short delay (5 to 10 seconds)
        setTimeout(() => {
          location.reload();
        }, Math.floor(Math.random() * (3000 - 2000 + 1)) + 2000);
      } else {
        alert('Error deleting recording');
      }
    })
    .catch((error) => console.error("Error deleting recording:", error));
}





document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById('togglePassword');
  const toggleBtn = document.getElementById('togglesPassword');

  function togglePasswordVisibility(inputId, icon) {
      const passwordInput = document.getElementById(inputId);
      icon.addEventListener('click', function () {
          const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
          passwordInput.setAttribute('type', type);
          icon.classList.toggle('fa-eye-slash');
      });
  }

  togglePasswordVisibility('password', toggleButton);
  togglePasswordVisibility('current_password', toggleBtn);
});


