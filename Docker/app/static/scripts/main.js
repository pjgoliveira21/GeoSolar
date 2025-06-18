import { initMapa, setMarkers, moveToTarget } from './modules/map.js';

// map.js
window.initMapa=initMapa;
window.setMarkers=setMarkers;
window.moveToTarget=moveToTarget;

import { fieldFormatFeedback, loginValidator, registerValidator, getRegEx, addStationValidator } from './modules/forms.js';

//forms.js
window.fieldFormatFeedback= fieldFormatFeedback;
window.loginValidator = loginValidator;
window.registerValidator = registerValidator;
window.getRegEx = getRegEx;
window.addStationValidator = addStationValidator;