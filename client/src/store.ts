import { writable } from 'svelte/store';
import { URLHandler } from "./etc/URLHandler"

/** Parameters to store in URL */
const init = URLHandler.parameters

function createQueryPhrase(maxLength=250) {
    const {subscribe, set, update} = writable(init['showQueryResults'] || false)

    return {
        subscribe, update,
        set: x => {
            console.log("Setting X with: ", x)
            console.log("Of length", x.length)
            set(x.slice(0, maxLength))
        }
    }
}

export const neuronIndex = writable(init['neuronIndex'] || 0);
export const queryPhrase = createQueryPhrase(300)
export const showQueryResults = writable(init['showQueryResults'] || false)
export const allowCustomInput = writable(init['allowCustomInput'] == "true" ? true : false)

neuronIndex.subscribe(value => {
    URLHandler.updateURLParam("neuronIndex", value)
})

queryPhrase.subscribe(value => {
    URLHandler.updateURLParam("queryPhrase", value)
})

showQueryResults.subscribe(value => {
    URLHandler.updateURLParam("showQueryResults", value)
})

allowCustomInput.subscribe(value => {
    URLHandler.updateURLParam("allowCustomInput", value)
})

/**Additional parameters */
export const offensiveNeurons = new Set([87, 96, 138, 153, 358])
// export const offensiveNeurons = new Set([87, 96, 138, 153, 358, 180, 203, 235, 312])