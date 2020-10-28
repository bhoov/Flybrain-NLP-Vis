<script lang="ts">
    export let tokens: string[] 
</script>

{#each tokens as token, i}
    <span class="px-2 py-1 mx-1 mb-3 border-solid border border-gray-600 bg-gray-300 .rounded-sm">{token}</span>
{/each}