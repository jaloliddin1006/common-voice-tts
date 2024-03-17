let isRecording = false;
let mediaRecorder;
let audioChunks = [];
const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

const sentence = document.querySelector("#sentence");
const sentence_id = document.querySelector("#sentence_id");
const startStopBtn = document.querySelector("#startStopBtn");

startStopBtn.addEventListener('click', function() {
    isRecording = !isRecording;
    if (isRecording) {
        startRecording();
        startStopBtn.innerHTML = 'Stop';
    } else {
        stopRecording();
        startStopBtn.innerHTML = 'Start';
    }
});

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true, video:false })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });
            mediaRecorder.start();
        });
}

function stopRecording() {
    mediaRecorder.addEventListener('stop', (stream) => {
        if (audioChunks.length === 0) {
            console.error('Audio fayl bo\'shligi sababli to\'xtadi!');
            return;
        }
        const audioBlob = new Blob(audioChunks, { 'type': 'audio/wav; codecs=opus' });
        sendAudioToServer(audioBlob);
        audioChunks = [];
    });

    if (mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }

    mediaRecorder.stop();
    
}

function sendAudioToServer(blob) {
    const formData = new FormData();
    formData.append('sentence_id', sentence_id.value);
    formData.append('sentence', sentence.innerHTML);
    formData.append('audio_file', blob, 'recorded_audio.wav');

    fetch('/save-voice/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        sentence.innerHTML = data.sentence;
        sentence_id.value = data.sentence_id;
    })
    .catch(error => {
        console.error(error);
    });
}
