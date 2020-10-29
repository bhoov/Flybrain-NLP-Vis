import { writable } from 'svelte/store';
import { URLHandler } from "./etc/URLHandler"

const init = URLHandler.parameters

export const headIndex = writable(init['headIndex'] || 0);
export const queryPhrase = writable(init['queryPhrase'] || "");
export const showQueryResults = writable(init['showQueryResults'] || false)

headIndex.subscribe(value => {
    URLHandler.updateURLParam("headIndex", value)
})

queryPhrase.subscribe(value => {
    URLHandler.updateURLParam("queryPhrase", value)
})

showQueryResults.subscribe(value => {
    URLHandler.updateURLParam("showQueryResults", value)
})
