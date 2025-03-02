<script setup lang="ts">
    import genes from "../genes.json"
        import Track from "./Track.vue"
        import { ref, computed } from 'vue'
        import Gene, { type GeneInfo } from "./Gene.vue"
        import { DIV } from "./constants"

        const selectedGene = ref<GeneInfo>()

        function handleGeneInfo(gene: GeneInfo) {
                selectedGene.value = gene
        }

        const length = 35000

        const fakeGenes = computed(() => {
            const fake: GeneInfo[] = []
            for (let i = 0; i < length; i+=1000) {
                fake.push({ start: i, end: i + 1000, sequence: "" })
            }
            return fake
        })

</script>

<template>
    <div class="flex flex-col justify-between h-screen">
        <div class="bg-gray-200">
            <div class="flex">
                <div>Prodigal</div>
                <Track>
                <Gene v-for="gene in genes.prodigal" :gene="gene" class="bg-blue-400 hover:bg-blue-500" @click="() => handleGeneInfo(gene)"  />
                </Track>
            </div>

            <div class="flex">
                <div>Glimmer</div>
            <Track>
            <Gene v-for="gene in genes.glimmer" :gene="gene"  class="bg-red-400 hover:bg-red-500" />
            </Track>
            </div>
            <Track>
            <Gene v-for="gene in fakeGenes" :gene="gene" class="whitespace-pre">
            {{ ` ${gene.end}` }}
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
