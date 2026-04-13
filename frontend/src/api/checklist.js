import { authAxios } from './config';

export const getProgress = async (sessionId) => {
  const response = await authAxios.get(`/api/v1/onboarding/${sessionId}/progress`);
  return response.data;
};

export const updateChecklistItem = async (itemId, status, notes = "") => {
  const response = await authAxios.patch(`/api/v1/checklist/${itemId}`, {
    status,
    notes
  });
  return response.data;
}
