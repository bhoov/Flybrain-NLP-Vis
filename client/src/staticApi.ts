/**
 * Copied from `api.ts`. This modification looks only for responses generated 
 * by `scripts/generateStaticApi.js` in `public/routeInfo/ROUTENAME/QUERY_HASH
 */
import * as d3 from 'd3';
import hash from "object-hash";
import * as tp from "./types";
import {memoize} from "./etc/cacher"

const staticURL = "/routeInfo"

function findResponseJson(routeName: string, query: {}) {
    const hashcode = hash(query)
    const responseAt = `${staticURL}/${routeName}/${hashcode}.json`
    return responseAt
}

function sentenceToKeywords(sentence: string): Promise<string[]> {
    const routeName = "sentence-to-keywords"
    const fname = findResponseJson(routeName, {sentence})
    return d3.json(fname)
}

function getNNeurons(): Promise<number> {
    const routeName = "n-heads"
    const fname = findResponseJson(routeName, {})
    return d3.json(fname)
}

function getNeuronConcepts(neuron_idx: number, n_show: number=20): Promise<tp.Concept[]> {
    const routeName = "memory-concepts"
    const fname = findResponseJson(routeName, {
        head_index:neuron_idx,
        n_show 
    })
    return d3.json(fname)
}

function getNeuronOrdering(): Promise<number[]> {
    const routeName = "mem-order"
    const fname = findResponseJson(routeName, {})
    return d3.json(fname)
}

function queryTopNeuronsByPhrase(phrase: string, beta:number=10.0): Promise<tp.TopMemResponse> {
    const routeName = "query-top-mems-by-phrase"
    const fname = findResponseJson(routeName, { phrase, beta })
    return d3.json(fname)
}

const exposedFunctions = [
    findResponseJson,
    sentenceToKeywords,
    getNNeurons,
    getNeuronConcepts,
    getNeuronOrdering,
    queryTopNeuronsByPhrase,
]

const exposed: any = exposedFunctions.reduce((acc, f: any) => {
    acc[f.name] = memoize(f)
    return acc
}, {})

export default exposed
