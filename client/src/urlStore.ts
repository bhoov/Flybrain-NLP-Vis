import { writable } from 'svelte/store';
import { URLHandler } from "./etc/URLHandler"

const init = URLHandler.parameters

export const neuronIndex = writable(init['neuronIndex'] || 0);
export const queryPhrase = writable(init['queryPhrase'] || "");
export const showQueryResults = writable(init['showQueryResults'] || false)
export const allowCustomInput = false
// export const allowCustomInput = writable(init['allowCustomInput'] == "true" ? true : false)

neuronIndex.subscribe(value => {
    URLHandler.updateURLParam("neuronIndex", value)
})

queryPhrase.subscribe(value => {
    URLHandler.updateURLParam("queryPhrase", value)
})

showQueryResults.subscribe(value => {
    URLHandler.updateURLParam("showQueryResults", value)
})

// allowCustomInput.subscribe(value => {
//     URLHandler.updateURLParam("allowCustomInput", value)
// })