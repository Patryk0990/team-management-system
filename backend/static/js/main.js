let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
});
let isFormSubmittedSuccessfully = false;

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function addAlertMessage(alertType, message) {
  const main = document.getElementsByTagName('main')[0];

  let alert = document.createElement('div')
  alert.classList.add('alert', 'alert-dismissible', `alert-${alertType}`, 'fade', 'show', 'd-flex', 'align-items-center', 'justify-content-center', 'position-absolute', 'w-100', 'z-3');
  alert.setAttribute('role', 'alert');

  let alertIcon = document.createElement('svg');
  alertIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  alertIcon.setAttribute('width', '16');
  alertIcon.setAttribute('height', '16');
  alertIcon.setAttribute('viewBox', '0 0 16 16');
  alertIcon.setAttribute('fill', 'currentColor');
  alertIcon.classList.add('bi', 'me-2', `text-${alertType}`);

  let alertIconContent = document.createElement('path');

  if (alertType === 'success') {
    alertIcon.classList.add('bi-check-square-fill');
    alertIconContent.setAttribute('d', 'M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z');
  }
  else if (alertType === 'danger' || alertType === 'warning') {
    alertIcon.classList.add('bi-exclamation-triangle-fill');
    alertIconContent.setAttribute('d', 'M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z');
  }
  else {
    alertIcon.classList.add('bi-info-square-fill');
    alertIconContent.setAttribute('d', 'M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm8.93 4.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM8 5.5a1 1 0 1 0 0-2 1 1 0 0 0 0 2z');
  }
  alertIcon.appendChild(alertIconContent);

  let alertContent = document.createElement('div');
  alertContent.innerHTML = message;

  let alertCloseButton = document.createElement('button');
  alertCloseButton.classList.add('btn-close');
  alertCloseButton.setAttribute('type', 'button');
  alertCloseButton.setAttribute('data-bs-dismiss', 'alert');
  alertCloseButton.setAttribute('aria-label', 'Close');

  alert.appendChild(alertIcon);
  alert.appendChild(alertContent);
  alert.appendChild(alertCloseButton);

  main.prepend(alert);
}

function toggleSidebar(event) {
  const sender = event.currentTarget;
  const sidebar = document.getElementById('sidebar');

  sender.classList.toggle('active');
  sidebar.classList.toggle('active');
}

