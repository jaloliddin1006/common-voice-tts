var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


function ClearSelectedRadio() {
    const radioButtons = document.getElementsByName("selector");

    for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            radioButtons[i].checked = false;
            break;
        }
    }
}


// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
            modal.style.display = "none";
            ClearSelectedRadio();
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    ClearSelectedRadio();
}
}




const submitBtn = document.getElementById("error_btn_submit");


submitBtn.addEventListener("click", function() {
    const radioButtons = document.getElementsByName("selector");
    const sentence_id = document.querySelector("#sentence_id");
    const sentence = document.querySelector("#sentence");
    const sentence_modal = document.querySelector("#modal-sentence");


    let selectedOption = null;
    for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            selectedOption = radioButtons[i].id;
            break;
        }
    }

    if (selectedOption !== null) {
        // console.log("Tanlangan radio tugmasi: " + selectedOption);
        // console.log("Sentence ID: " + sentence_id.value);

        // Ma'lumotlarni JSON formatida yaratish
        const formData = new FormData();
        formData.append("sentence_id", sentence_id.value);
        formData.append("error_type", selectedOption);


        // Ma'lumotlarni serverga yuborish
        fetch("/sentence-error-comment/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: formData
        }).then(response => {
        if (response.ok) {
            response.json().then(data => {
                sentence.innerHTML = data.sentence;
                sentence_modal.innerHTML = data.sentence;
                sentence_id.value = data.sentence_id;
            });
        
        }
        else {
            console.error("Next sentence error......");
            // alert("Tizimga kirishni tekshiring");
            // window.open(response.json().url, "_self");
        }
    })
    .catch(error => {
        console.error("Next sentence error::::", error);
    });


    modal.style.display = "none";
    ClearSelectedRadio();

    } else {
        console.log("Hech qanday radio tugmasi tanlanmagan");
    }
});


