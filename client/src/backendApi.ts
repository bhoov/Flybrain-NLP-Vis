import {json} from 'd3';
import { makeUrl, toPayload } from './etc/apiHelpers'
import { URLHandler } from './etc/URLHandler';
import * as tp from "./types"
import {memoize} from "./etc/cacher"

const baseurl = URLHandler.basicURL()
const backendURL = baseurl + "/api"

function sentenceToKeywords(sentence: string): Promise<string[]> {
        const route = "/sentence-to-keywords"
        let toSend = { sentence }
        const url = makeUrl(backendURL + route, toSend)
        console.log("--- GET " + url);
        return json(url)
}

function getNNeurons(): Promise<number> {
    const route = "/n-heads"
    const url = makeUrl(backendURL + route, {})
    console.log("--- GET " + url)
    return json(url)
}

function getNeuronConcepts(neuron_idx: number, n_show: number=20): Promise<number> {
    const route = "/memory-concepts"
    let toSend = { head_index:neuron_idx, n_show }
    const url = makeUrl(backendURL + route, toSend)
    console.log("--- GET " + url);
    return json(url)
}

function getNeuronOrdering(): Promise<number[]> {
    const route = "/mem-order"
    const url = makeUrl(backendURL + route, {})
    console.log("--- GET " + url);
    return json(url)
}

function queryTopNeuronsByPhrase(phrase: string, beta:number=10.0): Promise<tp.TopMemResponse> {
    const route = "/query-top-mems-by-phrase"
    let toSend = { phrase, beta }
    const url = makeUrl(backendURL + route, toSend)
    console.log("--- GET " + url);
    return json(url)
}

export const api = {
    findResponseJson: (s) => "Using live API, no JSON",
    sentenceToKeywords: memoize(sentenceToKeywords),
    getNNeurons: memoize(getNNeurons),
    getNeuronConcepts: memoize(getNeuronConcepts),
    getNeuronOrdering: memoize(getNeuronOrdering),
    queryTopNeuronsByPhrase: memoize(queryTopNeuronsByPhrase)
}