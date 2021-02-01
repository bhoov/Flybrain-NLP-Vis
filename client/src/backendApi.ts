import {json} from 'd3';
import { makeUrl, toPayload } from './etc/apiHelpers'
import { URLHandler } from './etc/URLHandler';
import * as tp from "./types"

const baseurl = URLHandler.basicURL()

export class API {

    constructor(private baseURL: string = null) {
        if (this.baseURL == null) {
            this.baseURL = baseurl + '/api';
        }
    }

    sentenceToKeywords(sentence: string): Promise<string[]> {
        const route = "/sentence-to-keywords"
        let toSend = { sentence }
        const url = makeUrl(this.baseURL + route, toSend)
        console.log("--- GET " + url);
        return json(url)
    }

    sentenceToTokens(sentence: string): Promise<string[]> {
        const route = "/sentence-to-tokens"
        let toSend = { sentence }
        const url = makeUrl(this.baseURL + route, toSend)
        console.log("--- GET " + url);
        return json(url)
    }

    getNNeurons(): Promise<number> {
        const route = "/n-heads"
        const url = makeUrl(this.baseURL + route, {})
        console.log("--- GET " + url)
        return json(url)
    }

    // Don't let user choose beta
    // getNeuronConcepts(head_index: number, n_show: number, beta:number): Promise<tp.Concept[]> {
    getNeuronConcepts(neuron_idx: number, n_show: number=20): Promise<tp.Concept[]> {
        const route = "/memory-concepts"
        let toSend = { head_index:neuron_idx, n_show }
        const url = makeUrl(this.baseURL + route, toSend)
        console.log("--- GET " + url);
        return json(url)
    }

    getNeuronOrdering(): Promise<number[]> {
        const route = "/mem-order"
        const url = makeUrl(this.baseURL + route, {})
        console.log("--- GET " + url);
        return json(url)
    }

    queryTopNeuronsByPhrase(phrase: string, beta:number=10.0): Promise<tp.TopMemResponse> {
        const route = "/query-top-mems-by-phrase"
        let toSend = { phrase, beta }
        const url = makeUrl(this.baseURL + route, toSend)
        console.log("--- GET " + url);
        return json(url)
    }
};

export const api = new API()