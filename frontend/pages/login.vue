<template>
    <UContainer class="container">
        <UAlert
            icon="i-heroicons-command-line"
            color="red"
            variant="subtle"
            title="Email oder Passwort falsch"
            :description="`Die eingegebene Email oder das Passwort ist falsch. Bitte überprüfen Sie Ihre Eingabe.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
            v-if="incorrect_error"
            @close="incorrect_error = null"
            class="mb-4"
        />
        <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
            <!-- Email -->
            <UFormGroup label="Email" name="email" >
                <UInput v-model="state.email" />
            </UFormGroup>

            <!-- Password -->
            <UFormGroup label="Password" name="password" >
                <UInput v-model="state.password" type="password" />
            </UFormGroup>
            <UAlert
                icon="i-heroicons-command-line"
                color="red"
                variant="subtle"
                title="Server Error"
                :description="`Entschuldigung, es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.`"
                :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
                v-if="other_error"
                @close="other_error = null"
                class="mt-4"
            />
            <!-- Buttons and Forgot Password Link -->
            <div class="flex items-center space-x-4 mt-4">
                <UButton type="submit" class="bg-blue-dianne-900">Login</UButton>
                <UButton
                    type="button"
                    @click="navigateTo('/register')"
                    class="border-blue-dianne-900 text-color-blue-dianne-900"
                    variant="outline"
                >
                    Register
                </UButton>
                <span
                    class="text-blue-dianne-900 cursor-pointer underline"
                    @click="navigateTo('/forgot-password')"
                >
                    Forgot Password?
                </span>
            </div>
        </UForm>
    </UContainer>
</template>

<script setup>
import {object, string } from 'yup'
const config = useRuntimeConfig();

const schema = object({
    email: string().email('Ungültige Email').required('Pflicht'),
    password: string().required("Pflicht"),
})

const state = reactive({
    email: '',
    password: '',
})

const incorrect_error = ref(false)
const other_error = ref(null)

async function onSubmit(event) {
    event.preventDefault()

    try {
        // login the user 
        const loginFormData = new FormData();
        loginFormData.append('username', state.email);
        loginFormData.append('password', state.password);

        const login_response = await $fetch(`${config.public.backendUrl}/api/users/login`, {
            method: 'POST',
            body: loginFormData
        })

        // save the token in the local storage
        localStorage.setItem('token', login_response.access_token)

        // redirect to the dashboard
        await navigateTo('/')
        location.reload()
    } catch (error) {
        if (error.status === 401 && error.data?.detail === 'Incorrect email or password') {
            incorrect_error.value = true
        } else {
            other_error.value = error
        }
    }
}

</script>

<style scoped>
.container {
    height: 60vh;
    padding: 50px
}
</style>