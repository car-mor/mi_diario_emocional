import { ref } from 'vue';
import { defineStore } from 'pinia';
import { isAxiosError } from 'axios'; // Importamos el verificador de tipo de Axios
import * as DiaryService from '@/modules/diary/services/diaryServices';

// 1. Usamos la interfaz limpia del servicio
export type DiaryEntry = DiaryService.DiaryEntryFromAPI;

export const useDiaryStore = defineStore('diary', () => {
  const entries = ref<DiaryEntry[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // 2. Acción para obtener todas las entradas
  const fetchEntries = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await DiaryService.getDiaryEntries();
      entries.value = response.data;
    } catch (err: unknown) {
      if (isAxiosError(err) && err.response) {
         error.value = `Error ${err.response.status}: No se pudieron cargar las entradas.`;
      } else {
         error.value = 'Error de conexión al cargar las entradas.';
      }
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  // 3. Acción para añadir una nueva entrada
  const createEntry = async (entryData: DiaryService.CreateDiaryEntryPayload) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await DiaryService.createDiaryEntry(entryData);
      // Añadimos la nueva entrada al principio de la lista para que aparezca primero
      entries.value.unshift(response.data);
      return response.data;
    } catch (err: unknown) {
      if (isAxiosError(err) && err.response) {
        error.value = 'Error al crear la entrada: ' + (err.response.data.detail || 'Datos inválidos.');
      } else {
        error.value = 'Error de conexión al crear la entrada.';
      }
      console.error(err);
      throw err; // Lanza el error para que el componente también lo pueda manejar
    } finally {
      loading.value = false;
    }
  };

  // 4. NUEVA ACCIÓN: Eliminar una entrada
  const deleteEntry = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
        await DiaryService.deleteDiaryEntry(id);
        // Filtramos la lista para eliminar la entrada del estado local
        entries.value = entries.value.filter(entry => entry.id !== id);
    } catch(err) {
        // ... manejo de errores ...
        error.value = 'No se pudo eliminar la entrada.';
        throw err;
    } finally {
        loading.value = false;
    }
  };

  // 5. NUEVA ACCIÓN: Actualizar una entrada
  const updateEntry = async (id: string, updateData: DiaryService.UpdateDiaryEntryPayload) => {
    loading.value = true;
    error.value = null;
    try {
        const response = await DiaryService.updateDiaryEntry(id, updateData);
        const index = entries.value.findIndex(entry => entry.id === id);
        if (index !== -1) {
            // Reemplazamos el objeto antiguo con el nuevo del backend
            entries.value[index] = response.data;
        }
        return response.data;
    } catch(err) {
        // ... manejo de errores ...
        error.value = 'No se pudo actualizar la entrada.';
        throw err;
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
    deleteEntry, // <-- Exportar nueva acción
    updateEntry, // <-- Exportar nueva acción
  };
});
