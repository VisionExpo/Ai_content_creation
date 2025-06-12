import api from './config';

export const generateVideo = async (videoData) => {
  try {
    // Extract actual title from the full text if it contains "Video Title:"
    const titleMatch = videoData.video_title.match(/Video Title:\s*(.*?)(?:\s+Duration:|$)/);
    const title = titleMatch ? titleMatch[1].trim() : videoData.video_title;

    // Create query parameters
    const params = {
      video_title: title,
      duration: videoData.duration
    };

    // Use GET request with query parameters
    const response = await api.get('/videos', { params });
    return response.data;
  } catch (error) {
    console.error('Error generating video:', error);
    throw error;
  }
};
