

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-sm bg-white shadow rounded-2xl p-6">
      <h1 class="text-2xl font-semibold mb-6">Accedi al CRM</h1>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full rounded-xl border px-3 py-2 focus:outline-none focus:ring"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full rounded-xl border px-3 py-2 focus:outline-none focus:ring"
          />
        </div>
        <button
          type="submit"
          class="w-full rounded-xl bg-blue-600 text-white py-2 hover:bg-blue-700"
        >
          Entra
        </button>
        <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
      </form>
    </div>
  </div>
</template>


<script setup>
const email = ref("admin@example.com");
const password = ref("Password!123");
const error = ref("");
const { login } = useAuth();

const onSubmit = async () => {
  error.value = "";
  try {
    await login(email.value, password.value);
    navigateTo("/dashboard");
  } catch (e) {
    error.value = e?.data?.detail || "Credenziali non valide";
  }
};
</script>