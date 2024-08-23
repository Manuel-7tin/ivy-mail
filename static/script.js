"use strict";
const options = document.querySelector(".options");
const emailOption = document.querySelector("#email");
const smsOption = document.querySelector("#sms");
const bothOption = document.querySelector("#both");
const uploadCsv = document.querySelectorAll(".upload-csv");
const uploadIcon = document.querySelectorAll(".upload-icon");
const csvInputFile = document.querySelector("#csv-file-upload");
const body = document.querySelectorAll(".body");
const emailBody = document.querySelector(".email-body");
const smsBody = document.querySelector(".sms-body");
const bothBody = document.querySelector(".both-body");
const textAreas = document.querySelectorAll(".msgs");
const allbtn = document.querySelectorAll(".btn");
const submitForm = document.querySelectorAll(".submit-form");
const csvForm = document.querySelector(".csv-form");
const csvBtn = document.querySelector("#csvBtn");
console.log(submitForm);
console.log(textAreas);

smsBody.classList.add("js-class1");
bothBody.classList.add("js-class1");

const screenWidth = window.innerWidth;
console.log(screenWidth);

console.log(uploadIcon);
emailOption.addEventListener("click", function () {
  emailBody.classList.remove("js-class1", "js-empty-class");
  smsBody.classList.add("js-class1");
  bothBody.classList.add("js-class1");
  emailOption.classList.add("js-class-option");
  smsOption.classList.remove("js-class-option");
  bothOption.classList.remove("js-class-option");
});
smsOption.addEventListener("click", function () {
  smsBody.classList.remove("js-class1", "js-empty-class");
  emailBody.classList.add("js-class1");
  bothBody.classList.add("js-class1");
  emailOption.classList.remove("js-class-option");
  smsOption.classList.add("js-class-option");
  bothOption.classList.remove("js-class-option");
});
bothOption.addEventListener("click", function () {
  bothBody.classList.remove("js-class1", "js-empty-class");
  emailBody.classList.add("js-class1");
  smsBody.classList.add("js-class1");
  emailOption.classList.remove("js-class-option");
  smsOption.classList.remove("js-class-option");
  bothOption.classList.add("js-class-option");
  console.log(this);
});

uploadIcon.forEach(function (single, i) {
  single.addEventListener("click", function () {
    csvInputFile.click();
    let arr = [];
    csvInputFile.onchange = function () {
      if (csvInputFile.files.length > 0) {
        for (let i = 0; i < csvInputFile.files.length; i++) {
          const value = csvInputFile.files.item(i).name;
          arr.push(value);
          console.log(value);
          console.log(arr);
          console.log();
          single.previousElementSibling.classList.add("js-class-p");
          if (arr.length > 1) {
            const toDisplay = arr.join().slice(0, 30);
            console.log(toDisplay);
            single.previousElementSibling.innerHTML = `${toDisplay}...`;
          } else {
            single.previousElementSibling.innerHTML = `${arr
              .join()
              .slice(0, 20)}...`;
          }
        }
      }
    };
  });
});

textAreas.forEach(function (single) {
  // single.style.color = "red";
  single.addEventListener("input", () => {
    const text = single.value;
    console.log(text);

    const sentences = text.split(". ");
    let i = 0;
    while (i < sentences.length) {
      sentences[i] =
        sentences[i].charAt(0).toUpperCase() + sentences[i].slice(1);
      console.log(sentences[i]);
      i++;
    }
    single.value = text.charAt(0).toUpperCase() + text.slice(1);
    console.log(sentences, text);
    single.value = sentences.join(". ");
  });
});

// VERY IMPORTANT!!
var quill = new Quill("#editor", {
  theme: "snow",
});

document
  .getElementById("messageForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Get HTML content from Quill editor
    var message = quill.root.innerHTML;

    // Create a FormData object to combine both forms' data
    var formData = new FormData(document.getElementById("csvForm"));
    formData.append("subject", document.getElementById("email-subject").value);
    formData.append("body", message);
    //    formData.append('body', document.getElementById('compose-email-input').value);

    // Submit the combined form data via POST
    fetch("/mail", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          // Redirect manually using the URL from the response
          window.location.href = response.url;
        } else {
          return response.json(); // For error handling or any other response
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
// IMPORTANCE ENDS!!!
// document.querySelector("#editor").style.color = "red";
textAreas.forEach(function (single) {
  // single.style.color = "red";
  single.addEventListener("input", () => {
    const text = single.value;
    console.log(text);

    const sentences = text.split(". ");
    let i = 0;
    while (i < sentences.length) {
      sentences[i] =
        sentences[i].charAt(0).toUpperCase() + sentences[i].slice(1);
      console.log(sentences[i]);
      i++;
    }
    single.value = text.charAt(0).toUpperCase() + text.slice(1);
    console.log(sentences, text);
    single.value = sentences.join(". ");
  });
});
//console.log("come on man")
//submitForm.forEach(function (single, i) {
//    console.log("come on man")
//  single.addEventListener("submit", function (e) {
//    e.preventDefault();
//    csvBtn.click();
////    csvForm.submit();
//  });
//});

// allbtn.forEach(function(btn, i){
//     btn.addEventListener('click', function(e){
//         console.log(e)
//         console.log(btn)
//         console.log(btn.parentElement.children)
//         if(btn.className.includes('email')){
//             const xhr=new XMLHttpRequest()
//             xhr.open("POST","/my-server-action")
//             xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded")
//             xhr.send('myInput' + document.querySelector(".compose-email-input").value)
//     //         xhr.send('myInput' + document.querySelector(".subject-input").value)
//     //
//     }
//          else if(btn.className.includes('sms')){
//             const xhr=new XMLHttpRequest()
//             xhr.open("POST","/my-server-action")
//             xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded")
//             xhr.send('myInput' + document.querySelector(".compose-sms-input").value)
//         }
//          else if(btn.className.includes('both')){
//             const xhr=new XMLHttpRequest()
//             xhr.open("POST","/my-server-action")
//             xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded")
//             xhr.send('myInput' + document.querySelector(".compose-both-input").value)
//         }

//     })
// })
