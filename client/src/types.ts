export interface Concept {
    token: string
    contribution: number
}

export interface MemActivation {
    head: number
    activation: number
}

export interface TopMemResponse {
    tokenized_phrase: string[]
    head_info: MemActivation[]
}