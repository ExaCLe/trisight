<template>
  <UContainer class="max-w-xl mx-auto py-10">
    <h1 class="text-2xl font-bold mb-6">Todo List</h1>

    <!-- Form to Add Todo -->
    <UForm @submit.prevent="addTodo" class="flex items-center space-x-4">
      <UInput v-model="newTodo" placeholder="Enter todo" required class="flex-grow" />
      <UButton type="submit" color="primary">Add Todo</UButton>
    </UForm>

    <!-- List of Todos -->
    <UList class="mt-8 space-y-4">
      <UListItem v-for="todo in todos" :key="todo.id" class="flex justify-between items-center">
        <div>
          <strong>{{ todo.name }}</strong>
          <p class="text-sm text-gray-500">Created: {{ new Date(todo.created).toLocaleString() }}</p>
        </div>
        <UButton color="red" @click="deleteTodo(todo.id)">Delete</UButton>
      </UListItem>
    </UList>
  </UContainer>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAPI } from '~/composables/useAPI'

const newTodo = ref('')
const todos = ref([])

const fetchTodos = async () => {
  const { data } = await useAPI('/api/todos')
  todos.value = data.value
}

const addTodo = async () => {
  if (!newTodo.value.trim()) return

  const { data } = await useAPI('/api/todos', {
    method: 'POST',
    body: { name: newTodo.value }
  })

  todos.value.push(data.value)
  newTodo.value = ''
}

const deleteTodo = async (id) => {
  await useAPI(`/api/todos/${id}`, {
    method: 'DELETE'
  })

  todos.value = todos.value.filter(todo => todo.id !== id)
}

onMounted(fetchTodos)
</script>
