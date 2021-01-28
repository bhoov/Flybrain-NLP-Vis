<script lang="ts">
    export let neuronID: number | null // This can theoretically be handled by the content
    export let neuronLabel: number | null
    export let show: boolean = false
    export let width: number
    export let height: number
    export let x: number
    export let y: number
    export let defaultPosition: string = "top-middle"
</script>

<style lang="postcss">
    .float-window {
        border: black solid 3px;
    }
</style>

<div class="float-window absolute">
    <p>WORKING?</p>
</div>