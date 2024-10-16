<template>
    <UContainer class="container">
        <h1 class="text-2xl font-bold mb-4">Passwort zurücksetzen</h1>
        <p class="mb-6">
            Sie können nun Ihr neues Passwort eingeben, um Ihr altes Passwort zu ersetzen. Nach erfolgreicher Zurücksetzung können Sie sich wieder einloggen.
        </p>

        <UAlert
            icon="i-heroicons-command-line"
            color="red"
            variant="subtle"
            title="Fehler bei der Zurücksetzung"
            :description="`Das Zurücksetzen des Passworts ist fehlgeschlagen. Bitte überprüfen Sie den Link oder versuchen Sie es später erneut.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
            v-if="reset_error"
            @close="reset_error = null"
            class="mb-4"
        />

        <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
            <!-- New Password -->
            <UFormGroup label="Neues Passwort" name="new_password">
                <UInput v-model="state.new_password" type="password" />
            </UFormGroup>

            <!-- Confirm Password -->
            <UFormGroup label="Passwort bestätigen" name="confirm_password">
                <UInput v-model="state.confirm_password" type="password" />
            </UFormGroup>

            <!-- Submit Button -->
            <UButton type="submit" :disabled="reset_success" class="bg-blue-dianne-900">Passwort zurücksetzen</UButton>
        </UForm>

        <UAlert
            icon="i-heroicons-check-circle"
            color="green"
            variant="subtle"
            title="Passwort erfolgreich zurückgesetzt"
            :description="`Ihr Passwort wurde erfolgreich zurückgesetzt. Sie können sich jetzt einloggen.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
            v-if="reset_success"
            @close="reset_success = null"
            class="mt-4"
        />

        <UButton v-if="reset_success" type="button" @click="navigateTo('/login')" class="mt-4 border-blue-dianne-900 text-color-blue-dianne-900" variant="outline">
            Zum Login
        </UButton>
    </UContainer>
</template>

<script setup>
import { object, string, ref as yupRef } from 'yup'
import { reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
const config = useRuntimeConfig();

// Form validation schema using yup
const schema = object({
    new_password: string().min(8, 'Das Passwort muss mindestens 8 Zeichen lang sein').required('Pflicht'),
    confirm_password: string()
        .oneOf([yupRef('new_password')], 'Passwörter stimmen nicht überein')
        .required('Pflicht'),
})

// Reactive state for form input
const state = reactive({
    new_password: '',
    confirm_password: '',
})

const route = useRoute()  // Get access to the current route to extract the token
const reset_error = ref(false)
const reset_success = ref(false)

async function onSubmit(event) {
    event.preventDefault()

    const token = route.query.token  // Extract the token from the query parameters

    if (!token) {
        reset_error.value = true
        return
    }

    try {
        // Send request to backend to reset the password
        const response = await $fetch(`${config.public.backendUrl}/api/users/reset-password`, {
            method: 'POST',
            body: { token, new_password: state.new_password },
        })

        // If successful, show success alert and disable further submissions
        reset_success.value = true
    } catch (error) {
        // If reset fails, show an error alert
        reset_error.value = true
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
