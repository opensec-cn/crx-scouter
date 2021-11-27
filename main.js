import './style.css'

const demo = async () => {

    const { check_all_crx, navigator_plugins } = await import('./scouter/scouter')
    
    const append_text = (crx_info, element_id) => {
      const element_text = `<li><b> ${crx_info.name} </b> (<a href="${crx_info.url}">${crx_info.url}</a>)</li>`
      const app_div = document.querySelector(element_id)
      app_div.innerHTML = app_div.innerHTML + element_text;
    }
    
    const callback = (crx_info) => {
      append_text(crx_info, "#app")
    }
    
    const nps = navigator_plugins()
    for (let i = 0; i < nps.length; i++) {
      const crx_info = nps[i]
      append_text(crx_info, "#app-plugins")
    }

    check_all_crx(callback)


}

demo().catch(console.error);
