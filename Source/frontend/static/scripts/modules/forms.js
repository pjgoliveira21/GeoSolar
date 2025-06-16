// Objeto global que abriga as expressões regulares para validação de formulários
var regexObj = {};

// Pedir ao servidor as expressões regulares
export async function getRegEx() {
  const response = await fetch('/get-regex');
  const patterns = await response.json();
  regexObj = {
    email: new RegExp(patterns.email),
    pwd: new RegExp(patterns.pwd),
  };
}

// Sendo chamada a cada mudança de input, dá feedback visual ao utilizador em tempo real sobre o respeito às regras de formato do campo alterado
// A partir do ID recebido do evento, a função é feita de forma a identificar o tipo de campo e a expressão regular a ser usada
export function fieldFormatFeedback(event) {
  
  // Identificação do tipo de campo e expressão regular a ser usada
  let sourceID = event.target.id;
  let type;
  if(sourceID.toLowerCase().includes("email")) { type="email"; }
  if(sourceID.toLowerCase().includes("pwd")) { type="pwd"; }
  let regEx = regexObj[type];  

  // Validação do campo e alteração de classes baseado na validação do campo
  let fieldElem = document.getElementById(sourceID);
  let fieldVal = fieldElem.value;
  fieldElem.classList.remove('border-success', 'border-danger', 'border-white');
  if (!fieldVal) fieldElem.classList.add('border-white');
  else if (!regEx.test(fieldVal)) fieldElem.classList.add('border-danger');
  else fieldElem.classList.add('border-success');
}

// Validar o formulário de login
export function loginValidator() {

  // Acesso aos elementos do formulário
  const emailField = document.getElementById('navEmail');
  const passwordField = document.getElementById('navPwd');
  if (regexObj['email'].test(emailField.value) && regexObj['pwd'].test(passwordField.value)) return true;
  alert("Verifique o formato dos dados inseridos. nos campos assinalados a vermelho.");
  return false;
}

// Função de validação de registo
export function registerValidator() {

  // Acesso aos elementos do formulário
  const emailField = document.getElementById('regEmail');
  const passwordField = document.getElementById('regPwd');
  const email2Field = document.getElementById('regEmail2');
  const password2Field = document.getElementById('regPwd2');

  // Validação dos campos de email
  if (!regexObj['email'].test(emailField.value)) {
    alert('Check email format rules.');
    return false;
  }

  // Se válidos, verificar se os emails são iguais
  if (emailField.value !== email2Field.value) {
    email2Field.classList.remove('border-success', 'border-danger', 'border-white');
    email2Field.classList.add('border-danger');
    alert("Inserted email addresses are not identical");
    return false;
  }

  // Validação dos campos de password
  if (!regexObj['pwd'].test(passwordField.value)) {
    alert('Check password format rules.');
    return false;
  }
  
  // Se válidos, verificar se as passwords são iguais
  if (passwordField.value !== password2Field.value) {
    password2Field.classList.remove('border-success', 'border-danger', 'border-white');
    password2Field.classList.add('border-danger');
    alert("Inserted passwords are not identical");
    return false;
  }
}

export function addStationValidator() {
  const latitude = document.getElementById('stationLatitude').value.trim();
  const longitude = document.getElementById('stationLongitude').value.trim();
  const capacity = document.getElementById('stationCapacity').value.trim();

  if (isNaN(latitude) || latitude < -90 || latitude > 90) {
      alert('Please enter a valid latitude between -90 and 90.');
      return false;
  }

  if (isNaN(longitude) || longitude < -180 || longitude > 180) {
      alert('Please enter a valid longitude between -180 and 180.');
      return false;
  }

  if (isNaN(capacity) || capacity <= 0) {
      alert('Please enter a positive valid capacity.');
      return false;
  }

  return true;
}
