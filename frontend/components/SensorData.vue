<template>
  <div class="flex flex-col">
    <h1 class="text-3xl text-orange-700">Sensor Data</h1>
    <table class="border-separate border border-slate-500">
      <tr class="bg-blue-200">
        <td class="border border-slate-200 ">Device ID</td>
        <td class="border border-slate-200 ">Moisture</td>
        <td class="border border-slate-200 ">Temperature</td>
        <td class="border border-slate-200 ">Timestamp</td>
      </tr>
      <tr v-for="(sensor_log, idx) in selectedDeviceData.value" :key="`${idx}-row`">
        <td :key="`${idx}-row-1-col`">{{ Number.parseFloat(selectedDevice).toFixed(0) }}</td>
        <td :key="`${idx}-row-2-col`">{{ Number.parseFloat(sensor_log.moisture).toFixed(2) * 100 }}</td>
        <td :key="`${idx}-row-3-col`">{{ Number.parseFloat(sensor_log.temperature_celcius).toFixed(1) }}</td>
        <td :key="`${idx}-row-4-col`">{{ sensor_log.timestamp }}</td>
      </tr>
    </table>

    <select class="w-36" v-model="selectedDevice">
      <option v-for="sensor in sensors" :value="sensor.id" :key="sensor.id">{{ sensor.name }}</option>
    </select>
    <div class="px-6 w-36 bg-slate-200 hover:bg-slate-500">
      <button @click="refreshData">Reload Data</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const { data: sensors } = await useFetch('http://localhost:8000/devices');
const selectedDevice = ref(undefined);
const selectedDeviceData = ref([]);
watch(selectedDevice, async (newVal, oldVal) => {
  const { data } = await useFetch(`http://localhost:8000/devices/${selectedDevice.value}/temperature_moisture_logs`);
  selectedDeviceData.value = data;
});

const refreshData = async () => {
  if (!selectedDevice.value) {
    return;
  }
  const { data } = await useFetch(`http://localhost:8000/devices/${selectedDevice.value}/temperature_moisture_logs`);
  selectedDeviceData.value = data;
}


</script>