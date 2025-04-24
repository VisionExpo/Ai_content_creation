import api from './config';

export const generateAd = async (adData) => {
  try {
    const response = await api.post('/generate_ad', adData);
    return response.data;
  } catch (error) {
    console.error('Error generating ad:', error);
    throw error;
  }
};
