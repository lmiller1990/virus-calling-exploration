
<script setup lang="ts">
    import { computed } from 'vue'
        import { DIV } from "./constants"

        export interface GeneInfo {
                        start: number,
                        end: number,
                        sequence: string,
                        }

        const props = defineProps<{
                gene: GeneInfo
                }>()

        const getStyle = computed(() => {
                return {
                        width: `${(props.gene.end - props.gene.start)/DIV}px`,
                        left: `${(props.gene.start)/DIV}px`
                }
        })
</script>

<template>
    <div :style="getStyle" class="absolute h-full cursor-pointer border-x-gray-500 border-x-2">
        <slot />
    </div>
</template>
