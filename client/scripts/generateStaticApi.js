#!/usr/bin/env node

/**
 * Run with `node --experimental-modules generateStaticApi.js
 */
import * as api from "./api.js"
const [,, ...args] = process.argv

console.log("Hello World?: ", args)
console.log("foo: ", api.foo().then(r => console.log(r)))