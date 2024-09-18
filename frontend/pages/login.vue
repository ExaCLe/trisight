<template>
    <UContainer>
        <UAlert
            icon="i-heroicons-command-line"
            color="red"
            variant="soft"
            title="Email oder Passwort falsch"
            :description="`Die eingegebene Email oder das Passwort ist falsch. Bitte überprüfen Sie Ihre Eingabe.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'gray', variant: 'link', padded: false }"
            v-if="incorrect_error"
            @close="incorrect_error = null"
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
            <UButton type="submit">Login</UButton>
            <UButton type="button" @click="navigateTo('/register')">Register</UButton>
        </UForm>
        <UAlert
            icon="i-heroicons-command-line"
            color="red"
            variant="solid"
            title="Server Error"
            :description="`Entschuldigung, es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.`"
            :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'gray', variant: 'link', padded: false }"
            v-if="other_error"
            @close="other_error = null"
        />
        
    </UContainer>
</template>

<script setup>
import {object, string } from 'yup'

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

        const login_response = await $fetch('http://localhost:8000/api/users/login', {
            method: 'POST',
            body: loginFormData
        })

        // save the token in the local storage
        localStorage.setItem('token', login_response.token)

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