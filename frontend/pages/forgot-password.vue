<template>
    <UContainer class="container">
        <h1 class="text-2xl font-bold mb-4">Passwort vergessen</h1>
        <p class="mb-6">
            Sie sind dabei, eine Anfrage zu stellen, um Ihr Passwort zurückzusetzen.
            Geben Sie bitte Ihre Email-Adresse ein, um eine E-Mail zum Zurücksetzen Ihres Passworts zu erhalten.
        </p>

        <UAlert
            icon="i-heroicons-command-line"
            color="red"
            variant="subtle"
            title="Email nicht gefunden"
            :description="`Die eingegebene Email-Adresse ist nicht registriert.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
            v-if="email_not_found_error"
            @close="email_not_found_error = null"
            class="mb-4"
        />

        <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
            <!-- Email Input -->
            <UFormGroup label="Email" name="email">
                <UInput v-model="state.email" />
            </UFormGroup>

            <!-- Submit Button -->
            <UButton type="submit" class="bg-blue-dianne-900">Senden</UButton>
        </UForm>

        <UAlert
            icon="i-heroicons-check-circle"
            color="green"
            variant="subtle"
            title="Email gesendet"
            :description="`Eine E-Mail zum Zurücksetzen Ihres Passworts wurde an die angegebene Adresse gesendet.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
            v-if="email_sent_success"
            @close="email_sent_success = null"
            class="mt-4"
        />
    </UContainer>
</template>

<script setup>
import { object, string } from 'yup'
import { reactive, ref } from 'vue'
const config = useRuntimeConfig();

// Form validation schema using yup
const schema = object({
    email: string().email('Ungültige Email').required('Pflicht'),
})

// State for form input
const state = reactive({
    email: '',
})

const email_not_found_error = ref(false)
const email_sent_success = ref(false)

async function onSubmit(event) {
    event.preventDefault()

    try {
        // Send request to backend to issue the reset password email
        const response = await $fetch(`${config.public.backendUrl}/api/users/forgot-password`, {
            method: 'POST',
            body: { email: state.email }
        })

        // If successful, show success alert
        email_sent_success.value = true
    } catch (error) {
        // If email is not found, show an error alert
        if (error.status === 404 && error.data?.detail === 'User not found') {
            email_not_found_error.value = true
        } else {
            // Handle other errors
            console.error('An error occurred:', error)
        }
    }
}
</script>

<style scoped>
.container {
    height: 60vh;
    padding: 50px;
}

.text-2xl {
    font-size: 1.5rem;
}

.font-bold {
    font-weight: bold;
}

.mb-4 {
    margin-bottom: 1rem;
}

.mb-6 {
    margin-bottom: 1.5rem;
}

.bg-blue-dianne-900 {
    background-color: #0D3B66;
}

.text-color-blue-dianne-900 {
    color: #0D3B66;
}
</style>
