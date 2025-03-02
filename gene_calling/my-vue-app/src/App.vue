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


const tracks = [
    { 
        label: "Prodigal",
        genes: genes.prodigal,
        class: 'bg-blue-500 hover:bg-blue-500'
    },
    { 
        label: "Glimmer",
        genes: genes.glimmer,
        class: 'bg-red-500 hover:bg-red-500'
    }
]
</script>

<template>
    <div class="flex flex-col justify-between h-screen">
        <div class="overflow-x-auto pb-[15px]">
            <div class="bg-gray-200">
                <div v-for="track of tracks" :key="track.label" class="flex">
                    <Track>
                    <template #label>
                        <div>{{ track.label }}</div>
                    </template>

                    <Gene v-for="gene in track.genes" :gene="gene" :class="track.class" @click="() => handleGeneInfo(gene)"  />
                    </Track>
                </div>

                <Track>
                <template #label>
                    <div>Coordinates</div>
                </template>
                <Gene v-for="gene in fakeGenes" :gene="gene" class="whitespace-pre text-xs pt-2 border-l-0 border-x-gray-100 border-dotted">
                {{ ` ${gene.start}` }}
                </Gene>
                </Track>
            </div>
        </div>

        <div class="h-80">
            <div v-if="selectedGene" class="break-all p-4">
                <p>Start: {{ selectedGene.start }}</p>
                <p>End: {{ selectedGene.end }}</p>
                <p>Sequence: {{ selectedGene.sequence }}</p>
            </div>
        </div>

    </div>
</template>
