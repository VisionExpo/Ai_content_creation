import api from './config';

export const generateVideo = async (videoData) => {
  try {
    const response = await api.post('/generate_video_concept', videoData);
    return response.data;
  } catch (error) {
    console.error('Error generating video:', error);
    throw error;
  }
};
