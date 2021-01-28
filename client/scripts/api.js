/**
 * NodeJS cannot use `d3.json` because it requires the fetch API that is client only. This is the `d3.json` function source code, copied below.
 * 
 * Also note, the `import fetch from "node-fetch"` syntax is only available when NodeJS runs the CLI script with `node --experimental-modules ___.js`
 */
import fetch from "node-fetch";

function responseJson(response) {
    if (!response.ok) throw new Error(response.status + " " + response.statusText);
    if (response.status === 204 || response.status === 205) return;
    return response.json();
  }

function json(input, init) {
    return fetch(input, init).then(responseJson);
}

/**
 * NodeJS can also not import TypeScript files, so I needed to copy the functions from the typescript files into this script
 */
function makeUrl(base, params) {
    if (params){
        let out = base + "?";

        Object.keys(params).forEach( k => {
            out += k;
            out += '=';
            out += params[k];
            out += "&";
        })
        return out.replace(/&$/g, "");
    }
    else {
        return base;
    }
};

/**
 * Convert object information the message for a POST request    
 */
const toPayload = (toSend) => {return {
    method:"POST",
    body:JSON.stringify(toSend),
    headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
}}



// class API {

//     constructor(baseURL = null) {
//         if (this.baseURL == null) {
//             this.baseURL = baseurl + '/api';
//         }
//     }

//     sentenceToKeywords(sentenc) {
//         const route = "/sentence-to-keywords"
//         let toSend = { sentence }
//         const url = makeUrl(this.baseURL + route, toSend)
//         console.log("--- GET " + url);
//         return d3.json(url)
//     }

//     sentenceToTokens(sentence) {
//         const route = "/sentence-to-tokens"
//         let toSend = { sentence }
//         const url = makeUrl(this.baseURL + route, toSend)
//         console.log("--- GET " + url);
//         return d3.json(url)
//     }

//     getNNeurons() {
//         const route = "/n-heads"
//         const url = makeUrl(this.baseURL + route, {})
//         console.log("--- GET " + url)
//         return d3.json(url)
//     }

//     // Don't let user choose beta
//     // getNeuronConcepts(head_index: number, n_show: number, beta:number): Promise<tp.Concept[]> {
//     getNeuronConcepts(neuron_idx, n_show) {
//         const route = "/memory-concepts"
//         let toSend = { head_index:neuron_idx, n_show }
//         const url = makeUrl(this.baseURL + route, toSend)
//         console.log("--- GET " + url);
//         return d3.json(url)
//     }

//     getNeuronOrdering() {
//         const route = "/mem-order"
//         const url = makeUrl(this.baseURL + route, {})
//         console.log("--- GET " + url);
//         return d3.json(url)
//     }

//     queryTopNeuronsByPhrase(phrase, beta) {
//         const route = "/query-top-mems-by-phrase"
//         let toSend = { phrase, beta }
//         const url = makeUrl(this.baseURL + route, toSend)
//         console.log("--- GET " + url);
//         return d3.json(url)
//     }
// };

// moduel.exports = {
//     API
// }

export function foo() {
    const route = makeUrl("http://127.0.0.1:8000/api/sentence-to-keywords", {sentence: "hello there friend"})
    return json(route)
}