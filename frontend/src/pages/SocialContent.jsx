import { useState } from 'react'
import { generateSocialContent } from '../api/socialContentService'

const SocialContent = () => {
  const [formData, setFormData] = useState({
    content_title: '',
    platform: 'instagram'
  })
  
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      const response = await generateSocialContent(formData)
      setResult(response)
    } catch (err) {
      setError('Failed to generate social content. Please try again.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Social Media Content Generator</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Create Social Content</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="content_title" className="block text-sm font-medium text-gray-700 mb-1">
                  Content Title/Topic
                </label>
                <input
                  type="text"
                  id="content_title"
                  name="content_title"
                  value={formData.content_title}
                  onChange={handleChange}
                  className="input-field"
                  required
                  placeholder="e.g., New Product Launch, Summer Sale, etc."
                />
              </div>
              
              <div>
                <label htmlFor="platform" className="block text-sm font-medium text-gray-700 mb-1">
                  Social Media Platform
                </label>
                <select
                  id="platform"
                  name="platform"
                  value={formData.platform}
                  onChange={handleChange}
                  className="input-field"
                  required
                >
                  <option value="instagram">Instagram</option>
                  <option value="facebook">Facebook</option>
                  <option value="twitter">Twitter</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="tiktok">TikTok</option>
                </select>
              </div>
              
              {error && (
                <div className="text-red-600 text-sm">{error}</div>
              )}
              
              <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Generating...' : 'Generate Content'}
              </button>
            </form>
          </div>
          
          <div className="mt-6 card bg-gray-50">
            <h3 className="text-lg font-semibold mb-3">Tips for Great Social Content</h3>
            <ul className="list-disc pl-5 space-y-2 text-gray-700">
              <li>Be specific about your topic to get more targeted content</li>
              <li>Different platforms have different content styles and lengths</li>
              <li>Consider your audience demographics when selecting a platform</li>
              <li>Add relevant hashtags to increase visibility</li>
              <li>Include a clear call-to-action in your posts</li>
            </ul>
          </div>
        </div>
        
        <div>
          <div className="card h-full">
            <h2 className="text-xl font-semibold mb-4">Generated Content</h2>
            
            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
              </div>
            ) : result ? (
              <div className="bg-gray-50 p-4 rounded-md border border-gray-200 min-h-[300px]">
                <div className="mb-3">
                  <span className="inline-block bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full font-medium capitalize">
                    {formData.platform}
                  </span>
                </div>
                
                <p className="whitespace-pre-line">{result.message}</p>
                
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => navigator.clipboard.writeText(result.message)}
                    className="btn btn-secondary text-sm flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                    Copy to Clipboard
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <p>Fill out the form and click "Generate Content" to create your social media post</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SocialContent
