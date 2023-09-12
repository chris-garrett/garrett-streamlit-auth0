import { Streamlit } from "streamlit-component-lib"
import createAuth0Client from '@auth0/auth0-spa-js';
import "./style.css"

const div = document.body.appendChild(document.createElement("div"))
const button = div.appendChild(document.createElement("button"))
button.className = "log"
button.textContent = "Login"


// set flex collumn so the error message appears under the button
div.style = "display: flex; flex-direction: column; color: rgb(104, 85, 224); font-weight: 600; margin: 0; padding: 10px"
const errorNode = div.appendChild(document.createTextNode(""))

// Global vars
let client_id
let domain
let audience
let debug_logs
let auth0

const getOriginUrl = () => {
  // Detect if you're inside an iframe
  if (window.parent !== window) {
    const currentIframeHref = new URL(document.location.href)
    const urlOrigin = currentIframeHref.origin
    const urlFilePath = decodeURIComponent(currentIframeHref.pathname)
    // Take referrer as origin
    return urlOrigin + urlFilePath
  } else {
    return window.location.origin
  }
}

const createClient = async () => {
  if (auth0) return;

  auth0 = await createAuth0Client({
    domain: domain,
    client_id: client_id,
    redirect_uri: getOriginUrl(),
    audience: audience,
    useRefreshTokens: true,
    cacheLocation: "localstorage",
  });
}

const logout = async () => {

  await createClient();

  auth0.logout({ returnTo: getOriginUrl() })


  Streamlit.setComponentValue(null)
  button.textContent = "Login"
  button.removeEventListener('click', logout)
  button.addEventListener('click', login)
}

const login = async () => {

  if (debug_logs) {
    console.log(
      "Starting session\n" +
      "Configuration:\n" +
      "  Client Id:" + client_id + "\n" +
      "  Domain:", domain + "\n" +
      "  Audience:", audience + "\n" +
      "  Callback urls set to: ", getOriginUrl() + "\n"
    );
  }

  button.textContent = 'working...'
  await createClient();

  try {
    await auth0.loginWithPopup();
    errorNode.textContent = ''
  }
  catch (err) {
    console.log(err)
    errorNode.textContent = `Popup blocked, please try again or enable popups` + String.fromCharCode(160)
    return
  }
  const user = await auth0.getUser();

  if (debug_logs) {
    console.log("user:", user)
  }

  let token = false

  try {

    token = await auth0.getTokenSilently({
      audience: audience,
      scope: "read:current_user",
    });
  }
  catch (error) {
    if (error.error === 'consent_required' || error.error === 'login_required') {
      if (debug_logs) {
        console.log('asking user for permission to their profile')
      }
      token = await auth0.getTokenWithPopup({
        audience: audience,
        scope: "read:current_user",
      });
      if (debug_logs) {
        console.log("token:", token)
      }
    }
    else {
      console.error(error)
      Streamlit.setComponentValue(null)
      button.textContent = "Login"
      return
    }
  }

  let userCopy = JSON.parse(JSON.stringify(user));
  userCopy.token = token
  if (debug_logs) {
    console.log("user:", userCopy);
  }

  Streamlit.setComponentValue(userCopy)
  button.textContent = "Logout"
  button.removeEventListener('click', login)
  button.addEventListener('click', logout)
}

const resume = async () => {
  if (debug_logs) {
    console.log(
      "Resuming session\n" +
      "Configuration:\n" +
      "  Client Id:" + client_id + "\n" +
      "  Domain:", domain + "\n" +
    "  Audience:", audience + "\n" +
    "  Callback urls set to: ", getOriginUrl() + "\n"
    );
  }

  button.textContent = 'working...'
  await createClient();

  const user = await auth0.getUser() || {};
  
  if (debug_logs) {
    console.log("user", user);
  }

  let token = false

  try {
    token = await auth0.getTokenSilently({
      audience: audience,
      scope: "read:current_user",
    });

  }
  catch (error) {
    console.error(error)
    Streamlit.setComponentValue(null)
    button.textContent = "Login"
    return
  }

  let userCopy = JSON.parse(JSON.stringify(user));
  userCopy.token = token
  if (debug_logs) {
    console.log("user:", userCopy);
  }

  Streamlit.setComponentValue(userCopy)
  button.textContent = "Logout"
  button.removeEventListener('click', login)
  button.addEventListener('click', logout)
}

button.addEventListener('click', login)

async function onRender(event) {
  const data = event.detail

  client_id = data.args["client_id"]
  domain = data.args["domain"]
  audience = data.args["audience"]
  debug_logs = data.args["debug_logs"]

  if (!window.auth0_component_rendered) {
    await createClient();
    if (await auth0.isAuthenticated()) {
      await resume();
    }
    window.auth0_component_rendered = true;
  }


  Streamlit.setFrameHeight()
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
