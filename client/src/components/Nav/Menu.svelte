<!-- Modified from https://svelte.dev/repl/03f0be0c4dc54eb4af5a168f644f5c31?version=3.19.1 -->

<script>
    import routes from "./navLinks"
</script>

<style lang="postcss">
    .a-link {
        @apply text-xl mx-2 no-underline;
        color: black;
        text-decoration: none;
        border-bottom: none;
    }

    .a-link:hover {
        @apply text-gray-600;
    }

    .link {
        position: relative;
        display: inline-block;
    }

    .pypi-link {
        text-decoration: none;
        border: 0;
        position: absolute;
        right: 0;
        font-size: 14px;
        margin-top: -7px;
    }

    .pypi-link:hover a {
        @apply text-gray-800;
    }

    a {
        @apply text-gray-600;
        text-decoration: none;
    }
</style>

<nav class="hidden text-gray-500 text-bold sm:block font-semibold whitespace-no-wrap">
    {#each routes as route}
        {#if route.newTab}
            <div class="link">
                <a href={route.url} class="a-link" target="_blank" rel="noopener noreferrer">{route.name}</a>
                {#if route.name == "Code"}
                    <div class="pypi-link"><a href="https://pypi.org/project/flyvec/" target="_blank" class="">+ PyPI</a></div>
                {/if}
            </div>
        {:else}
            <div class="inline"><a href={route.url} class="a-link">{route.name}</a></div>
        {/if}
    {/each}
</nav>