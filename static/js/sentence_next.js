const next_sentence_btn = document.querySelector("#nextSentenceBtn");
const sentence = document.querySelector("#sentence");
const sentence_modal = document.querySelector("#modal-sentence");
const sentence_id = document.querySelector("#sentence_id");
const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

next_sentence_btn.onclick = () => {

    const url = "/get_next_sentence/?sentence_id=" + encodeURIComponent(sentence_id.value);
    
    fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            response.json().then(data => {
                sentence.innerHTML = data.sentence;
                sentence_modal.innerHTML = data.sentence;
                sentence_id.value = data.sentence_id;
            });
        } else if (response.status === 401) {
            console.error("Tizimga kirishni tekshiring");
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
};
