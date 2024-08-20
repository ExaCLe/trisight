import type { UseFetchOptions } from 'nuxt/app'

export function useAPI<T>(
    url: string | (() => string),
    options?: UseFetchOptions<T>,
) {
    const { $api } = useNuxtApp();
    return useFetch(url, {
        ...options,
        $fetch: $api,
    })
}