
<script setup lang="ts">
        import { computed } from 'vue'

        export interface GeneInfo {
                        start: number,
                        end: number,
                        sequence: string,
                        }

        const props = defineProps<{
                gene: GeneInfo
                }>()

        const DIV = 5

        const getStyle = computed(() => {
                return {
                        width: `${(props.gene.end - props.gene.start)/DIV}px`,
                        left: `${(props.gene.start)/DIV}px`
                }
        })
</script>

<template>

        <div :style="getStyle" class="absolute h-full cursor-pointer">
        </div>
</template>
