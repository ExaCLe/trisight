<template>
    <UContainer class="container">
        <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
            <!-- Email -->
            <UFormGroup label="Email" name="email" >
                <UInput v-model="state.email" />
            </UFormGroup>

            <!-- Username -->
            <UFormGroup label="Username" name="username" >
                <UInput v-model="state.username" />
            </UFormGroup>

            <!-- Password -->
            <UFormGroup label="Password" name="password" >
                <UInput v-model="state.password" type="password" />
            </UFormGroup>
            <UAlert
                icon="i-heroicons-command-line"
                color="red"
                variant="subtle"
                title="Email bereits registriert"
                :description="`Die Email ist bereits registriert.`"
                :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
                v-if="email_error"
                @close="email_error = null"
            />
            <UAlert
                icon="i-heroicons-command-line"
                color="red"
                variant="subtle"
                title="Server Error"
                :description="`Entschuldigung, es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.`"
                :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'white', variant: 'link', padded: false }"
                v-if="other_error"
                @close="other_error = null"
            />
            <UButton type="submit" class="bg-blue-dianne-900">Register</UButton>
            <UButton type="button" @click="navigateTo('/login')" class="ml-4 border-blue-dianne-900 text-color-blue-dianne-900" variant="outline">Login</UButton>
        </UForm>
        
    </UContainer>
</template>

<script setup>
import {object, string } from 'yup'

const config = useRuntimeConfig();

const schema = object({
    email: string().email('Ungültige Email').required('Pflicht'),
    username: string()
        .required('Pflicht')
        .min(3, 'Mindestens 3 Zeichen')
        .test('unique-username', 'Benutzername wird bereits verwendet', async function (value) {
            if (value === '') {
                return true;
            }
            try {
                const response = await fetch(`${config.public.backendUrl}/api/users/exists/${value}`);
                const data = await response.json();
                return data.exists === false;
            } catch (error) {
                console.error(error)
                return true; // assume it does not exist
            }
        }),
    password: string().required("Pflicht").min(8, "Mindestens 8 Zeichen"),
})

const state = reactive({
    email: '',
    username: '',
    password: '',
})

const email_error = ref(null)

const other_error = ref(null)

async function onSubmit(event) {
    event.preventDefault()

    other_error.value = null
    email_error.value = null

    try {
        const response = await $fetch(`${config.public.backendUrl}/api/users/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(state)
        })

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
    } catch (error) {
        if (error.status === 400 && error.data?.detail === 'Email already registered') {
            email_error.value = state.email
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
</style>˚
