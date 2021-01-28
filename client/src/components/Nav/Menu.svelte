<!-- Modified from https://svelte.dev/repl/03f0be0c4dc54eb4af5a168f644f5c31?version=3.19.1 -->

<script>
    import routes from "./navLinks"
</script>

<style>
    a {
        color: black;
        text-decoration: none;
    }
</style>

<nav class="hidden text-gray-500 text-bold sm:block">
    {#each routes as route}
        {#if route.newTab}
        <a href={route.url} class="hover:text-gray-700 text-xl mx-2 hover:no-underline" target="_blank" rel="noopener noreferrer">{route.name}</a>
        {:else}
        <a href={route.url} class="hover:text-gray-700 text-xl mx-2 hover:no-underline">{route.name}</a>
        {/if}
    {/each}
</nav>