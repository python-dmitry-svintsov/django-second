const username = document.getElementById("username");
const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const password = document.getElementById("password");
const city = document.getElementById("city");
const sex = document.querySelectorAll(".sex_item");
const prodfile_sex_id = document.getElementById("sex_profile_id").value;
sex[prodfile_sex_id - 1].checked = true;
const foto = document.getElementById("image");
const button = document.getElementById("button");

const applicantForm = document.getElementById("form");
const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

const submit_trigger = applicantForm.querySelector("button.submit");
const submitEvent = new SubmitEvent("submit", { submitter: button });
// applicantForm.dispatchEvent(submitEvent);

const controller = new AbortController();
const fetch_request = [];
const redirect_url = document.getElementById("redirect_url");

function toggleLoader() {
  const loader = document.getElementById("loader");
  loader.classList.toggle("hidden");
}

async function sendData(data) {
  return await fetch(`/auth/profile/sda6/update`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      // "Content-Type":
      //   "multipart/form-data; boundary=-----WebKitFormBoundary7MA4YWxkTrZu0gW--",
    },
    body: data,
    signal: controller.signal,
    redirect: "manual",
    referrerPolicy: "no-referrer",
    core: "same-origin",
  });
}

function serializeForm(formNode) {
  const { elements } = formNode;

  const data = new FormData();
  data.append(username.name, username.value);
  data.append(first_name.name, first_name.value);
  data.append(last_name.name, last_name.value);
  data.append(password.name, password.value);
  data.append(city.name, city.value);
  for (var i = 0; i < sex.length; i++) {
    if (sex[i].checked == true) {
      data.append(sex[i].name, sex[i].id);
    }
  }
  data.append(foto.name, foto.files[0]);
  return data;
}

function onSuccess(url) {
  alert("Ваши данные изменены!");
  window.location.href = redirect_url.href;
}

function onError(error) {
  alert(error.message);
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const controller = new AbortController();

  const data = serializeForm(event.target);
  toggleLoader();
  const response = await sendData(data);
  console.log(response);
  controller.abort();
  const status = response.status;
  const error = response.error;
  const url = response.url;
  toggleLoader();
  // if (status === 200) {
  //   onSuccess(url);
  // } else {
  //   onError(error);
  // }
  if (error) {
    onError(error);
  } else {
    onSuccess(url);
  }
}

applicantForm.addEventListener("submit", handleFormSubmit);
// button.addEventListener("click", handleFormSubmit);
applicantForm.addEventListener("input", checkValidity);

function toggleLoader() {
  const loader = document.getElementById("loader");
  loader.classList.toggle("hidden");
}

function checkValidity(event) {
  // const formNode = event.target.form;
  // const isValid = formNode.checkValidity();
  isValid = username.value && password.value ? true : false;
  button.disabled = !isValid;
}
