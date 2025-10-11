import api from '@/modules/auth/services/authServices'; // Importamos la instancia configurada

export interface DiaryEntryPayload {
  title: string;
  content: string;
  selected_emotions: string[];
  emotion_summary: { [key: string]: number };
}

// ----------------------------------------------------------------------
// RUTAS DE DIARIO (Protegidas por JWT)
// ----------------------------------------------------------------------

export const getDiaryEntries = async () => {
  // Usa la instancia 'api' para que el interceptor añada el token
  return api.get('diary-entries/');
};

export const createDiaryEntry = async (entryData: DiaryEntryPayload) => {
  return api.post('diary-entries/', entryData);
};

export const updateDiaryEntry = async (id: string, entryData: DiaryEntryPayload) => {
  return api.put(`diary-entries/${id}/`, entryData);
};

export const deleteDiaryEntry = async (id: string) => {
  return api.delete(`diary-entries/${id}/`);
};
