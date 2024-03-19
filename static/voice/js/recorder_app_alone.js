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
             
        showLoader();
        hideContent();

        stopRecording();
        startStopBtn.innerHTML = 'Start';
            
        }
    
        showContent();
        hideLoader();
   
});

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true, video:false })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });
            mediaRecorder.start();
        })
        .catch(error => {
            console.error('Audio yozish uchun xatolik:', error);
        });
}


function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.addEventListener('stop', () => {
            if (audioChunks.length === 0) {
                console.error('Audio fayl bo\'shligi sababli to\'xtadi!');
                return;
            }
            const audioBlob = new Blob(audioChunks, { 'type': 'audio/wav' }); // Mime tipini tekshirib oling
            sendAudioToServer(audioBlob);
            audioChunks = [];
        });

        mediaRecorder.stop();
    }
}


function sendAudioToServer(blob) {
    const formData = new FormData();
    formData.append('sentence_id', sentence_id.value);
    formData.append('sentence', sentence.textContent);
    formData.append('audio_file', blob, 'recorded_audio.wav');
    // console.log(sentence.textContent);
    // console.log(sentence_id.value);
    // console.log(blob);     
    //  console.log(formData);
    fetch('/save-voice/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            response.json().then(data => {
                sentence.textContent = data.sentence;
                sentence_modal.textContent = data.sentence;
                sentence_id.value = data.sentence_id;
            });
        } else if (response.status === 401) {
            console.error("Tizimga kirishni tekshiring");
            alert("Tizimga kirishni tekshiring");
            response.json().then(data => {
                window.open(data.url, "_self");
            });
        }
        else {
            console.error("Next sentence error......");
            alert("Tizimga kirishni tekshiring");
            // window.open(response.json().url, "_self");
        }
    })
    .catch(error => {
        console.error("Next sentence error::::", error);
    });
}