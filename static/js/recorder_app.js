class VoiceRecorder {
	constructor() {
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			console.log("getUserMedia supported")
		} else {
			console.log("getUserMedia is not supported on your browser!")
		}

		this.mediaRecorder
		this.stream
		this.chunks = []
		this.isRecording = false

		this.recorderRef = document.querySelector("#recorder")
		this.playerRef = document.querySelector("#player")
		this.startStopBtn = document.querySelector("#startStopBtn")
		this.sentence = document.querySelector("#sentence")
		this.sentence_id = document.querySelector("#sentence_id")
		// this.startRef = document.querySelector("#start")
		// this.stopRef = document.querySelector("#stop")
		
		// this.startRef.onclick = this.startRecording.bind(this)
		// this.stopRef.onclick = this.stopRecording.bind(this)

        this.startStopBtn.onclick = () => {
            if (this.isRecording) {
                this.stopRecording()
            } else {
                this.startRecording()
            }
        }

		this.constraints = {
			audio: true,
			video: false
		}
		
	}

	handleSuccess(stream) {
		this.stream = stream
		this.stream.oninactive = () => {
			console.log("Stream ended!")
		};
		this.recorderRef.srcObject = this.stream
		this.mediaRecorder = new MediaRecorder(this.stream)
		console.log(this.mediaRecorder)
		this.mediaRecorder.ondataavailable = this.onMediaRecorderDataAvailable.bind(this)
		this.mediaRecorder.onstop = this.onMediaRecorderStop.bind(this)
		this.recorderRef.play()
		this.mediaRecorder.start()
	}

	handleError(error) {
		console.log("navigator.getUserMedia error: ", error)
	}
	
	onMediaRecorderDataAvailable(e) { this.chunks.push(e.data) }
	
	onMediaRecorderStop(e) { 
			const blob = new Blob(this.chunks, { 'type': 'audio/wav; codecs=opus' })
			const audioURL = window.URL.createObjectURL(blob)
			this.playerRef.src = audioURL
			this.chunks = []
			this.stream.getAudioTracks().forEach(track => track.stop())
			this.stream = null
	}

	startRecording() {
		if (this.isRecording) return
		this.isRecording = true
		this.startStopBtn.innerHTML = 'Recording...'
		this.playerRef.src = ''
		navigator.mediaDevices
			.getUserMedia(this.constraints)
			.then(this.handleSuccess.bind(this))
			.catch(this.handleError.bind(this))
	}
	
	stopRecording() {
		if (!this.isRecording) return;
		this.isRecording = false;
		this.startStopBtn.innerHTML = 'Record';
		this.recorderRef.pause();
		this.mediaRecorder.stop();
	
		const formData = new FormData();
		const blob = new Blob(this.chunks, { 'type': 'audio/wav; codecs=opus' });
		formData.append('audio', blob, 'recording.wav');
		formData.append('sentence', this.sentence.value);
		formData.append('sentence_id', this.sentence_id.value);

		const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
		
		// Yuborish uchun POST so'rovi
		fetch('/save-voice/', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken
			},
			body: formData
		})
		.then(response => {
			console.log(response);
			if (response.ok) {
				console.log(response);
				console.log('Audio muvaffaqiyatli yuborildi');
				response.json().then(data => {
					console.log(data);
					this.sentence.innerHTML = data.sentence;
					this.sentence_id.value = data.sentence_id;
				});

			} 
			else if (response.status === 401) {
				response.json().then(data => {
					window.open(data.url, "_self");
				});
			}
			else {
				console.error('Audio yuborishda xatolik yuz berdi');
				window.open(response.json().url, "_self");
			}
		})
		.catch(error => {
			console.error('Audio yuborishda xatolik:', error);
		})
		.finally(() => {
			this.chunks = [];
		});
	}
	
	
	
}

window.voiceRecorder = new VoiceRecorder()
