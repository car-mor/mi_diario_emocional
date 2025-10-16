import { api } from '@/modules/auth/services/authServices'; // Reutilizamos la instancia de axios
import type { AxiosResponse } from 'axios';

// --- INTERFACES ---

// Interfaz para los datos que vienen del backend
export interface DiaryEntryFromAPI {
  id: string;
  patient: string; // El backend devuelve el UUID del paciente
  title: string;
  entry_date: string; // ISO string
  content: string;
  selected_emotions: string[];
  emotion_summary: EmotionSummary;
  content_length: number;
}

// El tipo que ya tenías para el resumen de emociones
export type EmotionSummary = {
  [key: string]: number;
};

// Payload para CREAR una nueva entrada
export interface CreateDiaryEntryPayload {
  title: string;
  content: string;
  selected_emotions: string[];
  emotion_summary: EmotionSummary;
}

// Payload para ACTUALIZAR una entrada (todos los campos son opcionales)
export type UpdateDiaryEntryPayload = Partial<CreateDiaryEntryPayload>;


// --- FUNCIONES DE SERVICIO (API Calls) ---

// OBTENER todas las entradas del diario del usuario logueado
export const getDiaryEntries = async (): Promise<AxiosResponse<DiaryEntryFromAPI[]>> => {
  return api.get('diary-entries/');
};

// CREAR una nueva entrada en el diario
export const createDiaryEntry = async (data: CreateDiaryEntryPayload): Promise<AxiosResponse<DiaryEntryFromAPI>> => {
  return api.post('diary-entries/', data);
};

// ELIMINAR una entrada por su ID
export const deleteDiaryEntry = async (id: string): Promise<AxiosResponse> => {
  return api.delete(`diary-entries/${id}/`);
};

// ACTUALIZAR una entrada por su ID (usamos PATCH para actualizaciones parciales)
export const updateDiaryEntry = async (id: string, data: UpdateDiaryEntryPayload): Promise<AxiosResponse<DiaryEntryFromAPI>> => {
  return api.patch(`diary-entries/${id}/`, data);
};
