import tippy from "tippy.js"
import "tippy.js/dist/tippy.css"

export default function mytippy(node, props) {

    tippy(node, props)

    return {
        destroy() {
            console.log('A tippy was destroyed')
        }
    }
}