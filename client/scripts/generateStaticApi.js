#!/usr/bin/env node

/**
 * Run with `node --experimental-modules generateStaticApi.js
 */
import _ from "lodash";
import fs from "fs";
import path from "path";
import hash from "object-hash";
import fetch from "node-fetch";
import exampleSentences from "../src/config/exampleSentences.js"

/**
 * Let's write some helper functions to fetch information from the backend.
 * This is important because `d3.json` relies on `fetch` which has client-only functionality
 * 
 * Copied from d3's source code
 */
function responseJson(response) {
    if (!response.ok) throw new Error(response.status + " " + response.statusText);
    if (response.status === 204 || response.status === 205) return;
    return response.json();
  }

export function json(input, init) {
    return fetch(input, init).then(responseJson);
}

/**
 * NodeJS can also not import TypeScript files, so I needed to copy the functions from the typescript files into this script
 */
// Convert a base URL with params into a GET request
export function makeUrl(base, params) {
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

// Convert object information the message for a POST request    
export const toPayload = (toSend) => {return {
    method:"POST",
    body:JSON.stringify(toSend),
    headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
}}


const [,, ...args] = process.argv

/**
 * Configure the cache we want to save
 */
const outputDir = "../public/routeInfo/"
const baseUrl = "http://127.0.0.1:8000/api/"
const nNeurons = 400 // Should be the same as the backend's response to the `n-heads` query below
const nShow = 20

const toCache = [
    {
        routeName: "sentence-to-keywords",
        method: "GET",
        queries: exampleSentences.map(s => ({sentence: s})),
    },
    {
        routeName: "n-heads",
        method: "GET",
        queries: [{}], // Should be the same as nNeurons above
    },
    {
        routeName: "memory-concepts",
        method: "GET",
        queries: _.range(nNeurons).map(i => ({
            head_index: i,
            n_show: nShow
        })),
    },
    {
        routeName: "mem-order",
        method: "GET",
        queries: [{}], // Empty response
    },
    {
        routeName: "query-top-mems-by-phrase",
        method: "GET",
        queries: exampleSentences.map(s => ({
            phrase: s,
            beta: 10.0
        }))
    },
]

/**
 * We can use the above desired queries to hash results and put them into folders with expected repsponses
 */

// Take each query object in the `toCache` above and cache the backend response
async function cacheResponses(query) {
    const outDir = path.join(outputDir, query.routeName)
    fs.mkdir(outDir, {recursive: true}, err => (err && console.log(err)))

    const endpoint = baseUrl + query.routeName
    console.log("Working on ENDPOINT: ", endpoint)

    for (const q of query.queries) {
        const queryHash = hash(q)
        const url = makeUrl(endpoint, q)
        const response = await json(url)
        const fileContent = JSON.stringify(response)
        const outFile = path.join(outDir, queryHash + ".json")
        fs.writeFile(outFile, fileContent, err => {
            if (err) throw err
        })
    }
    console.log(`Finished processing ${endpoint}`)
}

for (const q of toCache) {
    cacheResponses(q)
}