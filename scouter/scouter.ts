
import { fparray } from './fp-1-realfile-all-ext'

export const check_all_crx = async (alive_callback) => {

    for (let index = 0; index < fparray.length; index++) {

        const fingerprint = fparray[index]
        const readfile_list = fingerprint.real_access_files

        const real_url = `chrome-extension://${fingerprint.extid}/${readfile_list[0]}`
        const flag = await check_crx_alive(real_url)

        if (flag) {
            alive_callback(fingerprint)
        }

    }
}

export const check_one = async (crxid, alive_callback) => {

    for (let index = 0; index < fparray.length; index++) {

        const fingerprint = fparray[index]

        if (fingerprint.extid != crxid) {
            continue
        }

        const readfile_list = fingerprint.real_access_files

        // TODO: support multiple real access file in fingerprint
        // use for loop in fingerprint.real_access_files
        const real_url = `chrome-extension://${fingerprint.extid}/${readfile_list[0]}`
        const flag = await check_crx_alive(real_url)

        if (flag) {
            // TODO: we need the extension name too.
            alive_callback(fingerprint)
        }

        return

    }
}

const check_crx_alive = async (url): Promise<boolean> =>  {

    return new Promise<boolean>((resolve, reject) => {

        if (!url.startsWith("chrome-extension://")) {
            reject(false)
        }

        let xhr = new XMLHttpRequest();

        xhr.open('GET', url);

        xhr.onload = function() {
            // xhr.status != 200
            // can get statusText and response.length
            if (xhr.status == 200) {
                resolve(true)
            }
        };

        xhr.onprogress = function(event) {
            if (event.lengthComputable && (event.total > 0)) {
                resolve(true)
            }
        };

        xhr.onerror = function() {
            // ingnore error
            resolve(false)
        };

        // error too much.
        try {

            xhr.send();

        } catch (error) {
            
            console.debug(error)

        }

    });

}

// check_crx_alive 
const check_crx_alive_ = (url, callback) => {

}
