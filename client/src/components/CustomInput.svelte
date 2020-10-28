<script lang="ts">
    export let min: number = 0
    export let max: number = 10
    export let value: number = 0
    export let step: number = 1

    if (value < min) {
        value = min
    }

    function inc() {
        value = value + step < max ? value + step : max
    }

    function dec() {
        value = value - step > min ? value - step : min
    }
</script>

<style>
    /* your styles go here */
</style>

<!-- markup (zero or more items) goes here -->
<div class="place-self-center">
    <div id="up" on:click={inc}>
        ^
    </div>

    <div>{value}</div>

    <div id="down" on:click={dec}>
        v
    </div>
</div>