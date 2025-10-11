// src/store/diary.ts
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { isAxiosError } from 'axios'; // Importamos el verificador de tipo de Axios
import * as DiaryService from '@/modules/diary/services/diaryService';

// Define la interfaz para una entrada del diario que viene del backend
export interface DiaryEntry extends DiaryService.DiaryEntryPayload {
  id: string;
  entry_date: string;
  // Añade otros campos de lectura si es necesario
}

export const useDiaryStore = defineStore('diary', () => {
  const entries = ref<DiaryEntry[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchEntries = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await DiaryService.getDiaryEntries();
      entries.value = response.data;
    } catch (err: unknown) { // <-- FIX: Usamos 'unknown'
      // Verificamos si es un error de Axios para extraer un mensaje legible
      if (isAxiosError(err) && err.response) {
         error.value = 'Error de la API (' + err.response.status + '): ' + (err.response.data.detail || 'Fallo de autenticación');
      } else {
         error.value = 'Error al cargar las entradas. ¿Estás logueado?';
      }
      console.error('Failed to fetch diary entries:', err);
    } finally {
      loading.value = false;
    }
  };

  const createEntry = async (entry: DiaryService.DiaryEntryPayload) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await DiaryService.createDiaryEntry(entry);
      entries.value.push(response.data);
      return response.data;
    } catch (err: unknown) { // <-- FIX: Usamos 'unknown'
      if (isAxiosError(err) && err.response) {
         error.value = 'Error al crear la entrada: ' + (err.response.data.detail || 'Datos inválidos.');
      } else {
         error.value = 'Error de conexión al crear la entrada.';
      }
      console.error('Failed to create diary entry:', err);
      throw err; // Es buena práctica lanzar el error para manejarlo en el componente
    } finally {
      loading.value = false;
    }
  };

  return {
    entries,
    loading,
    error,
    fetchEntries,
    createEntry,
  };
});
