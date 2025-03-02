<script setup lang="ts">
        import genes from "../genes.json"
        import Track from "./Track.vue"
        import { ref } from 'vue'
        import Gene, { GeneInfo } from "./Gene.vue"

        const selectedGene = ref<GeneInfo>()

        function handleGeneInfo(gene: GeneInfo) {
                selectedGene.value = gene
        }
</script>

<template>
        <div class="flex flex-col justify-between h-screen">
                <div class="bg-gray-200">
                        <Track>
                        <Gene v-for="gene in genes.prodigal" :gene="gene" class="bg-blue-400 hover:bg-blue-500" @click="() => handleGeneInfo(gene)" >
                        </Gene>
                        </Track>

                        <Track>
                        <Gene v-for="gene in genes.glimmer" :gene="gene"  class="bg-red-400 hover:bg-red-500">
                        </Gene>
                        </Track>
                </div>
                <div v-if="selectedGene" class="break-all p-4">
                        <p>Start: {{ selectedGene.start }}</p>
                        <p>End: {{ selectedGene.end }}</p>
                        <p>Sequence: {{ selectedGene.sequence }}</p>
                </div>

        </div>
</template>

<style scoped>
</style>
