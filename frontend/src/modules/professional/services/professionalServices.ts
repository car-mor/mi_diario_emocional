import { api } from '@/modules/auth/services/authServices';
import type { AxiosResponse } from 'axios';

// Interfaz que coincide con el PatientListSerializer de Django
export interface Patient {
  id: string; // Django devuelve UUIDs como strings
  name: string;
  age: number;
  gender: string;
  email: string;
  alias: string;
  avatar_url: string;
}

// Interfaz para una entrada del diario (ajusta según tu DiaryEntrySerializer)
export interface DiaryEntry {
    id: string;
    title: string;
    entry_date: string;
    content: string;
    selected_emotions: string[];
    analyzed_emotions: string[];
}
// Interfaz para la información del reporte
export interface ReportInfo {
    is_available: boolean;
    next_report_date: string;
    is_custom_range: boolean;
}

export interface ReportWeek {
    week_number: number;
    start_date: string;
    end_date: string;
    display_text: string;
}

// Interfaz para la respuesta completa de la API
export interface PatientDetailsData {
    patient_details: Patient;
    diary_history: DiaryEntry[];
    emotion_combinations: [string, number][];
    word_frequency: [string, number][];
    report_info: ReportInfo;
}

// Obtener todos los detalles de un paciente por su ID
export const getPatientDetails = async (
  patientId: string,
  dates?: { startDate: string; endDate: string }
): Promise<AxiosResponse<PatientDetailsData>> => {
  const params = new URLSearchParams();
  if (dates?.startDate) params.append('start_date', dates.startDate);
  if (dates?.endDate) params.append('end_date', dates.endDate);
  return api.get(`professional/patients/${patientId}/`, { params });
};


// OBTENER la lista de semanas de reporte disponibles
export const getReportWeeks = async (patientId: string): Promise<AxiosResponse<ReportWeek[]>> => {
  return api.get(`professional/patients/${patientId}/report-weeks/`);
};
// ---
// Descargar el reporte en PDF de un paciente
export const downloadPatientReport = async (
    patientId: string,
    dates?: { startDate: string; endDate: string }
): Promise<AxiosResponse<Blob>> => {
    const params = new URLSearchParams();
    if (dates?.startDate) params.append('start_date', dates.startDate);
    if (dates?.endDate) params.append('end_date', dates.endDate);
    return api.get(`professional/patients/${patientId}/download-report/`, {
        responseType: 'blob',
        params
    });
};

// OBTENER la lista de pacientes vinculados
export const getLinkedPatients = async (): Promise<AxiosResponse<Patient[]>> => {
  return api.get('professional/patients/');
};

// DESVINCULAR un paciente por su ID
export const disconnectPatient = async (patientId: string): Promise<AxiosResponse> => {
  return api.post(`professional/patients/${patientId}/disconnect/`);
};


export const linkToProfessional = async (linkCode: string) => {
  return api.post('patient/link-professional/', { link_code: linkCode });
};
