import tippy from "tippy.js"
// import "tippy.js/dist/tippy.css" // This needed to be included in the head of App.svelte

export default function mytippy(node, props) {

    tippy(node, props)

    return {
        destroy() {
            console.log('A tippy was destroyed')
        }
    }
}