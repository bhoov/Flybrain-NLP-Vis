import * as d3 from 'd3';
import { makeUrl, toPayload } from './etc/apiHelpers'
import { URLHandler } from './etc/URLHandler';
import * as tp from "./types"

const baseurl = "http://localhost:8000"

export class API {

    constructor(private baseURL: string = null, private makeDemoHashes: boolean = false) {
        if (this.baseURL == null) {
            this.baseURL = baseurl + '/api';
        }
    }

    sentenceToTokens(sentence: string): Promise<string[]> {
        const route = "/sentence-to-tokens"
        let toSend = { sentence }
        const url = makeUrl(this.baseURL + route, toSend)
        console.log("--- GET " + url);
        return d3.json(url)
    }

    // Don't let user choose beta
    // getMemoryConcepts(head_index: number, n_show: number, beta:number): Promise<tp.Concept[]> {
    getMemoryConcepts(head_index: number, n_show: number=20): Promise<tp.Concept[]> {
        const route = "/get-memory-concepts"
        let toSend = { head_index, n_show }
        const url = makeUrl(this.baseURL + route, toSend)
        console.log("--- GET " + url);
        return d3.json(url)
    }

    // attentionsFromTokens(tokens: string[], target_idx?: number, hash_length: number = 32): Promise<tp.AttentionResponse> {
    //     const route = "/attentions-from-tokens"
    //     let toSend = { tokens, target_idx, hash_length }
    //     // let toSend = { tokens, hashLength }
    //     const key = hash({ route, ...toSend })
    //     if (this.makeDemoHashes) {
    //         toSend['request_hash'] = key
    //     }

    //     const payload = toPayload(toSend)
    //     const url = makeUrl(this.baseURL + route)
    //     console.log("--- POST " + url);

    //     return d3.json(url, payload)
    //     //@ts-ignore
    //     // return checkDemoAPI(key, url, payload)
    // }

    // getKNearestContextIndependent(hash_query: number[], k: number=10, hash_length:number=32): Promise<{tokens: string[]}> {
    //     const route = "/get-k-nearest-context-independent"
    //     let toSend = { hash_query, k, hash_length }
    //     // let toSend = { tokens, hashLength }
    //     const key = hash({ route, ...toSend })
    //     if (this.makeDemoHashes) {
    //         toSend['request_hash'] = key
    //     }

    //     const payload = toPayload(toSend)
    //     const url = makeUrl(this.baseURL + route)
    //     console.log("--- POST " + url);

    //     return d3.json(url, payload)
    // }

    // getKNearestContextDependent(hash_query: number[], k: number=10, hash_length:number=32): Promise<tp.CorpusSentenceMatch[]> {
    //     const route = "/get-k-nearest-context-dependent"
    //     let toSend = { hash_query, k, hash_length }

    //     const key = hash({ route, ...toSend })
    //     if (this.makeDemoHashes) {
    //         toSend['request_hash'] = key
    //     }

    //     const payload = toPayload(toSend)
    //     const url = makeUrl(this.baseURL + route)
    //     console.log("--- POST " + url);

    //     return d3.json(url, payload)
    // }
};