function setFormData(event, toggleToModify, params) {
  event.stopPropagation();
  const sender = event.currentTarget;
  const formId = sender.getAttribute('data-target');
  const form = document.getElementById(formId);
  const formResponseContainer = form.parentElement.parentElement.querySelector(`#${formId}-response`);
  const submitButton = form.parentElement.parentElement.querySelector('button[type="submit"]');
  let url = form.getAttribute('data-schema-url');

  for (const [key, value] of Object.entries(params)) {
    url = url.replace(key, String(value));
  }

  if (toggleToModify) {
    submitButton.style.display = "none";
  }

  formResponseContainer.innerHTML = "<span class='loader'></span>";

  fetch(url, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then((response) => {
      return response.text().then(text => {
        return response.ok ? text : Promise.reject(text)
      });
    })
    .then(data => {
      form.setAttribute('action', url);
      form.innerHTML += data;
      formResponseContainer.innerHTML = "";
      if (toggleToModify) {
        for (const input of form.elements) {
          input.setAttribute('disabled', '');
        }
      }
    })
    .catch(responseErrorData => {
      formResponseContainer.classList.add('text-danger');
      formResponseContainer.innerHTML = "Error";
      console.error('Collecting form failed.', responseErrorData);
    });
}

function closeForm(event, resetForm, deleteFormElements) {
  const sender = event.currentTarget;

  if (isFormSubmittedSuccessfully) {
    location.reload();
  }
  else {
    const formId = sender.getAttribute('data-target');
    const form = document.getElementById(formId);
    const formResponseContainer = document.getElementById(`${formId}-response`);

    formResponseContainer.innerHTML = "";
    formResponseContainer.className = "";

    if (deleteFormElements) {
      let formGroups = form.querySelectorAll('div.form-group, div.form-check');

      formGroups.forEach((formGroup) => {
          formGroup.remove();
      });
      form.removeAttribute('action');
    }
    else if (resetForm) {
      form.reset();

      // reset errors
      const fieldsWithErrors = form.querySelectorAll('.is-invalid');
      fieldsWithErrors.forEach(fieldWithErrors => {
        fieldWithErrors.classList.remove('is-invalid');
        fieldWithErrors.parentElement.getElementsByClassName('invalid-feedback')[0].remove();
      });
    }

  }
}

function submitForm(event, hideSubmitButton) {
  const sender = event.currentTarget;
  const formId = sender.getAttribute('data-target');
  const form = document.getElementById(formId);
  const formResponseContainer = document.getElementById(`${formId}-response`);

  const formData = new FormData(form);

  // reset errors
  const fieldsWithErrors = form.querySelectorAll('.is-invalid');
  fieldsWithErrors.forEach(fieldWithErrors => {
    fieldWithErrors.classList.remove('is-invalid');
    fieldWithErrors.parentElement.getElementsByClassName('invalid-feedback')[0].remove();
  });
  formResponseContainer.innerHTML = "<span class='loader'></span>";
  formResponseContainer.className = "";

  fetch(form.action, {
    method: form.method,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: formData,
  })
    .then((response) => {
      return response.json().then(json => {
        return response.ok ? json : Promise.reject(json)
      });
    })
    .then(data => {
      formResponseContainer.classList.add('text-success');
      formResponseContainer.innerHTML = data.message;
      isFormSubmittedSuccessfully = true;

      if (hideSubmitButton) {
        sender.style.display = "none";
      }

    })
    .catch((responseErrorData) => {
      formResponseContainer.classList.add('text-danger');
      if ('non_field_errors' in responseErrorData.message || 'field_errors' in responseErrorData.message) {
        let errors = ''
        for (const error of responseErrorData.message.non_field_errors) {
          errors += `${error}<br>`
        }

        if (errors !== '') {
          formResponseContainer.innerHTML = errors;
        }
        else {
          formResponseContainer.innerHTML = '';
        }

        for (const field in responseErrorData.message.field_errors) {
          let input = form.elements[field];
          input.classList.add('is-invalid');

          let field_errors = document.createElement('div');
          field_errors.classList.add('invalid-feedback');
          for (const error of responseErrorData.message.field_errors[field]) {
            field_errors.innerHTML += `${error}<br>`;
          }
          input.parentElement.appendChild(field_errors);
        }
      }
      else {
        formResponseContainer.innerHTML = responseErrorData.message;
      }

      console.error('Submit form failed.', responseErrorData);
    });
}

function toggleFormInputs(event) {
  const sender = event.currentTarget;
  const formId = sender.getAttribute('data-target');
  const form = document.getElementById(formId);
  const state = sender.getAttribute('data-state');
  const submitButton = form.parentElement.parentElement.querySelector('button[type="submit"]');

  if (state === 'disabled') {
    for (const input of form.elements) {
      input.removeAttribute('disabled');
    }
    sender.setAttribute('data-state', 'enabled');
    submitButton.style.display = "block";
  }
  else {
    for (const input of form.elements) {
      input.setAttribute('disabled', '');
    }
    sender.setAttribute('data-state', 'disabled');
    submitButton.style.display = "none";
  }
}

function setDeleteData(event, params) {
  event.stopPropagation()
  const sender = event.currentTarget;
  let modal;

  if (sender.getAttribute('data-bs-target')) {
    const modalId = sender.getAttribute('data-bs-target').substring(1);
    modal = document.getElementById(modalId);
  }
  else {
    modal = sender.parentElement.parentElement;
  }

  const modalBody = modal.querySelector(".modal-body:not(.modal-select)");
  const submitButton = modal.querySelector('button[type="submit"]');
  let url = submitButton.getAttribute('data-schema-url');

  for (const [key, value] of Object.entries(params)) {
    url = url.replace(key, String(value));
  }

  modalBody.style.display = "block";
  submitButton.setAttribute('data-action', url);
  submitButton.style.display = "block";
}

function closeDeleteData(event, resetURL) {
  const sender = event.currentTarget;

  if (isFormSubmittedSuccessfully) {
    location.reload();
  }
  else {
    const modal = sender.parentElement.parentElement;
    const modalBody = modal.querySelector(".modal-body:not(.modal-select)");
    const submitButton = modal.querySelector('button[type="submit"]');
    const responseContainerId = submitButton.getAttribute('data-response-container-id');
    const responseContainer = modal.querySelector(`#${responseContainerId}`);

    if (resetURL) {
      submitButton.removeAttribute('data-action');
    }

    modalBody.style.display = "none";
    submitButton.style.display = "none";
    responseContainer.className = "";
    responseContainer.innerHTML = "";
  }
}

function submitDeleteModal(event) {
  const sender = event.currentTarget;

  const url = sender.getAttribute('data-action');
  const fetch_method = sender.getAttribute('data-method');
  const responseContainerId = sender.getAttribute('data-response-container-id');
  const responseContainer = document.getElementById(responseContainerId);
  const CSRFToken = getCookie('csrftoken');

  responseContainer.innerHTML = "<span class='loader'></span>";
  responseContainer.className = "";

  fetch(url, {
    method: fetch_method,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': CSRFToken,
    },
  })
    .then((response) => {
      return response.json().then(json => {
        return response.ok ? json : Promise.reject(json)
      });
    })
    .then(data => {
      responseContainer.classList.add('text-success');
      responseContainer.innerHTML = data.message;
      sender.style.display = "none";
      isFormSubmittedSuccessfully = true;
    })
    .catch(responseErrorData => {
      responseContainer.classList.add('text-danger');
      responseContainer.innerHTML = responseErrorData.message;
      if (fetch_method === 'DELETE') {
        console.error('Deleting object failed.', responseErrorData);
      }
      else {
        console.error('Modifying object failed.', responseErrorData);
      }
    });
}

