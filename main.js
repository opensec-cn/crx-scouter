import './style.css'
import {check_all_crx, check_one} from './scouter/scouter'


const callback = (crx_info) => {
  const element_text = `<li><b> ${crx_info.name} </b> (<a href="${crx_info.url}">${crx_info.url}</a>)</li>`
  const app_div = document.querySelector("#app")
  app_div.innerHTML = app_div.innerHTML + element_text;
}

check_all_crx(callback)
