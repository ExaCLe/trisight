<template>
  <div>
    <h1>Todo List</h1>

    <!-- Form to Add Todo -->
    <form @submit.prevent="addTodo">
      <input v-model="newTodo" placeholder="Enter todo" required />
      <button type="submit">Add Todo</button>
    </form>

    <!-- List of Todos -->
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        {{ todo.name }} (Created: {{ new Date(todo.created).toLocaleString() }})
        <button @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>
  </div>
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
