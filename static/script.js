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
const allbtn = document.querySelectorAll(".btn");
const submitForm = document.querySelectorAll(".submit-form");
const csvForm = document.querySelector(".csv-form");
const csvBtn = document.querySelector("#csvBtn")
console.log(submitForm);

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

// Select the forms and elements
const csvForm = document.querySelector('.csv-form'); // The form for uploading the CSV
const csvInputFile = document.querySelector('#csv-file-upload'); // The file input element
const submitForms = document.querySelectorAll('.submit-form'); // The forms with the send buttons

// Attach a submit event listener to each form with a send button
// Select the elements and forms
const csvForm = document.querySelector('.csv-form'); // The form for uploading the CSV
const csvInputFile = document.querySelector('#csv-file-upload'); // The file input element
const submitForms = document.querySelectorAll('.submit-form'); // The forms with the send buttons

// Attach a submit event listener to each form with a send button
submitForms.forEach(function (singleForm) {
    singleForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Create a new FormData object to hold the combined data
        const combinedData = new FormData();

        // Append the CSV file if one is selected
        if (csvInputFile.files.length > 0) {
            combinedData.append('csvFile', csvInputFile.files[0]);
        }

        // Append data from the submit form
        const formElements = singleForm.elements;
        for (let i = 0; i < formElements.length; i++) {
            const element = formElements[i];
            if (element.name && element.type !== 'file') {
                combinedData.append(element.name, element.value);
            }
        }

        // Send the combined data as a POST request to the server via AJAX
        fetch(singleForm.action, {
            method: 'POST', // Use POST method
            body: combinedData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Redirect or update the page based on the response
            window.location.href = data.redirect_url || '/';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
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
