<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white transition-colors duration-500">
    <!-- Sidebar -->
    <aside class="w-64 bg-white dark:bg-gray-800 shadow-lg p-6">
      <h1 class="text-2xl font-bold text-primary mb-6">관리자 Dashboard</h1>
      <nav class="flex flex-col gap-4">
        <a href="#" class="px-4 py-2 rounded-lg font-medium hover:bg-primary hover:text-white">Dashboard</a>
        <router-link to="/admin/users" class="px-4 py-2 rounded-lg font-medium hover:bg-primary hover:text-white">회원관리</router-link>
        <a href="#" class="px-4 py-2 rounded-lg font-medium hover:bg-primary hover:text-white">Customers</a>
        <a href="#" class="px-4 py-2 rounded-lg font-medium hover:bg-primary hover:text-white">Reports</a>
        <a href="#" class="px-4 py-2 rounded-lg font-medium hover:bg-primary hover:text-white">Settings</a>
      </nav>
    </aside>

    <!-- Main -->
    <main class="flex-1 p-8 space-y-10">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-bold">Dashboard</h2>
          <p class="text-gray-500 dark:text-gray-400">Sales overview & insights</p>
        </div>
        <div class="flex items-center gap-4">
          <input
            type="text"
            placeholder="Search..."
            class="px-4 py-2 rounded-lg border dark:bg-gray-700"
          />
          <button
            @click="toggleDarkMode"
            class="bg-accent text-white px-4 py-2 rounded-lg shadow"
          >
            Toggle Mode
          </button>
        </div>
      </div>

      <!-- KPI -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="kpi in kpis"
          :key="kpi.label"
          class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow"
        >
          <h3 class="text-sm text-gray-500 dark:text-gray-400">{{ kpi.label }}</h3>
          <p class="text-2xl font-bold mt-2">{{ kpi.value }}</p>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold mb-4">Sales Trend</h3>
          <canvas ref="salesChart"></canvas>
        </div>
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold mb-4">Customer Growth</h3>
          <canvas ref="customersChart"></canvas>
        </div>
      </div>

      <!-- Profile -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow">
        <h3 class="text-lg font-semibold mb-4">Admin Profile</h3>
        <div class="flex items-center gap-6">
          <img
            src="https://i.pravatar.cc/100?img=3"
            class="w-20 h-20 rounded-full"
          />
          <div>
            <h4 class="text-xl font-bold">Alex Jordan</h4>
            <p class="text-gray-500 dark:text-gray-400">Senior Analyst</p>
            <button class="mt-2 px-4 py-2 bg-primary text-white rounded-lg">
              Edit Profile
            </button>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow">
        <h3 class="text-lg font-semibold mb-4">Recent Sales</h3>
        <table class="w-full text-left">
          <thead>
            <tr>
              <th class="py-2">Customer</th>
              <th class="py-2">Product</th>
              <th class="py-2">Amount</th>
              <th class="py-2">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in sales" :key="row.customer">
              <td class="py-2">{{ row.customer }}</td>
              <td class="py-2">{{ row.product }}</td>
              <td class="py-2">{{ row.amount }}</td>
              <td class="py-2">{{ row.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import Chart from "chart.js/auto"

const salesChart = ref(null)
const customersChart = ref(null)

const toggleDarkMode = () => {
  document.documentElement.classList.toggle("dark")
}

const kpis = [
  { label: "Total Sales", value: "$154,300" },
  { label: "New Customers", value: "1,203" },
  { label: "Pending Orders", value: "317" },
  { label: "Support Tickets", value: "45" },
]

const sales = [
  { customer: "Jane Smith", product: "Consulting Plan", amount: "$5,000", date: "Apr 10" },
  { customer: "Michael Rose", product: "CRM Package", amount: "$3,500", date: "Apr 11" },
  { customer: "Sarah Lee", product: "Analytics", amount: "$2,800", date: "Apr 12" },
]

onMounted(() => {
  new Chart(salesChart.value, {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr"],
      datasets: [
        {
          label: "Sales",
          data: [12000, 15000, 18000, 20000],
          borderWidth: 2,
        },
      ],
    },
  })

  new Chart(customersChart.value, {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr"],
      datasets: [
        {
          label: "New Customers",
          data: [300, 400, 450, 500],
        },
      ],
    },
  })
})
</script>
