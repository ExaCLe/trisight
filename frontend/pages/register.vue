<template>
    <UContainer>
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
                variant="soft"
                title="Email bereits registriert"
                :description="`Die Email ${email_error.value} ist bereits registriert.`"
                :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'gray', variant: 'link', padded: false }"
                v-if="email_error"
                @close="email_error = null"
            />
            <UButton type="submit">Register</UButton>
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
    username: string().required('Pflicht'),
    username: string()
        .required('Pflicht')
        .min(3, 'Mindestens 3 Zeichen')
        .test('unique-username', 'Benutzername wird bereits verwendet', async function (value) {
            if (value === '') {
                return true;
            }
            try {
                const response = await fetch(`http://localhost:8000/api/users/exists/${value}`);
            } catch (error) {
                return true; // assume it does not exist
            }
            const data = await response.json();
            return data.exists === false;
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

    try {
        const response = await $fetch('http://localhost:8000/api/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(state)
        })

        // login the user 
        const loginFormData = new FormData();
        loginFormData.append('username', state.username);
        loginFormData.append('password', state.password);

        const login_response = await $fetch('http://localhost:8000/api/users/login', {
            method: 'POST',
            body: loginFormData
        })

        // save the token in the local storage
        localStorage.setItem('token', login_response.token)

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
