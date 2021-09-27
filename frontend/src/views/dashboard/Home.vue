<template>
  <div class="flex justify-between px-4 mt-4 sm:px-8">
    <h2 class="text-2xl text-gray-600">Magic Collections</h2>

    <div class="flex items-center space-x-1 text-xs">
      <a href="#" class="font-bold text-indigo-700">Home</a>
      <svg xmlns="http://www.w3.org/2000/svg" class="h-2 w-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
      <span class="text-gray-600">Magic Collections</span>
    </div>
  </div>

  <div class="grid grid-cols-1 gap-4 px-4 mt-8 sm:grid-cols-4 sm:px-8">
    <div v-for="(stat, index) in stats" :key="stat.title">
      <div class="flex items-center bg-white border rounded-sm overflow-hidden shadow">
        <div :class="'p-4 bg-' + colors[index] + '-400'">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-12 w-12 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"
            />
          </svg>
        </div>
        <div class="px-4 text-gray-700">
          <h3 class="text-sm tracking-wider">{{ stat.title }}</h3>
          <p class="text-3xl">{{ stat.number }}</p>
        </div>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 px-4 gap-4 mt-8 sm:grid-cols-3 sm:px-8">
    <div v-for="collection in collections" :key="collection.name">
      <div class="px-4 py-2 bg-white border rounded-md overflow-hidden shadow">
        <h3 class="text-xl text-gray-600 mb-4">{{ collection.name }}</h3>
        <apexchart type="area" :height="300" :options="chartOptions" :series="collection.value_history"></apexchart>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import { ref } from 'vue'

export default {
  components: {
    apexchart: VueApexCharts,
  },

  setup() {
    const host = 'http://127.0.0.1:5000'

    const collections = ref([])

    async function getCollections() {
      const response = await fetch(`${host}/api/collections`)
      collections.value = await response.json()
    }
    getCollections()

    const stats = ref([])

    async function getStats() {
      const response = await fetch(`${host}/api/stats`)
      stats.value = await response.json()
    }
    getStats()

    const chartOptions = {
      chart: {
        id: 'pageview-chart',
        toolbar: {
          show: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
    }

    var colors = ['blue', 'green', 'red', 'yellow', 'indigo', 'purple']

    return {
      chartOptions,
      stats,
      collections,
      colors,
    }
  },
}
</script>