function resetSelectInput(event) {
  const sender = event.currentTarget;
  const modal = sender.parentElement.parentElement;
  const selectId = sender.getAttribute('data-select-id');
  const select = modal.querySelector(`#${selectId}`);
  select.selectedIndex = 0;
}

function changeModifyFormData(event, params) {
  const sender = event.currentTarget;
  const modal = sender.parentElement.parentElement;
  const modalBody = modal.querySelector(".modal-body:not(.modal-select)");

  modalBody.style.display = "none";
  closeForm(event, true, true);
  modalBody.style.display = "block";
  setFormData(event, false, params);
}

function closeModifyModal(event) {
  const sender = event.currentTarget;
  const modal = sender.parentElement.parentElement;
  const modalBody = modal.querySelector(".modal-body:not(.modal-select)");

  closeForm(event, true, true);
  modalBody.style.display = "none";
  resetSelectInput(event);
}

function changeDeleteFormData(event, params) {
  closeDeleteData(event, true);
  setDeleteData(event, params);
}

function closeDeleteModal(event) {
  closeDeleteData(event, true);
  resetSelectInput(event);
}

function getList(event, params) {
  event.stopPropagation();
  const sender = event.currentTarget;
  const elementsContainer = document.getElementById(sender.getAttribute('data-elements-target'));
  let url = elementsContainer.getAttribute('data-schema-url');

  for (const [key, value] of Object.entries(params)) {
    url = url.replace(key, String(value));
  }
  elementsContainer.innerHTML = "<span class='loader'></span>";
  elementsContainer.className = "";

  fetch(url, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then((response) => {
      return response.text().then(text => {
        return response.ok ? text : Promise.reject(text)
      });
    })
    .then(data => {
      elementsContainer.setAttribute('data-url', url);
      elementsContainer.innerHTML = data;
    })
    .catch(responseErrorData => {
      elementsContainer.classList.add('text-danger');
      elementsContainer.innerHTML = "Error";
      console.error('Collecting elements failed.', responseErrorData);
    });
}

function resetList(event) {
  const sender = event.currentTarget;
  const elementsContainer = document.getElementById(sender.getAttribute('data-elements-target'));
  elementsContainer.innerHTML = "";
  elementsContainer.className = "";
  elementsContainer.removeAttribute('data-url');
}

function getNewList(event) {
  const sender = event.currentTarget;
  const elementsContainer = sender.parentElement.parentElement.parentElement.parentElement;
  const page = sender.getAttribute('data-page');
  let url = `${elementsContainer.getAttribute('data-url')}?${new URLSearchParams({page: page})}`

  elementsContainer.innerHTML = "<span class='loader'></span>";
  elementsContainer.className = "";

  fetch(url, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then((response) => {
      return response.text().then(text => {
        return response.ok ? text : Promise.reject(text)
      });
    })
    .then(data => {
      elementsContainer.innerHTML = data;
    })
    .catch(responseErrorData => {
      elementsContainer.classList.add('text-danger');
      elementsContainer.innerHTML = "Error";
      console.error('Collecting elements failed.', responseErrorData);
    });
}

function changeListWithCreateModal(event, params) {
  getList(event, params);
  setFormData(event, false, params);
}

function closeListWithCreateModal(event) {
  resetList(event);
  closeForm(event, true, true);
}